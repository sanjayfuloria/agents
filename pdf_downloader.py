#!/usr/bin/env python3
"""
Generic PDF Downloader

A flexible program to download PDF documents from any website.
Can be configured to work with different website structures and patterns.

Author: AI Agent
Date: 2025
"""

import os
import json
import time
import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
from pathlib import Path
from typing import List, Dict, Optional, Union
import re
import hashlib


class PDFDownloader:
    """
    A generic PDF downloader that can extract and download PDF documents
    from any website based on configurable patterns and rules.
    """
    
    def __init__(self, 
                 base_url: str,
                 download_dir: str = "downloaded_pdfs",
                 config: Optional[Dict] = None):
        """
        Initialize the PDF downloader.
        
        Args:
            base_url: The website URL to scrape PDFs from
            download_dir: Directory to save downloaded PDFs
            config: Configuration dictionary for customizing behavior
        """
        self.base_url = base_url
        self.download_dir = Path(download_dir)
        self.session = requests.Session()
        
        # Default configuration
        self.config = {
            'request_timeout': 30,
            'download_timeout': 120,
            'delay_between_downloads': 1,
            'max_retries': 3,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'pdf_patterns': [
                r'.*\.pdf$',
                r'.*\.PDF$',
                r'.*\.pdf\?.*',
                r'.*\.PDF\?.*'
            ],
            'exclude_patterns': [
                r'.*\.php.*',
                r'.*download\.aspx.*'
            ],
            'link_selectors': [
                'a[href$=".pdf"]',
                'a[href$=".PDF"]',
                'a[href*=".pdf"]',
                'a[href*="pdf"]'
            ],
            'filename_max_length': 100,
            'create_subdirs': True,
            'preserve_structure': False,
            'verify_pdf_content': True
        }
        
        # Update with user-provided config
        if config:
            self.config.update(config)
        
        # Create download directory
        self.download_dir.mkdir(exist_ok=True, parents=True)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO, 
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Configure session
        self.session.headers.update({
            'User-Agent': self.config['user_agent']
        })
    
    def discover_pdf_links(self, url: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Discover PDF links on a webpage.
        
        Args:
            url: URL to scan (defaults to base_url)
            
        Returns:
            List of dictionaries containing PDF link information
        """
        target_url = url or self.base_url
        pdf_links = []
        
        try:
            self.logger.info(f"Scanning for PDF links on: {target_url}")
            response = self.session.get(
                target_url, 
                timeout=self.config['request_timeout']
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Method 1: Use CSS selectors
            for selector in self.config['link_selectors']:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href', '')
                    if href:
                        pdf_info = self._process_pdf_link(link, href, target_url)
                        if pdf_info and pdf_info not in pdf_links:
                            pdf_links.append(pdf_info)
            
            # Method 2: Pattern matching on all links
            all_links = soup.find_all('a', href=True)
            for link in all_links:
                href = link.get('href', '')
                if self._matches_pdf_pattern(href):
                    pdf_info = self._process_pdf_link(link, href, target_url)
                    if pdf_info and pdf_info not in pdf_links:
                        pdf_links.append(pdf_info)
            
            # Method 3: Look for embedded objects or iframes
            for tag in soup.find_all(['object', 'embed', 'iframe']):
                src = tag.get('src') or tag.get('data', '')
                if src and self._matches_pdf_pattern(src):
                    pdf_info = {
                        'url': urljoin(target_url, src),
                        'title': self._extract_title(tag, soup),
                        'filename': self._generate_filename(src),
                        'source_url': target_url,
                        'link_text': tag.get_text(strip=True)[:100]
                    }
                    if pdf_info not in pdf_links:
                        pdf_links.append(pdf_info)
            
            self.logger.info(f"Found {len(pdf_links)} PDF links")
            return pdf_links
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching webpage {target_url}: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Unexpected error discovering PDFs: {e}")
            return []
    
    def _process_pdf_link(self, link, href: str, base_url: str) -> Optional[Dict[str, str]]:
        """Process a potential PDF link and extract information."""
        # Skip if excluded by patterns
        if self._matches_exclude_pattern(href):
            return None
        
        # Get full URL
        full_url = urljoin(base_url, href)
        
        # Extract link information
        link_text = link.get_text(strip=True)
        title = self._extract_title(link, None)
        
        return {
            'url': full_url,
            'title': title,
            'filename': self._generate_filename(href, title),
            'source_url': base_url,
            'link_text': link_text[:100] if link_text else ''
        }
    
    def _matches_pdf_pattern(self, url: str) -> bool:
        """Check if URL matches any PDF pattern."""
        for pattern in self.config['pdf_patterns']:
            if re.search(pattern, url, re.IGNORECASE):
                return True
        return False
    
    def _matches_exclude_pattern(self, url: str) -> bool:
        """Check if URL matches any exclude pattern."""
        for pattern in self.config['exclude_patterns']:
            if re.search(pattern, url, re.IGNORECASE):
                return True
        return False
    
    def _extract_title(self, element, soup) -> str:
        """Extract a meaningful title from the element or surrounding context."""
        # Try title attribute
        title = element.get('title', '').strip()
        if title:
            return title
        
        # Try link text
        text = element.get_text(strip=True)
        if text and len(text) > 3:
            return text
        
        # Try alt attribute
        alt = element.get('alt', '').strip()
        if alt:
            return alt
        
        # Try nearby text elements
        if soup:
            # Look for heading elements near the link
            for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                if element in heading.find_all() or heading in element.find_parents():
                    heading_text = heading.get_text(strip=True)
                    if heading_text:
                        return heading_text
        
        # Look in parent elements
        parent = element.parent
        if parent:
            parent_text = parent.get_text(strip=True)
            # Use parent text if it's reasonable length
            if parent_text and 10 <= len(parent_text) <= 200:
                return parent_text
        
        return "PDF Document"
    
    def _generate_filename(self, url: str, title: str = "") -> str:
        """Generate a clean filename for the PDF."""
        # Start with URL filename
        parsed_url = urlparse(url)
        url_filename = os.path.basename(unquote(parsed_url.path))
        
        # If we have a good title, use it
        if title and len(title.strip()) > 3:
            # Clean title for filename
            clean_title = re.sub(r'[^\w\s-]', '', title.strip())
            clean_title = re.sub(r'\s+', '_', clean_title)
            clean_title = clean_title[:self.config['filename_max_length']]
            
            if clean_title:
                return f"{clean_title}.pdf"
        
        # Use URL filename if it's good
        if url_filename and url_filename.lower().endswith('.pdf'):
            return url_filename
        
        # Generate from URL path
        path_parts = [p for p in parsed_url.path.split('/') if p]
        if path_parts:
            clean_name = re.sub(r'[^\w\s-]', '', path_parts[-1])
            clean_name = re.sub(r'\s+', '_', clean_name)
            if clean_name:
                return f"{clean_name}.pdf"
        
        # Last resort: generate from URL hash
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        return f"document_{url_hash}.pdf"
    
    def download_pdf(self, pdf_info: Dict[str, str]) -> Optional[Path]:
        """
        Download a single PDF file.
        
        Args:
            pdf_info: Dictionary containing PDF information
            
        Returns:
            Path to downloaded file or None if failed
        """
        url = pdf_info['url']
        filename = pdf_info['filename']
        
        # Create subdirectory if configured
        if self.config['create_subdirs']:
            domain = urlparse(url).netloc
            safe_domain = re.sub(r'[^\w\-_.]', '_', domain)
            subdir = self.download_dir / safe_domain
            subdir.mkdir(exist_ok=True)
            filepath = subdir / filename
        else:
            filepath = self.download_dir / filename
        
        # Check if file already exists
        if filepath.exists():
            self.logger.info(f"File already exists: {filename}")
            return filepath
        
        # Download with retries
        for attempt in range(self.config['max_retries']):
            try:
                self.logger.info(f"Downloading: {filename} (attempt {attempt + 1})")
                
                response = self.session.get(
                    url, 
                    timeout=self.config['download_timeout'],
                    stream=True
                )
                response.raise_for_status()
                
                # Verify content type if configured
                if self.config['verify_pdf_content']:
                    content_type = response.headers.get('content-type', '').lower()
                    if 'pdf' not in content_type and not url.lower().endswith('.pdf'):
                        # Check first few bytes for PDF signature
                        chunk = next(response.iter_content(chunk_size=8), b'')
                        if not chunk.startswith(b'%PDF'):
                            self.logger.warning(f"File may not be a PDF: {filename}")
                
                # Download the file
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                file_size = filepath.stat().st_size
                self.logger.info(f"Downloaded: {filename} ({file_size} bytes)")
                
                # Delay before next download
                if self.config['delay_between_downloads'] > 0:
                    time.sleep(self.config['delay_between_downloads'])
                
                return filepath
                
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Download error for {filename} (attempt {attempt + 1}): {e}")
                if attempt == self.config['max_retries'] - 1:
                    self.logger.error(f"Failed to download {filename} after {self.config['max_retries']} attempts")
                else:
                    time.sleep(2 ** attempt)  # Exponential backoff
            except Exception as e:
                self.logger.error(f"Unexpected error downloading {filename}: {e}")
                break
        
        return None
    
    def download_all_pdfs(self, urls: Optional[List[str]] = None) -> Dict[str, any]:
        """
        Discover and download all PDFs from the configured website(s).
        
        Args:
            urls: Optional list of URLs to scan (defaults to base_url)
            
        Returns:
            Summary of download results
        """
        summary = {
            'start_time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'urls_scanned': [],
            'pdfs_found': 0,
            'pdfs_downloaded': 0,
            'successful_downloads': [],
            'failed_downloads': [],
            'errors': []
        }
        
        target_urls = urls or [self.base_url]
        
        try:
            # Discover PDFs from all target URLs
            all_pdf_links = []
            for url in target_urls:
                summary['urls_scanned'].append(url)
                pdf_links = self.discover_pdf_links(url)
                all_pdf_links.extend(pdf_links)
            
            # Remove duplicates based on URL
            unique_pdfs = []
            seen_urls = set()
            for pdf in all_pdf_links:
                if pdf['url'] not in seen_urls:
                    unique_pdfs.append(pdf)
                    seen_urls.add(pdf['url'])
            
            summary['pdfs_found'] = len(unique_pdfs)
            
            # Download each PDF
            for pdf_info in unique_pdfs:
                try:
                    filepath = self.download_pdf(pdf_info)
                    if filepath:
                        summary['pdfs_downloaded'] += 1
                        summary['successful_downloads'].append({
                            'filename': pdf_info['filename'],
                            'url': pdf_info['url'],
                            'filepath': str(filepath)
                        })
                    else:
                        summary['failed_downloads'].append(pdf_info)
                        
                except Exception as e:
                    error_msg = f"Error downloading {pdf_info['filename']}: {e}"
                    self.logger.error(error_msg)
                    summary['errors'].append(error_msg)
                    summary['failed_downloads'].append(pdf_info)
            
            summary['end_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
            
            # Save summary
            summary_path = self.download_dir / 'download_summary.json'
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Download completed. Summary saved to: {summary_path}")
            return summary
            
        except Exception as e:
            error_msg = f"Critical error in download process: {e}"
            self.logger.error(error_msg)
            summary['errors'].append(error_msg)
            summary['end_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
            return summary


def load_config_from_file(config_path: str) -> Dict:
    """Load configuration from JSON file."""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Configuration file not found: {config_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error parsing configuration file: {e}")
        return {}


def main():
    """Main function to run the PDF downloader."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Download PDF documents from any website')
    parser.add_argument('url', help='Website URL to download PDFs from')
    parser.add_argument('--output-dir', '-o', default='downloaded_pdfs', 
                       help='Output directory for downloaded PDFs')
    parser.add_argument('--config', '-c', help='Configuration file path')
    parser.add_argument('--delay', '-d', type=float, default=1.0,
                       help='Delay between downloads in seconds')
    parser.add_argument('--timeout', '-t', type=int, default=30,
                       help='Request timeout in seconds')
    parser.add_argument('--max-retries', '-r', type=int, default=3,
                       help='Maximum retry attempts for failed downloads')
    parser.add_argument('--no-verify', action='store_true',
                       help='Skip PDF content verification')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Setup logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Load configuration
    config = {}
    if args.config:
        config = load_config_from_file(args.config)
    
    # Override config with command line arguments
    config.update({
        'delay_between_downloads': args.delay,
        'request_timeout': args.timeout,
        'max_retries': args.max_retries,
        'verify_pdf_content': not args.no_verify
    })
    
    # Initialize downloader
    downloader = PDFDownloader(
        base_url=args.url,
        download_dir=args.output_dir,
        config=config
    )
    
    print("Generic PDF Downloader")
    print("=" * 50)
    print(f"Target URL: {args.url}")
    print(f"Output directory: {args.output_dir}")
    print(f"Configuration: {len(config)} settings applied")
    print()
    
    # Run download process
    summary = downloader.download_all_pdfs()
    
    # Print results
    print("\nDownload Summary:")
    print(f"URLs scanned: {len(summary['urls_scanned'])}")
    print(f"PDFs found: {summary['pdfs_found']}")
    print(f"PDFs downloaded: {summary['pdfs_downloaded']}")
    print(f"Successful downloads: {len(summary['successful_downloads'])}")
    print(f"Failed downloads: {len(summary['failed_downloads'])}")
    
    if summary['errors']:
        print(f"\nErrors encountered: {len(summary['errors'])}")
        for error in summary['errors'][:5]:  # Show first 5 errors
            print(f"  - {error}")
    
    if summary['successful_downloads']:
        print(f"\nDownloaded files:")
        for download in summary['successful_downloads'][:10]:  # Show first 10
            print(f"  - {download['filename']}")
    
    print(f"\nResults saved in: {args.output_dir}")


if __name__ == "__main__":
    main()
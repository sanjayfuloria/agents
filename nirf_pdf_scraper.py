#!/usr/bin/env python3
"""
NIRF Engineering Rankings PDF Scraper

This script downloads PDF documents from the NIRF India Engineering Rankings website
and extracts data from them for analysis.

Author: AI Agent
Date: 2025
"""

import os
import json
import time
import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path
import pypdf
from typing import List, Dict, Optional
import re


class NIRFPDFScraper:
    """
    A class to scrape PDF documents from NIRF Engineering Rankings website
    and extract data from them.
    """
    
    def __init__(self, base_url: str = "https://www.nirfindia.org/Rankings/2024/EngineeringRanking.html", 
                 download_dir: str = "nirf_pdfs", 
                 data_dir: str = "nirf_data"):
        """
        Initialize the scraper.
        
        Args:
            base_url: The URL to scrape PDFs from
            download_dir: Directory to save downloaded PDFs
            data_dir: Directory to save extracted data
        """
        self.base_url = base_url
        self.download_dir = Path(download_dir)
        self.data_dir = Path(data_dir)
        self.session = requests.Session()
        
        # Create directories if they don't exist
        self.download_dir.mkdir(exist_ok=True)
        self.data_dir.mkdir(exist_ok=True)
        
        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # User agent to avoid blocking
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_pdf_links(self) -> List[Dict[str, str]]:
        """
        Extract PDF links from the NIRF rankings page.
        
        Returns:
            List of dictionaries containing PDF URLs and college names
        """
        try:
            self.logger.info(f"Fetching PDF links from {self.base_url}")
            response = self.session.get(self.base_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            pdf_links = []
            
            # Find all links that point to PDF files
            # This is a generic approach that should work for most ranking websites
            all_links = soup.find_all('a', href=True)
            
            for link in all_links:
                href = link.get('href', '')
                if href.lower().endswith('.pdf'):
                    # Get the full URL
                    full_url = urljoin(self.base_url, href)
                    
                    # Try to extract college name from link text or nearby text
                    college_name = self._extract_college_name(link, soup)
                    
                    pdf_links.append({
                        'url': full_url,
                        'college_name': college_name,
                        'filename': self._generate_filename(college_name, href)
                    })
            
            # Alternative approach: Look for specific patterns in NIRF website
            # Find table rows or div elements that contain ranking information
            ranking_rows = soup.find_all(['tr', 'div'], class_=re.compile(r'rank|college|institution', re.I))
            
            for row in ranking_rows:
                pdf_link = row.find('a', href=lambda x: x and x.lower().endswith('.pdf'))
                if pdf_link:
                    href = pdf_link.get('href', '')
                    full_url = urljoin(self.base_url, href)
                    college_name = self._extract_college_name_from_row(row)
                    
                    pdf_info = {
                        'url': full_url,
                        'college_name': college_name,
                        'filename': self._generate_filename(college_name, href)
                    }
                    
                    # Avoid duplicates
                    if pdf_info not in pdf_links:
                        pdf_links.append(pdf_info)
            
            self.logger.info(f"Found {len(pdf_links)} PDF links")
            return pdf_links
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching PDF links: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return []
    
    def _extract_college_name(self, link, soup) -> str:
        """Extract college name from link or surrounding context."""
        # Try to get text from the link itself
        link_text = link.get_text(strip=True)
        if link_text and not link_text.lower() in ['pdf', 'download', 'view']:
            return self._clean_college_name(link_text)
        
        # Look for text in parent elements
        parent = link.parent
        if parent:
            parent_text = parent.get_text(strip=True)
            if parent_text and len(parent_text) < 200:  # Reasonable length
                return self._clean_college_name(parent_text)
        
        # Look for nearby text elements
        prev_sibling = link.find_previous_sibling()
        if prev_sibling:
            prev_text = prev_sibling.get_text(strip=True)
            if prev_text and len(prev_text) < 200:
                return self._clean_college_name(prev_text)
        
        # Default fallback
        href = link.get('href', '')
        filename = os.path.basename(href)
        return self._clean_college_name(filename.replace('.pdf', ''))
    
    def _extract_college_name_from_row(self, row) -> str:
        """Extract college name from a table row or div element."""
        # Look for common patterns in NIRF rankings
        text_elements = row.find_all(['td', 'div', 'span'], string=True)
        
        for element in text_elements:
            text = element.get_text(strip=True)
            # Skip if it's just numbers, ranking info, or too short
            if text and len(text) > 10 and not text.isdigit() and 'rank' not in text.lower():
                return self._clean_college_name(text)
        
        # Fallback to entire row text
        row_text = row.get_text(strip=True)
        return self._clean_college_name(row_text[:100])  # Limit length
    
    def _clean_college_name(self, name: str) -> str:
        """Clean and standardize college name."""
        # Remove extra whitespace and special characters
        name = re.sub(r'\s+', ' ', name.strip())
        name = re.sub(r'[^\w\s-]', '', name)
        return name[:100]  # Limit length
    
    def _generate_filename(self, college_name: str, original_href: str) -> str:
        """Generate a clean filename for the PDF."""
        # Use college name if available, otherwise use original filename
        if college_name and college_name.strip():
            # Clean the name for filename use
            clean_name = re.sub(r'[^\w\s-]', '', college_name)
            clean_name = re.sub(r'\s+', '_', clean_name.strip())
            return f"{clean_name}.pdf"
        else:
            # Use original filename
            return os.path.basename(original_href)
    
    def download_pdf(self, pdf_info: Dict[str, str]) -> Optional[Path]:
        """
        Download a single PDF file.
        
        Args:
            pdf_info: Dictionary containing PDF URL, college name, and filename
            
        Returns:
            Path to downloaded file or None if failed
        """
        try:
            url = pdf_info['url']
            filename = pdf_info['filename']
            filepath = self.download_dir / filename
            
            # Skip if file already exists
            if filepath.exists():
                self.logger.info(f"File already exists: {filename}")
                return filepath
            
            self.logger.info(f"Downloading: {filename}")
            response = self.session.get(url, timeout=60, stream=True)
            response.raise_for_status()
            
            # Check if it's actually a PDF
            content_type = response.headers.get('content-type', '').lower()
            if 'pdf' not in content_type and not url.lower().endswith('.pdf'):
                self.logger.warning(f"File might not be a PDF: {filename}")
            
            # Download with progress
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            self.logger.info(f"Downloaded: {filename} ({filepath.stat().st_size} bytes)")
            return filepath
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error downloading {pdf_info['filename']}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error downloading {pdf_info['filename']}: {e}")
            return None
    
    def extract_text_from_pdf(self, pdf_path: Path) -> Dict[str, any]:
        """
        Extract text and metadata from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing extracted text and metadata
        """
        try:
            self.logger.info(f"Extracting text from: {pdf_path.name}")
            
            with open(pdf_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                
                # Extract metadata
                metadata = {
                    'filename': pdf_path.name,
                    'num_pages': len(pdf_reader.pages),
                    'file_size': pdf_path.stat().st_size,
                    'extracted_at': time.strftime('%Y-%m-%d %H:%M:%S')
                }
                
                # Try to get PDF metadata
                if pdf_reader.metadata:
                    metadata.update({
                        'title': str(pdf_reader.metadata.get('/Title', '')),
                        'author': str(pdf_reader.metadata.get('/Author', '')),
                        'subject': str(pdf_reader.metadata.get('/Subject', '')),
                        'creator': str(pdf_reader.metadata.get('/Creator', ''))
                    })
                
                # Extract text from all pages
                full_text = ""
                page_texts = []
                
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        page_texts.append({
                            'page_number': page_num + 1,
                            'text': page_text,
                            'char_count': len(page_text)
                        })
                        full_text += page_text + "\n"
                    except Exception as e:
                        self.logger.warning(f"Error extracting text from page {page_num + 1}: {e}")
                        page_texts.append({
                            'page_number': page_num + 1,
                            'text': '',
                            'char_count': 0,
                            'error': str(e)
                        })
                
                # Extract structured data (college information)
                structured_data = self._extract_structured_data(full_text)
                
                return {
                    'metadata': metadata,
                    'full_text': full_text,
                    'pages': page_texts,
                    'structured_data': structured_data,
                    'word_count': len(full_text.split()),
                    'char_count': len(full_text)
                }
                
        except Exception as e:
            self.logger.error(f"Error extracting text from {pdf_path}: {e}")
            return {
                'metadata': {'filename': pdf_path.name, 'error': str(e)},
                'full_text': '',
                'pages': [],
                'structured_data': {},
                'word_count': 0,
                'char_count': 0
            }
    
    def _extract_structured_data(self, text: str) -> Dict[str, any]:
        """
        Extract structured information from PDF text.
        
        Args:
            text: Full text extracted from PDF
            
        Returns:
            Dictionary containing structured data
        """
        structured = {}
        
        # Extract college name
        college_patterns = [
            r'College[:\s]+([^\n]+)',
            r'Institute[:\s]+([^\n]+)',
            r'University[:\s]+([^\n]+)',
            r'Name[:\s]+([^\n]+)'
        ]
        
        for pattern in college_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                structured['college_name'] = match.group(1).strip()
                break
        
        # Extract location/address
        location_patterns = [
            r'Address[:\s]+([^\n]+)',
            r'Location[:\s]+([^\n]+)',
            r'City[:\s]+([^\n]+)',
            r'State[:\s]+([^\n]+)'
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                structured['location'] = match.group(1).strip()
                break
        
        # Extract ranking information
        ranking_patterns = [
            r'Rank[:\s]+(\d+)',
            r'Position[:\s]+(\d+)',
            r'#(\d+)'
        ]
        
        for pattern in ranking_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                structured['rank'] = int(match.group(1))
                break
        
        # Extract scores/ratings
        score_patterns = [
            r'Score[:\s]+([\d.]+)',
            r'Rating[:\s]+([\d.]+)',
            r'Points[:\s]+([\d.]+)'
        ]
        
        scores = []
        for pattern in score_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            scores.extend([float(score) for score in matches])
        
        if scores:
            structured['scores'] = scores
            structured['average_score'] = sum(scores) / len(scores)
        
        # Extract other numerical data
        numbers = re.findall(r'\d+\.?\d*', text)
        if numbers:
            structured['all_numbers'] = [float(num) for num in numbers[:20]]  # Limit to first 20
        
        return structured
    
    def save_extracted_data(self, pdf_info: Dict[str, str], extracted_data: Dict[str, any]) -> None:
        """
        Save extracted data to JSON file.
        
        Args:
            pdf_info: Original PDF information
            extracted_data: Extracted text and metadata
        """
        try:
            # Create filename based on college name or PDF filename
            college_name = extracted_data.get('structured_data', {}).get('college_name', 
                                                                       pdf_info.get('college_name', 'unknown'))
            safe_name = re.sub(r'[^\w\s-]', '', college_name)
            safe_name = re.sub(r'\s+', '_', safe_name.strip())
            
            json_filename = f"{safe_name}_data.json"
            json_path = self.data_dir / json_filename
            
            # Combine PDF info with extracted data
            combined_data = {
                'pdf_info': pdf_info,
                'extracted_data': extracted_data,
                'processed_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(combined_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Saved extracted data to: {json_filename}")
            
        except Exception as e:
            self.logger.error(f"Error saving extracted data: {e}")
    
    def scrape_and_download_all(self) -> Dict[str, any]:
        """
        Complete workflow: scrape website, download PDFs, and extract data.
        
        Returns:
            Summary of the scraping process
        """
        summary = {
            'start_time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'pdf_links_found': 0,
            'pdfs_downloaded': 0,
            'pdfs_processed': 0,
            'errors': [],
            'successful_files': [],
            'failed_files': []
        }
        
        try:
            # Step 1: Get PDF links
            pdf_links = self.get_pdf_links()
            summary['pdf_links_found'] = len(pdf_links)
            
            if not pdf_links:
                self.logger.warning("No PDF links found on the website")
                return summary
            
            # Step 2: Download and process each PDF
            for pdf_info in pdf_links:
                try:
                    # Download PDF
                    pdf_path = self.download_pdf(pdf_info)
                    if pdf_path:
                        summary['pdfs_downloaded'] += 1
                        
                        # Extract data from PDF
                        extracted_data = self.extract_text_from_pdf(pdf_path)
                        
                        # Save extracted data
                        self.save_extracted_data(pdf_info, extracted_data)
                        summary['pdfs_processed'] += 1
                        summary['successful_files'].append(pdf_info['filename'])
                        
                        # Small delay to be respectful to the server
                        time.sleep(1)
                    else:
                        summary['failed_files'].append(pdf_info['filename'])
                        
                except Exception as e:
                    error_msg = f"Error processing {pdf_info['filename']}: {e}"
                    self.logger.error(error_msg)
                    summary['errors'].append(error_msg)
                    summary['failed_files'].append(pdf_info['filename'])
            
            summary['end_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
            
            # Save summary
            summary_path = self.data_dir / 'scraping_summary.json'
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Scraping completed. Summary saved to: {summary_path}")
            return summary
            
        except Exception as e:
            error_msg = f"Critical error in scraping process: {e}"
            self.logger.error(error_msg)
            summary['errors'].append(error_msg)
            summary['end_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
            return summary


def main():
    """Main function to run the scraper."""
    scraper = NIRFPDFScraper()
    
    print("NIRF Engineering Rankings PDF Scraper")
    print("=====================================")
    print(f"Target URL: {scraper.base_url}")
    print(f"Download directory: {scraper.download_dir}")
    print(f"Data directory: {scraper.data_dir}")
    print()
    
    # Run the complete scraping process
    summary = scraper.scrape_and_download_all()
    
    # Print summary
    print("\nScraping Summary:")
    print(f"PDF links found: {summary['pdf_links_found']}")
    print(f"PDFs downloaded: {summary['pdfs_downloaded']}")
    print(f"PDFs processed: {summary['pdfs_processed']}")
    print(f"Successful files: {len(summary['successful_files'])}")
    print(f"Failed files: {len(summary['failed_files'])}")
    
    if summary['errors']:
        print(f"\nErrors encountered: {len(summary['errors'])}")
        for error in summary['errors'][:5]:  # Show first 5 errors
            print(f"  - {error}")
    
    print(f"\nResults saved in: {scraper.data_dir}")


if __name__ == "__main__":
    main()
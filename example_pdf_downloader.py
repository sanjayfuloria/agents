#!/usr/bin/env python3
"""
Example usage of the Generic PDF Downloader

This script demonstrates different ways to use the PDF downloader
for various common scenarios.
"""

import os
from pdf_downloader import PDFDownloader


def example_basic_usage():
    """Basic example - download PDFs from a single website."""
    print("Example 1: Basic Usage")
    print("-" * 30)
    
    # Simple usage with defaults
    downloader = PDFDownloader(
        base_url="https://example.com/documents",
        download_dir="example_downloads"
    )
    
    # This would download all PDFs found on the page
    # summary = downloader.download_all_pdfs()
    print("Created downloader for: https://example.com/documents")
    print("Output directory: example_downloads/")
    print()


def example_with_configuration():
    """Example using custom configuration."""
    print("Example 2: Custom Configuration")
    print("-" * 35)
    
    # Custom configuration for more control
    config = {
        'delay_between_downloads': 2.0,  # 2 seconds between downloads
        'max_retries': 5,                # Try 5 times if download fails
        'request_timeout': 60,           # 60 second timeout for requests
        'create_subdirs': True,          # Create subdirectories by domain
        'verify_pdf_content': True,      # Verify files are actual PDFs
        'filename_max_length': 80        # Shorter filenames
    }
    
    downloader = PDFDownloader(
        base_url="https://research.university.edu/papers",
        download_dir="research_papers",
        config=config
    )
    
    print("Configured for research paper downloads:")
    print(f"- 2 second delays between downloads")
    print(f"- 5 retry attempts")
    print(f"- 60 second timeouts")
    print(f"- Organized in subdirectories")
    print()


def example_multiple_sites():
    """Example downloading from multiple websites."""
    print("Example 3: Multiple Sites")
    print("-" * 28)
    
    # List of sites to download from
    academic_sites = [
        "https://university1.edu/cs/papers",
        "https://university2.edu/research/publications",
        "https://conference2024.org/proceedings"
    ]
    
    # Configuration optimized for academic sites
    academic_config = {
        'delay_between_downloads': 3.0,  # Be respectful to academic servers
        'pdf_patterns': [
            r'.*\.pdf$',
            r'.*paper.*\.pdf',
            r'.*proceedings.*\.pdf',
            r'.*thesis.*\.pdf'
        ],
        'exclude_patterns': [
            r'.*admin.*',
            r'.*login.*',
            r'.*private.*'
        ]
    }
    
    for site in academic_sites:
        # Create domain-specific output directory
        domain = site.split('//')[1].split('/')[0]
        output_dir = f"academic_papers/{domain}"
        
        downloader = PDFDownloader(
            base_url=site,
            download_dir=output_dir,
            config=academic_config
        )
        
        print(f"Would download from: {site}")
        print(f"Output directory: {output_dir}")
    print()


def example_government_documents():
    """Example for downloading government documents."""
    print("Example 4: Government Documents")
    print("-" * 34)
    
    # Configuration for government sites
    gov_config = {
        'delay_between_downloads': 1.5,
        'pdf_patterns': [
            r'.*\.pdf$',
            r'.*report.*\.pdf',
            r'.*document.*\.pdf',
            r'.*policy.*\.pdf'
        ],
        'link_selectors': [
            'a[href$=".pdf"]',
            'a[href*="document"]',
            'a[href*="report"]',
            'a.download-link'
        ],
        'user_agent': 'Mozilla/5.0 (compatible; PDFDownloader/1.0; +http://example.com/bot)',
        'create_subdirs': True
    }
    
    downloader = PDFDownloader(
        base_url="https://government.example/documents",
        download_dir="government_docs",
        config=gov_config
    )
    
    print("Configured for government document downloads:")
    print("- Specialized PDF patterns for reports and policies")
    print("- Custom CSS selectors for government sites")
    print("- Respectful crawling with delays")
    print()


def example_with_file_config():
    """Example using configuration file."""
    print("Example 5: Configuration File")
    print("-" * 31)
    
    # Using the provided configuration file
    config_file = "pdf_downloader_config.json"
    
    if os.path.exists(config_file):
        from pdf_downloader import load_config_from_file
        
        config = load_config_from_file(config_file)
        
        downloader = PDFDownloader(
            base_url="https://docs.example.com",
            download_dir="doc_downloads",
            config=config
        )
        
        print(f"Loaded configuration from: {config_file}")
        print(f"Settings loaded: {len(config)} configuration options")
    else:
        print(f"Configuration file not found: {config_file}")
        print("You can create one based on the example in the repository")
    print()


def main():
    """Run all examples."""
    print("Generic PDF Downloader - Usage Examples")
    print("=" * 50)
    print()
    
    example_basic_usage()
    example_with_configuration()
    example_multiple_sites()
    example_government_documents()
    example_with_file_config()
    
    print("Command Line Usage Examples:")
    print("-" * 30)
    print("# Basic download")
    print("python pdf_downloader.py https://example.com/docs")
    print()
    print("# With options")
    print("python pdf_downloader.py https://site.com \\")
    print("    --output-dir my_pdfs/ \\")
    print("    --delay 2 \\")
    print("    --max-retries 5 \\")
    print("    --verbose")
    print()
    print("# Using configuration file")
    print("python pdf_downloader.py https://docs.site.com \\")
    print("    --config pdf_downloader_config.json")
    print()
    print("See README_PDF_DOWNLOADER.md for complete documentation!")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Test script for Generic PDF Downloader

This script tests the functionality of the generic PDF downloader with mock data.
"""

import os
import sys
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
import requests

# Add current directory to path to import our modules
sys.path.insert(0, '.')

try:
    from pdf_downloader import PDFDownloader, load_config_from_file
    print("✓ Successfully imported Generic PDF Downloader")
except ImportError as e:
    print(f"Error importing PDF downloader: {e}")
    sys.exit(1)


def create_test_html_simple():
    """Create a simple HTML page with PDF links for testing."""
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Test Page with PDFs</title></head>
    <body>
        <h1>Documents</h1>
        <ul>
            <li><a href="document1.pdf">Important Document 1</a></li>
            <li><a href="files/document2.pdf">Research Paper</a></li>
            <li><a href="http://example.com/external.pdf">External PDF</a></li>
            <li><a href="report.PDF">Annual Report</a> (uppercase extension)</li>
            <li><a href="not-a-pdf.doc">Word Document</a> (should be ignored)</li>
        </ul>
        
        <div>
            <h2>Embedded PDFs</h2>
            <object data="embedded.pdf" type="application/pdf">PDF Object</object>
            <iframe src="viewer.pdf"></iframe>
        </div>
        
        <p>Some text with a <a href="inline.pdf">PDF link</a> in the middle.</p>
    </body>
    </html>
    """


def create_test_html_complex():
    """Create a more complex HTML page for testing."""
    return """
    <!DOCTYPE html>
    <html>
    <head><title>University Research Papers</title></head>
    <body>
        <div class="header">
            <h1>Research Publications</h1>
        </div>
        
        <table class="papers">
            <tr>
                <th>Title</th>
                <th>Authors</th>
                <th>Download</th>
            </tr>
            <tr>
                <td>Machine Learning in Education</td>
                <td>Dr. Smith, Prof. Johnson</td>
                <td><a href="papers/ml_education_2024.pdf" title="ML Education Paper">Download PDF</a></td>
            </tr>
            <tr>
                <td>Artificial Intelligence Ethics</td>
                <td>Dr. Brown</td>
                <td><a href="papers/ai_ethics.pdf">PDF</a></td>
            </tr>
        </table>
        
        <div class="archived">
            <h3>Archived Papers</h3>
            <a href="archive/2023/old_paper.pdf">Old Research</a>
            <a href="conference_proceedings.pdf">Conference Proceedings</a>
        </div>
    </body>
    </html>
    """


def create_mock_pdf_content():
    """Create mock PDF content for testing."""
    return b'%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\nMock PDF content for testing'


def test_basic_functionality():
    """Test basic functionality of the PDF downloader."""
    print("Testing Generic PDF Downloader basic functionality...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        download_dir = os.path.join(temp_dir, "test_downloads")
        
        # Test with minimal configuration
        downloader = PDFDownloader(
            base_url="http://example.com/test",
            download_dir=download_dir
        )
        
        # Test directory creation
        assert downloader.download_dir.exists(), "Download directory should be created"
        print("✓ Directory creation works")
        
        # Test filename generation
        test_cases = [
            ("http://example.com/document.pdf", "Research Paper", "Research_Paper.pdf"),
            ("http://example.com/file.pdf", "", "file.pdf"),
            ("http://example.com/path/to/report.pdf", "Annual Report 2024", "Annual_Report_2024.pdf"),
            ("http://example.com/complex/path", "Test Document", "Test_Document.pdf")
        ]
        
        for url, title, expected_pattern in test_cases:
            filename = downloader._generate_filename(url, title)
            assert filename.endswith('.pdf'), f"Generated filename should end with .pdf: {filename}"
            assert len(filename) <= 104, f"Filename should not be too long: {filename}"  # 100 + .pdf
        
        print("✓ Filename generation works")
        
        # Test PDF pattern matching
        pdf_urls = [
            "http://example.com/doc.pdf",
            "http://example.com/doc.PDF",
            "http://example.com/file.pdf?download=1"
        ]
        
        non_pdf_urls = [
            "http://example.com/doc.doc",
            "http://example.com/image.jpg",
            "javascript:void(0)"
        ]
        
        for url in pdf_urls:
            assert downloader._matches_pdf_pattern(url), f"Should match PDF pattern: {url}"
        
        for url in non_pdf_urls:
            assert not downloader._matches_pdf_pattern(url), f"Should not match PDF pattern: {url}"
        
        print("✓ PDF pattern matching works")
    
    print("Basic functionality tests passed!")


def test_html_parsing_simple():
    """Test HTML parsing with simple content."""
    print("\nTesting HTML parsing (simple)...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        downloader = PDFDownloader(
            base_url="http://example.com/test",
            download_dir=os.path.join(temp_dir, "downloads")
        )
        
        # Mock the requests.get method
        mock_response = Mock()
        mock_response.content = create_test_html_simple().encode('utf-8')
        mock_response.raise_for_status = Mock()
        
        with patch.object(downloader.session, 'get', return_value=mock_response):
            pdf_links = downloader.discover_pdf_links()
            
            assert len(pdf_links) >= 4, f"Should find at least 4 PDF links, found {len(pdf_links)}"
            
            # Check that each link has required fields
            for link in pdf_links:
                assert 'url' in link, "Each link should have URL"
                assert 'title' in link, "Each link should have title"
                assert 'filename' in link, "Each link should have filename"
                assert 'source_url' in link, "Each link should have source URL"
                assert link['filename'].endswith('.pdf'), f"Filename should end with .pdf: {link['filename']}"
            
            # Check for specific expected links
            urls = [link['url'] for link in pdf_links]
            assert any('document1.pdf' in url for url in urls), "Should find document1.pdf"
            assert any('document2.pdf' in url for url in urls), "Should find document2.pdf"
            
            print(f"✓ Found {len(pdf_links)} PDF links")
            for link in pdf_links[:3]:  # Show first 3
                print(f"  - {link['filename']}: {link['url']}")
    
    print("Simple HTML parsing tests passed!")


def test_html_parsing_complex():
    """Test HTML parsing with complex content."""
    print("\nTesting HTML parsing (complex)...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        downloader = PDFDownloader(
            base_url="http://university.edu/research",
            download_dir=os.path.join(temp_dir, "downloads")
        )
        
        # Mock the requests.get method
        mock_response = Mock()
        mock_response.content = create_test_html_complex().encode('utf-8')
        mock_response.raise_for_status = Mock()
        
        with patch.object(downloader.session, 'get', return_value=mock_response):
            pdf_links = downloader.discover_pdf_links()
            
            assert len(pdf_links) >= 3, f"Should find at least 3 PDF links, found {len(pdf_links)}"
            
            # Check for title extraction
            titles = [link['title'] for link in pdf_links]
            assert any('Machine Learning' in title or 'ML Education' in title for title in titles), \
                "Should extract meaningful titles"
            
            print(f"✓ Found {len(pdf_links)} PDF links with titles")
            for link in pdf_links:
                print(f"  - {link['title'][:50]}... -> {link['filename']}")
    
    print("Complex HTML parsing tests passed!")


def test_download_functionality():
    """Test PDF download functionality with mocking."""
    print("\nTesting download functionality...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        download_dir = os.path.join(temp_dir, "downloads")
        downloader = PDFDownloader(
            base_url="http://example.com",
            download_dir=download_dir
        )
        
        # Create test PDF info
        pdf_info = {
            'url': 'http://example.com/test.pdf',
            'title': 'Test Document',
            'filename': 'test_document.pdf',
            'source_url': 'http://example.com',
            'link_text': 'Download Test PDF'
        }
        
        # Mock successful download
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.headers = {'content-type': 'application/pdf'}
        mock_response.iter_content = Mock(return_value=[create_mock_pdf_content()])
        
        with patch.object(downloader.session, 'get', return_value=mock_response):
            filepath = downloader.download_pdf(pdf_info)
            
            assert filepath is not None, "Download should return a filepath"
            assert filepath.exists(), "Downloaded file should exist"
            assert filepath.name == 'test_document.pdf', "Filename should match expected"
            
            # Check file content
            with open(filepath, 'rb') as f:
                content = f.read()
                assert content.startswith(b'%PDF'), "File should start with PDF signature"
            
            print(f"✓ Successfully downloaded: {filepath.name}")
    
    print("Download functionality tests passed!")


def test_configuration_loading():
    """Test configuration file loading."""
    print("\nTesting configuration loading...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test config file
        config_data = {
            "delay_between_downloads": 2.5,
            "max_retries": 5,
            "custom_setting": "test_value"
        }
        
        config_path = os.path.join(temp_dir, "test_config.json")
        with open(config_path, 'w') as f:
            json.dump(config_data, f)
        
        # Test loading configuration
        loaded_config = load_config_from_file(config_path)
        
        assert loaded_config['delay_between_downloads'] == 2.5, "Should load delay setting"
        assert loaded_config['max_retries'] == 5, "Should load retry setting"
        assert loaded_config['custom_setting'] == "test_value", "Should load custom setting"
        
        # Test downloader with custom config
        downloader = PDFDownloader(
            base_url="http://example.com",
            download_dir=os.path.join(temp_dir, "downloads"),
            config=loaded_config
        )
        
        assert downloader.config['delay_between_downloads'] == 2.5, "Should apply custom delay"
        assert downloader.config['max_retries'] == 5, "Should apply custom retries"
        
        print("✓ Configuration loading works")
    
    print("Configuration tests passed!")


def test_integration():
    """Test full integration workflow."""
    print("\nTesting integration workflow...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        download_dir = os.path.join(temp_dir, "downloads")
        
        # Configure downloader
        config = {
            'delay_between_downloads': 0,  # Speed up tests
            'create_subdirs': True
        }
        
        downloader = PDFDownloader(
            base_url="http://testsite.com",
            download_dir=download_dir,
            config=config
        )
        
        # Mock discovery
        mock_discovery_response = Mock()
        mock_discovery_response.content = create_test_html_simple().encode('utf-8')
        mock_discovery_response.raise_for_status = Mock()
        
        # Mock downloads
        mock_download_response = Mock()
        mock_download_response.raise_for_status = Mock()
        mock_download_response.headers = {'content-type': 'application/pdf'}
        mock_download_response.iter_content = Mock(return_value=[create_mock_pdf_content()])
        
        with patch.object(downloader.session, 'get') as mock_get:
            # First call for discovery, subsequent calls for downloads
            mock_get.side_effect = [mock_discovery_response] + [mock_download_response] * 10
            
            # Run full workflow
            summary = downloader.download_all_pdfs()
            
            assert summary['pdfs_found'] > 0, "Should find PDF links"
            assert summary['pdfs_downloaded'] > 0, "Should download some PDFs"
            assert len(summary['successful_downloads']) > 0, "Should have successful downloads"
            
            # Check that files were actually created
            download_path = Path(download_dir)
            downloaded_files = list(download_path.rglob("*.pdf"))
            assert len(downloaded_files) > 0, "Should create PDF files"
            
            # Check summary file
            summary_file = download_path / 'download_summary.json'
            assert summary_file.exists(), "Should create summary file"
            
            print(f"✓ Found {summary['pdfs_found']} PDFs")
            print(f"✓ Downloaded {summary['pdfs_downloaded']} files")
            print(f"✓ Created {len(downloaded_files)} files on disk")
    
    print("Integration tests passed!")


def main():
    """Run all tests."""
    print("Running Generic PDF Downloader Tests")
    print("=" * 60)
    
    try:
        test_basic_functionality()
        test_html_parsing_simple()
        test_html_parsing_complex()
        test_download_functionality()
        test_configuration_loading()
        test_integration()
        
        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        print("The Generic PDF Downloader is ready to use.")
        print("\nUsage examples:")
        print("  python pdf_downloader.py https://example.com")
        print("  python pdf_downloader.py https://university.edu/papers --output-dir papers/")
        print("  python pdf_downloader.py https://site.com --config pdf_downloader_config.json")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
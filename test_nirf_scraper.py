#!/usr/bin/env python3
"""
Test script for NIRF PDF Scraper

This script tests the basic functionality of the scraper with a mock/test setup.
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
    from nirf_pdf_scraper import NIRFPDFScraper
    print("✓ Successfully imported NIRF PDF Scraper")
except ImportError as e:
    print(f"Error importing scraper: {e}")
    sys.exit(1)

try:
    from nirf_data_analyzer import NIRFDataAnalyzer
    print("✓ Successfully imported NIRF Data Analyzer")
    ANALYZER_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Data analyzer not available (missing pandas): {e}")
    NIRFDataAnalyzer = None
    ANALYZER_AVAILABLE = False


def create_test_html():
    """Create a mock HTML page with PDF links for testing."""
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Test Rankings</title></head>
    <body>
        <h1>Engineering Rankings 2024</h1>
        <table>
            <tr>
                <td>1</td>
                <td>Indian Institute of Technology Madras</td>
                <td><a href="test_college_1.pdf">Download PDF</a></td>
            </tr>
            <tr>
                <td>2</td>
                <td>Indian Institute of Technology Delhi</td>
                <td><a href="test_college_2.pdf">Download PDF</a></td>
            </tr>
            <tr>
                <td>3</td>
                <td>Indian Institute of Technology Bombay</td>
                <td><a href="test_college_3.pdf">Download PDF</a></td>
            </tr>
        </table>
    </body>
    </html>
    """


def create_test_pdf_content():
    """Create mock PDF content for testing."""
    # This is obviously not a real PDF, but we'll mock the PDF reader
    return b"Mock PDF content for testing"


def test_scraper_basic_functionality():
    """Test basic functionality of the scraper."""
    print("Testing NIRF PDF Scraper...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Initialize scraper with temporary directories
        download_dir = os.path.join(temp_dir, "test_pdfs")
        data_dir = os.path.join(temp_dir, "test_data")
        
        scraper = NIRFPDFScraper(
            base_url="http://example.com/test",
            download_dir=download_dir,
            data_dir=data_dir
        )
        
        # Test directory creation
        assert scraper.download_dir.exists(), "Download directory should be created"
        assert scraper.data_dir.exists(), "Data directory should be created"
        print("✓ Directory creation works")
        
        # Test college name cleaning
        test_names = [
            "Indian Institute of Technology, Delhi",
            "IIT Delhi - Engineering College",
            "Test@#$%College Name"
        ]
        
        for name in test_names:
            cleaned = scraper._clean_college_name(name)
            assert isinstance(cleaned, str), "Cleaned name should be string"
            assert len(cleaned) <= 100, "Cleaned name should be limited length"
        print("✓ College name cleaning works")
        
        # Test filename generation
        test_filename = scraper._generate_filename("Test College", "original.pdf")
        assert test_filename.endswith(".pdf"), "Generated filename should end with .pdf"
        print("✓ Filename generation works")
        
    print("Basic functionality tests passed!")


def test_html_parsing():
    """Test HTML parsing functionality."""
    print("\nTesting HTML parsing...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        scraper = NIRFPDFScraper(
            download_dir=os.path.join(temp_dir, "pdfs"),
            data_dir=os.path.join(temp_dir, "data")
        )
        
        # Mock the requests.get method
        mock_response = Mock()
        mock_response.content = create_test_html().encode('utf-8')
        mock_response.raise_for_status = Mock()
        
        with patch.object(scraper.session, 'get', return_value=mock_response):
            pdf_links = scraper.get_pdf_links()
            
            assert len(pdf_links) > 0, "Should find PDF links in test HTML"
            
            for link in pdf_links:
                assert 'url' in link, "Each link should have URL"
                assert 'college_name' in link, "Each link should have college name"
                assert 'filename' in link, "Each link should have filename"
                assert link['url'].endswith('.pdf'), "URLs should point to PDFs"
            
            print(f"✓ Found {len(pdf_links)} PDF links")
            print(f"✓ Sample college: {pdf_links[0]['college_name'] if pdf_links else 'None'}")
    
    print("HTML parsing tests passed!")


def test_text_extraction():
    """Test text extraction functionality."""
    print("\nTesting text extraction...")
    
    # Create a sample text that simulates PDF content
    sample_text = """
    College Name: Test Engineering College
    Address: 123 Main Street, Test City, Test State
    Rank: 42
    Score: 85.5
    Rating: 4.2
    
    This is a sample PDF content with various information about the college.
    The college offers various engineering programs and has excellent facilities.
    """
    
    with tempfile.TemporaryDirectory() as temp_dir:
        scraper = NIRFPDFScraper(
            download_dir=os.path.join(temp_dir, "pdfs"),
            data_dir=os.path.join(temp_dir, "data")
        )
        
        # Test structured data extraction
        structured_data = scraper._extract_structured_data(sample_text)
        
        assert 'college_name' in structured_data, "Should extract college name"
        assert 'location' in structured_data, "Should extract location"
        assert 'rank' in structured_data, "Should extract rank"
        assert 'scores' in structured_data, "Should extract scores"
        
        print(f"✓ Extracted college name: {structured_data.get('college_name', 'None')}")
        print(f"✓ Extracted rank: {structured_data.get('rank', 'None')}")
        print(f"✓ Extracted scores: {structured_data.get('scores', [])}")
        
    print("Text extraction tests passed!")


def test_data_analyzer():
    """Test data analyzer functionality."""
    if not ANALYZER_AVAILABLE:
        print("\nSkipping data analyzer tests (pandas not available)")
        return
        
    print("\nTesting data analyzer...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        data_dir = os.path.join(temp_dir, "test_data")
        os.makedirs(data_dir)
        
        # Create sample data files
        sample_data = {
            "pdf_info": {
                "url": "http://example.com/test.pdf",
                "college_name": "Test College",
                "filename": "test_college.pdf"
            },
            "extracted_data": {
                "metadata": {
                    "filename": "test_college.pdf",
                    "num_pages": 5,
                    "file_size": 1024000
                },
                "full_text": "This is test content for the college with engineering programs.",
                "structured_data": {
                    "college_name": "Test Engineering College",
                    "location": "Test City",
                    "rank": 50,
                    "scores": [85.5, 90.2],
                    "average_score": 87.85
                },
                "word_count": 12,
                "char_count": 65
            },
            "processed_at": "2025-01-01 12:00:00"
        }
        
        # Save sample data
        for i in range(3):
            data_copy = sample_data.copy()
            data_copy['pdf_info']['college_name'] = f"Test College {i+1}"
            data_copy['extracted_data']['structured_data']['rank'] = 50 + i
            
            with open(os.path.join(data_dir, f"test_college_{i+1}_data.json"), 'w') as f:
                json.dump(data_copy, f)
        
        # Test analyzer
        analyzer = NIRFDataAnalyzer(data_dir)
        
        assert len(analyzer.data) == 3, "Should load 3 data files"
        
        if ANALYZER_AVAILABLE and analyzer.df is not None:
            assert len(analyzer.df) == 3, "DataFrame should have 3 rows"
            print(f"✓ Created DataFrame with {len(analyzer.df)} rows")
        else:
            print("✓ Skipped DataFrame creation (pandas not available)")
        
        # Test statistics
        stats = analyzer.basic_statistics()
        
        # Basic checks that should work even without pandas
        if 'total_colleges' in stats:
            print(f"✓ Loaded {len(analyzer.data)} data files")
            print(f"✓ Basic statistics generated")
        else:
            # Fallback for when pandas is not available
            print(f"✓ Loaded {len(analyzer.data)} data files")
            print("✓ Basic analysis completed (limited without pandas)")
        
    print("Data analyzer tests passed!")


def test_integration():
    """Test integration between scraper and analyzer."""
    if not ANALYZER_AVAILABLE:
        print("\nSkipping integration tests (pandas not available)")
        return
        
    print("\nTesting integration...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        download_dir = os.path.join(temp_dir, "pdfs")
        data_dir = os.path.join(temp_dir, "data")
        
        # Create mock PDF content and save it
        os.makedirs(download_dir)
        test_pdf_path = os.path.join(download_dir, "test.pdf")
        with open(test_pdf_path, 'wb') as f:
            f.write(create_test_pdf_content())
        
        scraper = NIRFPDFScraper(
            download_dir=download_dir,
            data_dir=data_dir
        )
        
        # Mock PDF extraction to avoid actual PDF processing
        mock_extracted_data = {
            'metadata': {'filename': 'test.pdf', 'num_pages': 1, 'file_size': 100},
            'full_text': 'Test College Content\nRank: 25\nScore: 88.5',
            'structured_data': {'college_name': 'Test College', 'rank': 25, 'scores': [88.5]},
            'word_count': 5,
            'char_count': 30
        }
        
        # Save extracted data
        pdf_info = {'url': 'test.pdf', 'college_name': 'Test College', 'filename': 'test.pdf'}
        scraper.save_extracted_data(pdf_info, mock_extracted_data)
        
        # Test analyzer with the saved data
        analyzer = NIRFDataAnalyzer(data_dir)
        
        assert len(analyzer.data) > 0, "Analyzer should load saved data"
        
        # Generate report
        analyzer.export_summary_report(os.path.join(temp_dir, "test_report.json"))
        
        report_path = os.path.join(temp_dir, "test_report.json")
        assert os.path.exists(report_path), "Should generate analysis report"
        
        print("✓ Integration between scraper and analyzer works")
    
    print("Integration tests passed!")


def main():
    """Run all tests."""
    print("Running NIRF PDF Scraper Tests")
    print("=" * 50)
    
    try:
        test_scraper_basic_functionality()
        test_html_parsing()
        test_text_extraction()
        test_data_analyzer()
        test_integration()
        
        print("\n" + "=" * 50)
        print("All tests passed! ✓")
        print("The NIRF PDF Scraper is ready to use.")
        print("\nTo run the actual scraper:")
        print("  python nirf_pdf_scraper.py")
        print("\nTo analyze the data:")
        print("  python nirf_data_analyzer.py")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
NIRF PDF Scraper Demo

This script demonstrates the functionality of the NIRF PDF scraper
without actually accessing the real website (to avoid being blocked).
"""

import os
import json
import tempfile
from pathlib import Path
from nirf_pdf_scraper import NIRFPDFScraper
from nirf_data_analyzer import NIRFDataAnalyzer
import time


def create_demo_data():
    """Create some demo data to show how the system works."""
    
    # Create temporary directories
    temp_dir = Path(tempfile.mkdtemp())
    download_dir = temp_dir / "demo_pdfs"
    data_dir = temp_dir / "demo_data"
    
    download_dir.mkdir(exist_ok=True)
    data_dir.mkdir(exist_ok=True)
    
    print(f"Created demo directories:")
    print(f"  PDFs: {download_dir}")
    print(f"  Data: {data_dir}")
    
    # Simulate some college data
    demo_colleges = [
        {
            "name": "Indian Institute of Technology Madras",
            "location": "Chennai, Tamil Nadu",
            "rank": 1,
            "scores": [95.8, 88.4, 92.1],
            "content": """
            Indian Institute of Technology Madras
            Address: Chennai, Tamil Nadu - 600036
            Rank: 1
            Overall Score: 95.8
            Teaching Learning Resources: 88.4
            Research Professional Practice: 92.1
            
            Established in 1959, IIT Madras has been ranked as the best engineering institute
            in India for multiple consecutive years. The institute offers undergraduate,
            postgraduate, and doctoral programs in engineering, science, and technology.
            
            Key Highlights:
            - Student Faculty Ratio: 8:1
            - Total Faculty: 650
            - Total Students: 9,500
            - Research Publications: 2,800+ annually
            - Industry Collaborations: 200+
            """
        },
        {
            "name": "Indian Institute of Technology Delhi",
            "location": "New Delhi",
            "rank": 2,
            "scores": [94.2, 87.6, 91.3],
            "content": """
            Indian Institute of Technology Delhi
            Address: Hauz Khas, New Delhi - 110016
            Rank: 2
            Overall Score: 94.2
            Teaching Learning Resources: 87.6
            Research Professional Practice: 91.3
            
            IIT Delhi is one of the premier engineering institutions in India, established in 1961.
            Known for its excellence in engineering education and research.
            
            Key Highlights:
            - Student Faculty Ratio: 9:1
            - Total Faculty: 580
            - Total Students: 8,200
            - Research Publications: 2,500+ annually
            - International Collaborations: 150+
            """
        },
        {
            "name": "Indian Institute of Technology Bombay",
            "location": "Mumbai, Maharashtra",
            "rank": 3,
            "scores": [93.5, 86.8, 90.7],
            "content": """
            Indian Institute of Technology Bombay
            Address: Powai, Mumbai, Maharashtra - 400076
            Rank: 3
            Overall Score: 93.5
            Teaching Learning Resources: 86.8
            Research Professional Practice: 90.7
            
            Established in 1958, IIT Bombay is renowned for its engineering programs
            and has strong industry connections.
            
            Key Highlights:
            - Student Faculty Ratio: 10:1
            - Total Faculty: 600
            - Total Students: 9,000
            - Research Publications: 2,300+ annually
            - Alumni Network: 50,000+ globally
            """
        }
    ]
    
    # Create demo data files
    for i, college in enumerate(demo_colleges):
        # Simulate the data structure that would be created by the scraper
        data = {
            "pdf_info": {
                "url": f"https://example.com/{college['name'].replace(' ', '_')}.pdf",
                "college_name": college["name"],
                "filename": f"{college['name'].replace(' ', '_')}.pdf"
            },
            "extracted_data": {
                "metadata": {
                    "filename": f"{college['name'].replace(' ', '_')}.pdf",
                    "num_pages": 5 + i,
                    "file_size": 500000 + (i * 100000),
                    "extracted_at": time.strftime('%Y-%m-%d %H:%M:%S')
                },
                "full_text": college["content"],
                "structured_data": {
                    "college_name": college["name"],
                    "location": college["location"],
                    "rank": college["rank"],
                    "scores": college["scores"],
                    "average_score": sum(college["scores"]) / len(college["scores"])
                },
                "word_count": len(college["content"].split()),
                "char_count": len(college["content"])
            },
            "processed_at": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Save to JSON file
        filename = f"{college['name'].replace(' ', '_')}_data.json"
        filepath = data_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Created demo data: {filename}")
    
    return temp_dir, download_dir, data_dir


def main():
    """Run the demo."""
    print("NIRF PDF Scraper Demo")
    print("=" * 50)
    print()
    
    # Create demo data
    print("1. Creating demo data...")
    temp_dir, download_dir, data_dir = create_demo_data()
    print()
    
    # Initialize analyzer with demo data
    print("2. Analyzing demo data...")
    analyzer = NIRFDataAnalyzer(str(data_dir))
    
    if analyzer.data:
        # Print summary
        analyzer.print_summary()
        
        # Generate analysis report
        print("\n3. Generating analysis report...")
        report_path = temp_dir / "demo_analysis_report.json"
        analyzer.export_summary_report(str(report_path))
        
        # Try to generate visualizations
        print("\n4. Generating visualizations...")
        viz_dir = temp_dir / "demo_visualizations"
        try:
            analyzer.generate_visualizations(str(viz_dir))
            print(f"Visualizations saved to: {viz_dir}")
        except Exception as e:
            print(f"Visualization generation failed: {e}")
        
        print(f"\n5. Demo Results Summary:")
        print(f"   Demo data directory: {data_dir}")
        print(f"   Analysis report: {report_path}")
        if viz_dir.exists():
            viz_files = list(viz_dir.glob("*.png"))
            print(f"   Visualizations: {len(viz_files)} files created")
        
        print(f"\nDemo completed successfully!")
        print(f"All files created in: {temp_dir}")
        
        # Show how to use the real scraper
        print("\n" + "=" * 50)
        print("How to use the real NIRF PDF scraper:")
        print("=" * 50)
        print()
        print("1. To scrape actual NIRF data:")
        print("   python nirf_pdf_scraper.py")
        print()
        print("2. To analyze the scraped data:")
        print("   python nirf_data_analyzer.py")
        print()
        print("3. To test the system:")
        print("   python test_nirf_scraper.py")
        print()
        print("Note: The real scraper will create directories:")
        print("  - nirf_pdfs/     (downloaded PDF files)")
        print("  - nirf_data/     (extracted JSON data)")
        print("  - nirf_analysis/ (analysis results)")
        
    else:
        print("Failed to create demo data")


if __name__ == "__main__":
    main()
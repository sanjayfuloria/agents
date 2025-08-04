#!/usr/bin/env python3
"""
NIRF Data Analyzer

This script analyzes the extracted data from NIRF Engineering Rankings PDFs.

Author: AI Agent
Date: 2025
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any
from collections import Counter, defaultdict
import re

try:
    import pandas as pd
    import numpy as np
    PANDAS_AVAILABLE = True
except ImportError:
    print("Warning: pandas not available. Some features will be limited.")
    PANDAS_AVAILABLE = False
    pd = None
    np = None

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    print("Warning: matplotlib/seaborn not available. Visualizations will be skipped.")
    MATPLOTLIB_AVAILABLE = False
    plt = None
    sns = None


class NIRFDataAnalyzer:
    """
    A class to analyze data extracted from NIRF Engineering Rankings PDFs.
    """
    
    def __init__(self, data_dir: str = "nirf_data"):
        """
        Initialize the analyzer.
        
        Args:
            data_dir: Directory containing extracted JSON data files
        """
        self.data_dir = Path(data_dir)
        self.data = []
        self.df = None
        
        if not self.data_dir.exists():
            print(f"Data directory {data_dir} does not exist. Please run the scraper first.")
            return
        
        self.load_data()
    
    def load_data(self) -> None:
        """Load all JSON data files from the data directory."""
        json_files = list(self.data_dir.glob("*_data.json"))
        
        print(f"Found {len(json_files)} data files to analyze")
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.data.append(data)
            except Exception as e:
                print(f"Error loading {json_file}: {e}")
        
        print(f"Successfully loaded {len(self.data)} data files")
        
        if self.data:
            self.create_dataframe()
    
    def create_dataframe(self) -> None:
        """Create a pandas DataFrame from the loaded data."""
        if not PANDAS_AVAILABLE:
            print("Pandas not available. Skipping DataFrame creation.")
            return
            
        records = []
        
        for item in self.data:
            record = {}
            
            # Extract basic info
            pdf_info = item.get('pdf_info', {})
            extracted_data = item.get('extracted_data', {})
            structured_data = extracted_data.get('structured_data', {})
            metadata = extracted_data.get('metadata', {})
            
            # Basic information
            record['filename'] = pdf_info.get('filename', 'unknown')
            record['college_name'] = (structured_data.get('college_name') or 
                                    pdf_info.get('college_name', 'unknown'))
            record['location'] = structured_data.get('location', 'unknown')
            record['rank'] = structured_data.get('rank')
            
            # File metadata
            record['file_size'] = metadata.get('file_size', 0)
            record['num_pages'] = metadata.get('num_pages', 0)
            record['word_count'] = extracted_data.get('word_count', 0)
            record['char_count'] = extracted_data.get('char_count', 0)
            
            # Scores and ratings
            scores = structured_data.get('scores', [])
            record['num_scores'] = len(scores)
            record['average_score'] = structured_data.get('average_score')
            record['max_score'] = max(scores) if scores else None
            record['min_score'] = min(scores) if scores else None
            
            # Text analysis
            full_text = extracted_data.get('full_text', '')
            record['text_length'] = len(full_text)
            record['unique_words'] = len(set(full_text.lower().split())) if full_text else 0
            
            # Processing info
            record['processed_at'] = item.get('processed_at')
            record['extraction_successful'] = len(full_text) > 0
            
            records.append(record)
        
        self.df = pd.DataFrame(records)
        print(f"Created DataFrame with {len(self.df)} rows and {len(self.df.columns)} columns")
    
    def basic_statistics(self) -> Dict[str, Any]:
        """Generate basic statistics about the data."""
        if not self.data:
            return {"error": "No data available"}
        
        # If pandas is not available, use basic Python statistics
        if not PANDAS_AVAILABLE or self.df is None:
            stats = {
                "total_colleges": len(self.data),
                "note": "Limited statistics without pandas"
            }
            
            # Count successful extractions
            successful = sum(1 for item in self.data 
                           if item.get('extracted_data', {}).get('full_text', ''))
            stats["successful_extractions"] = successful
            stats["failed_extractions"] = len(self.data) - successful
            stats["success_rate"] = f"{(successful / len(self.data) * 100):.1f}%" if self.data else "0%"
            
            return stats
        
        # Full statistics with pandas
        if self.df.empty:
            return {"error": "No data available"}
        
        stats = {
            "total_colleges": len(self.df),
            "successful_extractions": self.df['extraction_successful'].sum(),
            "failed_extractions": (~self.df['extraction_successful']).sum(),
            "success_rate": f"{(self.df['extraction_successful'].sum() / len(self.df) * 100):.1f}%"
        }
        
        # File statistics
        if 'file_size' in self.df.columns:
            stats["avg_file_size_mb"] = f"{self.df['file_size'].mean() / (1024*1024):.2f}"
            stats["total_data_mb"] = f"{self.df['file_size'].sum() / (1024*1024):.2f}"
        
        # Page statistics
        if 'num_pages' in self.df.columns:
            stats["avg_pages"] = f"{self.df['num_pages'].mean():.1f}"
            stats["total_pages"] = int(self.df['num_pages'].sum())
        
        # Text statistics
        if 'word_count' in self.df.columns:
            stats["avg_words_per_college"] = f"{self.df['word_count'].mean():.0f}"
            stats["total_words_extracted"] = int(self.df['word_count'].sum())
        
        # Ranking statistics
        ranked_colleges = self.df[self.df['rank'].notna()]
        if not ranked_colleges.empty:
            stats["colleges_with_rank"] = len(ranked_colleges)
            stats["highest_rank"] = int(ranked_colleges['rank'].min())
            stats["lowest_rank"] = int(ranked_colleges['rank'].max())
        
        return stats
    
    def analyze_colleges(self) -> Dict[str, Any]:
        """Analyze college-specific information."""
        if self.df is None or self.df.empty:
            return {"error": "No data available"}
        
        analysis = {}
        
        # Top colleges by rank
        ranked_df = self.df[self.df['rank'].notna()].sort_values('rank')
        if not ranked_df.empty:
            analysis["top_10_colleges"] = ranked_df[['college_name', 'rank', 'location']].head(10).to_dict('records')
        
        # Colleges by location
        location_counts = self.df['location'].value_counts()
        analysis["colleges_by_location"] = location_counts.head(10).to_dict()
        
        # Score analysis
        scored_df = self.df[self.df['average_score'].notna()]
        if not scored_df.empty:
            analysis["highest_scoring_colleges"] = (
                scored_df.nlargest(10, 'average_score')[['college_name', 'average_score', 'rank']]
                .to_dict('records')
            )
        
        # File size analysis (might indicate data richness)
        if 'file_size' in self.df.columns:
            analysis["largest_files"] = (
                self.df.nlargest(5, 'file_size')[['college_name', 'file_size', 'num_pages']]
                .to_dict('records')
            )
        
        return analysis
    
    def text_analysis(self) -> Dict[str, Any]:
        """Analyze text content across all PDFs."""
        if self.df is None or self.df.empty:
            return {"error": "No data available"}
        
        analysis = {}
        
        # Combine all text for analysis
        all_text = ""
        for item in self.data:
            full_text = item.get('extracted_data', {}).get('full_text', '')
            all_text += full_text + " "
        
        if not all_text.strip():
            return {"error": "No text data available"}
        
        # Word frequency analysis
        words = re.findall(r'\b[a-zA-Z]{3,}\b', all_text.lower())
        word_freq = Counter(words)
        
        # Remove common stop words
        stop_words = {'the', 'and', 'for', 'are', 'with', 'this', 'that', 'from', 'they', 'have', 'been', 'will', 'their', 'said', 'each', 'which', 'what', 'were', 'been', 'more', 'than', 'into', 'very', 'after', 'first', 'well', 'year', 'years'}
        filtered_freq = {word: count for word, count in word_freq.items() if word not in stop_words}
        
        analysis["most_common_words"] = dict(Counter(filtered_freq).most_common(20))
        analysis["total_unique_words"] = len(word_freq)
        analysis["total_words"] = len(words)
        
        # Look for specific engineering-related terms
        engineering_terms = ['engineering', 'technology', 'technical', 'science', 'research', 'laboratory', 'faculty', 'department', 'program', 'course', 'student', 'education', 'academic', 'institute', 'university', 'college']
        engineering_freq = {term: word_freq.get(term, 0) for term in engineering_terms}
        analysis["engineering_terms_frequency"] = {k: v for k, v in engineering_freq.items() if v > 0}
        
        return analysis
    
    def generate_visualizations(self, output_dir: str = "nirf_analysis") -> None:
        """Generate visualization plots."""
        if not MATPLOTLIB_AVAILABLE:
            print("Matplotlib not available. Skipping visualizations.")
            return
            
        if self.df is None or self.df.empty:
            print("No data available for visualization")
            return
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Set style
        plt.style.use('default')
        sns.set_palette("husl")
        
        # 1. Distribution of file sizes
        if 'file_size' in self.df.columns and self.df['file_size'].notna().any():
            plt.figure(figsize=(10, 6))
            self.df['file_size_mb'] = self.df['file_size'] / (1024 * 1024)
            plt.hist(self.df['file_size_mb'].dropna(), bins=20, alpha=0.7)
            plt.xlabel('File Size (MB)')
            plt.ylabel('Number of Colleges')
            plt.title('Distribution of PDF File Sizes')
            plt.savefig(output_path / 'file_size_distribution.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        # 2. Pages vs Word Count
        if 'num_pages' in self.df.columns and 'word_count' in self.df.columns:
            valid_data = self.df[(self.df['num_pages'] > 0) & (self.df['word_count'] > 0)]
            if not valid_data.empty:
                plt.figure(figsize=(10, 6))
                plt.scatter(valid_data['num_pages'], valid_data['word_count'], alpha=0.6)
                plt.xlabel('Number of Pages')
                plt.ylabel('Word Count')
                plt.title('Pages vs Word Count')
                plt.savefig(output_path / 'pages_vs_words.png', dpi=300, bbox_inches='tight')
                plt.close()
        
        # 3. Top locations
        if 'location' in self.df.columns:
            location_counts = self.df['location'].value_counts().head(15)
            if not location_counts.empty:
                plt.figure(figsize=(12, 8))
                location_counts.plot(kind='bar')
                plt.xlabel('Location')
                plt.ylabel('Number of Colleges')
                plt.title('Top 15 Locations by Number of Colleges')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                plt.savefig(output_path / 'colleges_by_location.png', dpi=300, bbox_inches='tight')
                plt.close()
        
        # 4. Rank distribution
        ranked_df = self.df[self.df['rank'].notna()]
        if not ranked_df.empty:
            plt.figure(figsize=(10, 6))
            plt.hist(ranked_df['rank'], bins=20, alpha=0.7)
            plt.xlabel('Rank')
            plt.ylabel('Number of Colleges')
            plt.title('Distribution of College Rankings')
            plt.savefig(output_path / 'rank_distribution.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        print(f"Visualizations saved to {output_path}")
    
    def export_summary_report(self, output_file: str = "nirf_analysis_report.json") -> None:
        """Export a comprehensive analysis report."""
        report = {
            "analysis_timestamp": "2025-01-01T00:00:00",  # Fallback timestamp
            "basic_statistics": self.basic_statistics(),
            "college_analysis": self.analyze_colleges(),
            "text_analysis": self.text_analysis()
        }
        
        if PANDAS_AVAILABLE and pd is not None:
            report["analysis_timestamp"] = pd.Timestamp.now().isoformat()
        
        # Add DataFrame summary if available
        if self.df is not None:
            report["dataframe_info"] = {
                "shape": self.df.shape,
                "columns": list(self.df.columns),
                "missing_data": self.df.isnull().sum().to_dict()
            }
        
        output_path = Path(output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"Analysis report exported to {output_path}")
    
    def print_summary(self) -> None:
        """Print a summary of the analysis."""
        print("\n" + "="*60)
        print("NIRF Engineering Rankings Analysis Summary")
        print("="*60)
        
        stats = self.basic_statistics()
        
        print(f"\nData Overview:")
        print(f"  Total colleges analyzed: {stats.get('total_colleges', 0)}")
        print(f"  Successful text extractions: {stats.get('successful_extractions', 0)}")
        print(f"  Success rate: {stats.get('success_rate', 'N/A')}")
        
        if 'total_data_mb' in stats:
            print(f"  Total data processed: {stats['total_data_mb']} MB")
            print(f"  Average file size: {stats['avg_file_size_mb']} MB")
        
        if 'total_pages' in stats:
            print(f"  Total pages processed: {stats['total_pages']}")
            print(f"  Average pages per college: {stats['avg_pages']}")
        
        if 'total_words_extracted' in stats:
            print(f"  Total words extracted: {stats['total_words_extracted']:,}")
            print(f"  Average words per college: {stats['avg_words_per_college']}")
        
        # Rankings info
        if 'colleges_with_rank' in stats:
            print(f"\nRanking Information:")
            print(f"  Colleges with rank data: {stats['colleges_with_rank']}")
            print(f"  Highest rank (best): {stats.get('highest_rank', 'N/A')}")
            print(f"  Lowest rank: {stats.get('lowest_rank', 'N/A')}")
        
        # College analysis
        college_analysis = self.analyze_colleges()
        if 'top_10_colleges' in college_analysis:
            print(f"\nTop 10 Ranked Colleges:")
            for i, college in enumerate(college_analysis['top_10_colleges'][:5], 1):
                print(f"  {i}. {college['college_name']} (Rank: {college['rank']})")
        
        if 'colleges_by_location' in college_analysis:
            print(f"\nTop Locations by Number of Colleges:")
            for location, count in list(college_analysis['colleges_by_location'].items())[:5]:
                print(f"  {location}: {count} colleges")
        
        print("\n" + "="*60)


def main():
    """Main function to run the analyzer."""
    print("NIRF Engineering Rankings Data Analyzer")
    print("=======================================")
    
    # Initialize analyzer
    analyzer = NIRFDataAnalyzer()
    
    if not analyzer.data:
        print("No data found. Please run the scraper first with nirf_pdf_scraper.py")
        return
    
    # Print summary
    analyzer.print_summary()
    
    # Generate visualizations
    print("\nGenerating visualizations...")
    try:
        analyzer.generate_visualizations()
    except ImportError:
        print("Matplotlib/Seaborn not available. Skipping visualizations.")
    except Exception as e:
        print(f"Error generating visualizations: {e}")
    
    # Export detailed report
    print("\nExporting detailed analysis report...")
    analyzer.export_summary_report()
    
    print("\nAnalysis complete!")


if __name__ == "__main__":
    main()
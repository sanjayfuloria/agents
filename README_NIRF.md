# NIRF Engineering Rankings PDF Scraper

This project provides tools to download and analyze PDF documents from the NIRF (National Institutional Ranking Framework) India Engineering Rankings website.

## Features

- **PDF Scraping**: Automatically discovers and downloads PDF documents from the NIRF rankings page
- **Data Extraction**: Extracts text content and metadata from downloaded PDFs
- **Structured Data**: Attempts to extract structured information like college names, rankings, scores, and locations
- **Data Analysis**: Provides comprehensive analysis of the extracted data
- **Visualizations**: Generates charts and graphs to visualize the data
- **Export Options**: Saves data in JSON format and generates analysis reports

## Files

- `nirf_pdf_scraper.py`: Main scraper script that downloads PDFs and extracts data
- `nirf_data_analyzer.py`: Analysis script that processes extracted data and generates reports
- `nirf_config.json`: Configuration file with settings and parameters
- `README_NIRF.md`: This documentation file

## Requirements

The following Python packages are required (most are already included in the project dependencies):

- `requests`: For HTTP requests
- `beautifulsoup4`: For HTML parsing
- `lxml`: For XML/HTML processing
- `pypdf`: For PDF text extraction
- `pandas`: For data analysis (optional but recommended)
- `matplotlib`: For visualizations (optional)
- `seaborn`: For enhanced visualizations (optional)

## Installation

1. Ensure you have the required dependencies installed:
```bash
pip install requests beautifulsoup4 lxml pypdf pandas matplotlib seaborn
```

2. The scripts are ready to use from the project root directory.

## Usage

### Step 1: Download and Extract Data

Run the main scraper script to download PDFs and extract data:

```bash
python nirf_pdf_scraper.py
```

This will:
- Scrape the NIRF Engineering Rankings website for PDF links
- Download each PDF to the `nirf_pdfs/` directory
- Extract text and metadata from each PDF
- Save structured data to JSON files in the `nirf_data/` directory
- Create a summary report of the scraping process

### Step 2: Analyze the Data

After the scraper has finished, run the analyzer to process the extracted data:

```bash
python nirf_data_analyzer.py
```

This will:
- Load all extracted data files
- Generate comprehensive statistics
- Create visualizations (saved to `nirf_analysis/` directory)
- Export a detailed analysis report (`nirf_analysis_report.json`)
- Print a summary to the console

## Output Structure

### Downloaded PDFs
```
nirf_pdfs/
├── College_Name_1.pdf
├── College_Name_2.pdf
└── ...
```

### Extracted Data
```
nirf_data/
├── College_Name_1_data.json
├── College_Name_2_data.json
├── scraping_summary.json
└── ...
```

### Analysis Results
```
nirf_analysis/
├── file_size_distribution.png
├── pages_vs_words.png
├── colleges_by_location.png
├── rank_distribution.png
└── nirf_analysis_report.json
```

## Data Structure

Each extracted data file contains:

```json
{
  "pdf_info": {
    "url": "PDF download URL",
    "college_name": "Extracted college name",
    "filename": "Local filename"
  },
  "extracted_data": {
    "metadata": {
      "filename": "PDF filename",
      "num_pages": "Number of pages",
      "file_size": "File size in bytes"
    },
    "full_text": "Complete extracted text",
    "structured_data": {
      "college_name": "College name",
      "location": "College location",
      "rank": "Ranking number",
      "scores": ["List of scores found"],
      "average_score": "Average score"
    },
    "word_count": "Total words",
    "char_count": "Total characters"
  },
  "processed_at": "Processing timestamp"
}
```

## Configuration

You can modify `nirf_config.json` to customize:

- Target URLs
- Directory paths
- Request timeouts
- Download delays
- Pattern matching for PDFs and college names

## Troubleshooting

### Common Issues

1. **No PDFs found**: 
   - Check if the website structure has changed
   - Verify the URL is accessible
   - Look at the HTML source to understand the page structure

2. **Download failures**:
   - Check your internet connection
   - Some PDFs might be restricted or require authentication
   - Increase timeout values in the configuration

3. **Text extraction errors**:
   - Some PDFs might be image-based (scanned) and require OCR
   - Encrypted or password-protected PDFs cannot be processed
   - Corrupted PDF files will be skipped

4. **Analysis errors**:
   - Ensure pandas is installed for full analysis features
   - Install matplotlib/seaborn for visualizations
   - Check that data files exist in the expected directory

### Logging

The scraper includes detailed logging. Check the console output for:
- Progress updates
- Error messages
- File processing status
- Summary statistics

## Legal and Ethical Considerations

- **Respect robots.txt**: Check the website's robots.txt file
- **Rate limiting**: The scraper includes delays between requests
- **Fair use**: Only download what you need for legitimate research/analysis
- **Copyright**: Respect the copyright of the downloaded content
- **Terms of service**: Review the website's terms of service before scraping

## Customization

### Adding New Extraction Patterns

To extract additional data from PDFs, modify the `_extract_structured_data` method in `NIRFPDFScraper`:

```python
# Add new patterns for specific data
new_pattern = r'Your Pattern Here[:\s]+([^\n]+)'
match = re.search(new_pattern, text, re.IGNORECASE)
if match:
    structured['new_field'] = match.group(1).strip()
```

### Supporting Different Websites

To adapt the scraper for other ranking websites:

1. Update the `base_url` in the configuration
2. Modify the `get_pdf_links` method to match the new site structure
3. Adjust the college name extraction logic if needed

### Custom Analysis

Add new analysis functions to `NIRFDataAnalyzer`:

```python
def custom_analysis(self) -> Dict[str, Any]:
    """Your custom analysis logic here."""
    # Implement your analysis
    return results
```

## Future Enhancements

Potential improvements could include:

- OCR support for image-based PDFs
- Machine learning for better data extraction
- Database storage instead of JSON files
- Web interface for data exploration
- Real-time monitoring of ranking changes
- Integration with other ranking systems

## Support

For issues or questions:

1. Check the console output for error messages
2. Review the generated log files
3. Verify all dependencies are installed
4. Test with a single PDF first
5. Check the website accessibility

## License

This tool is provided for educational and research purposes. Please respect the terms of service of the websites you scrape and the copyright of the downloaded content.
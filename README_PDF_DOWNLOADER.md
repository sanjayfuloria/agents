# Generic PDF Downloader

A flexible Python program to download PDF documents from any website. This tool can automatically discover and download PDF files from web pages based on configurable patterns and rules.

## Features

- **Universal Website Support**: Works with any website structure
- **Intelligent PDF Discovery**: Multiple methods to find PDF links
- **Configurable Patterns**: Customizable rules for PDF detection
- **Robust Downloads**: Retry logic, timeout handling, and error recovery
- **Content Verification**: Validates downloaded files are actual PDFs
- **Organized Storage**: Option to create subdirectories by domain
- **Progress Tracking**: Detailed logging and summary reports
- **Command-line Interface**: Easy to use from terminal or scripts

## Quick Start

### Basic Usage

```bash
# Download PDFs from a website
python pdf_downloader.py https://example.com/documents

# Specify output directory
python pdf_downloader.py https://university.edu/papers --output-dir ./research_papers/

# Use configuration file
python pdf_downloader.py https://site.com --config my_config.json

# Verbose mode with custom settings
python pdf_downloader.py https://docs.site.com --verbose --delay 2 --max-retries 5
```

### Python API Usage

```python
from pdf_downloader import PDFDownloader

# Basic usage
downloader = PDFDownloader(
    base_url="https://example.com/documents",
    download_dir="my_pdfs"
)

# Download all PDFs
summary = downloader.download_all_pdfs()
print(f"Downloaded {summary['pdfs_downloaded']} PDFs")

# Advanced configuration
config = {
    'delay_between_downloads': 2.0,
    'max_retries': 5,
    'create_subdirs': True,
    'verify_pdf_content': True
}

downloader = PDFDownloader(
    base_url="https://research.university.edu",
    download_dir="research_papers",
    config=config
)

# Download from multiple URLs
urls = [
    "https://university.edu/cs/papers",
    "https://university.edu/math/publications",
    "https://university.edu/physics/research"
]

summary = downloader.download_all_pdfs(urls)
```

## Configuration

### Configuration File

Create a JSON configuration file to customize the downloader behavior:

```json
{
    "request_timeout": 30,
    "download_timeout": 120,
    "delay_between_downloads": 1,
    "max_retries": 3,
    "pdf_patterns": [
        ".*\\.pdf$",
        ".*\\.PDF$",
        ".*\\.pdf\\?.*"
    ],
    "exclude_patterns": [
        ".*\\.php.*pdf.*",
        ".*javascript:"
    ],
    "link_selectors": [
        "a[href$=\".pdf\"]",
        "a[href*=\"pdf\"]"
    ],
    "filename_max_length": 100,
    "create_subdirs": true,
    "verify_pdf_content": true
}
```

### Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `request_timeout` | 30 | Timeout for web requests (seconds) |
| `download_timeout` | 120 | Timeout for file downloads (seconds) |
| `delay_between_downloads` | 1 | Delay between downloads (seconds) |
| `max_retries` | 3 | Maximum retry attempts for failed downloads |
| `pdf_patterns` | See default | Regular expressions to match PDF URLs |
| `exclude_patterns` | See default | Patterns to exclude from downloads |
| `link_selectors` | See default | CSS selectors for finding PDF links |
| `filename_max_length` | 100 | Maximum length for generated filenames |
| `create_subdirs` | true | Create subdirectories by domain |
| `verify_pdf_content` | true | Verify downloaded files are PDFs |

## How It Works

### PDF Discovery Methods

The downloader uses multiple strategies to find PDF links:

1. **CSS Selectors**: Searches for specific link patterns
2. **URL Pattern Matching**: Uses regular expressions on all links
3. **Embedded Content**: Finds PDFs in `<object>`, `<embed>`, and `<iframe>` tags
4. **Content Analysis**: Examines link context for meaningful titles

### Smart Filename Generation

- Uses link text or title attributes when available
- Cleans special characters and formats consistently
- Handles duplicate names automatically
- Limits filename length for filesystem compatibility

### Download Process

1. **Discovery Phase**: Scans target website(s) for PDF links
2. **Deduplication**: Removes duplicate URLs
3. **Download Phase**: Downloads each PDF with retry logic
4. **Verification**: Checks PDF file signatures (if enabled)
5. **Reporting**: Generates summary with statistics

## Command Line Options

```
python pdf_downloader.py URL [OPTIONS]

Positional Arguments:
  url                   Website URL to download PDFs from

Options:
  -o, --output-dir      Output directory for downloaded PDFs
  -c, --config          Configuration file path
  -d, --delay           Delay between downloads in seconds
  -t, --timeout         Request timeout in seconds
  -r, --max-retries     Maximum retry attempts for failed downloads
  --no-verify           Skip PDF content verification
  -v, --verbose         Enable verbose logging
  -h, --help            Show help message
```

## Examples

### Research Paper Collection

```bash
# Download computer science papers
python pdf_downloader.py https://arxiv.org/list/cs.AI/recent \
    --output-dir ./cs_papers/ \
    --delay 2 \
    --verbose

# Download from multiple conferences
python pdf_downloader.py https://nips.cc/Conferences/2024/Schedule \
    --config research_config.json
```

### Document Archives

```bash
# Download government documents
python pdf_downloader.py https://government.site/documents \
    --output-dir ./gov_docs/ \
    --no-verify \
    --max-retries 5

# Download technical specifications
python pdf_downloader.py https://standards.org/specifications \
    --delay 3 \
    --timeout 60
```

### Bulk Collection

```python
# Python script for bulk downloads
from pdf_downloader import PDFDownloader

sites = [
    "https://university1.edu/papers",
    "https://university2.edu/research", 
    "https://university3.edu/publications"
]

for site in sites:
    print(f"Processing {site}...")
    downloader = PDFDownloader(site, f"papers/{site.split('//')[1].split('/')[0]}")
    summary = downloader.download_all_pdfs()
    print(f"Downloaded {summary['pdfs_downloaded']} PDFs from {site}")
```

## Output

### Directory Structure

```
downloaded_pdfs/
├── example.com/
│   ├── document1.pdf
│   ├── research_paper.pdf
│   └── report_2024.pdf
├── university.edu/
│   ├── thesis_smith.pdf
│   └── conference_proceedings.pdf
└── download_summary.json
```

### Summary Report

The downloader generates a detailed JSON summary:

```json
{
    "start_time": "2025-01-06 10:30:00",
    "end_time": "2025-01-06 10:35:30",
    "urls_scanned": ["https://example.com/docs"],
    "pdfs_found": 15,
    "pdfs_downloaded": 12,
    "successful_downloads": [
        {
            "filename": "important_document.pdf",
            "url": "https://example.com/doc.pdf",
            "filepath": "/path/to/downloaded/file.pdf"
        }
    ],
    "failed_downloads": [...],
    "errors": [...]
}
```

## Error Handling

- **Network Issues**: Automatic retries with exponential backoff
- **Invalid PDFs**: Content verification catches non-PDF files
- **File System**: Handles long filenames and invalid characters
- **Rate Limiting**: Configurable delays to respect server limits

## Best Practices

1. **Respect Robots.txt**: Check site's robots.txt before bulk downloading
2. **Use Delays**: Set appropriate delays to avoid overwhelming servers
3. **Monitor Progress**: Use verbose mode for long-running operations
4. **Configure Timeouts**: Adjust timeouts based on site responsiveness
5. **Verify Content**: Keep PDF verification enabled for quality assurance

## Comparison with NIRF Scraper

| Feature | Generic PDF Downloader | NIRF PDF Scraper |
|---------|------------------------|------------------|
| Target | Any website | NIRF rankings only |
| Configuration | Highly configurable | NIRF-specific |
| PDF Discovery | Multiple methods | NIRF-optimized |
| Data Extraction | Download only | Full text extraction |
| Analysis | Basic summary | Advanced analytics |
| Use Case | General purpose | Educational rankings |

## Troubleshooting

### Common Issues

**No PDFs found:**
- Check if the website actually contains PDF links
- Verify the URL is accessible
- Try different CSS selectors in configuration

**Download failures:**
- Increase timeout values
- Check network connectivity
- Verify the PDF URLs are still valid

**Permission denied:**
- Check output directory permissions
- Try a different output location

**Large file handling:**
- Increase download timeout
- Check available disk space

## Requirements

- Python 3.6+
- requests
- beautifulsoup4
- pathlib (included in Python 3.4+)

## Installation

```bash
# Install dependencies
pip install requests beautifulsoup4

# Download the script
wget https://raw.githubusercontent.com/example/pdf_downloader.py

# Make executable
chmod +x pdf_downloader.py
```

## License

This tool is provided as-is for educational and research purposes. Please respect website terms of service and copyright when downloading content.
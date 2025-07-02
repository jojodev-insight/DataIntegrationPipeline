# Document Parser

A professional Python project that extracts content from PDF, DOCX, Excel, and CSV files, converting them into structured JSON format with consistent schema.

## Features

- Parse PDF, DOCX, Excel (XLSX/XLS), and CSV files with page-by-page content extraction
- Preserve document structure (paragraphs, headings, tables, etc.)
- Standardized JSON output schema for all document types
- Command-line interface and importable package
- Comprehensive error handling and logging
- Type hints and comprehensive documentation
- Unit tests with pytest

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd DataIntegrationPipeline
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

```bash
# Parse a PDF file
python -m document_parser parse document.pdf --output output.json

# Parse an Excel file
python -m document_parser parse spreadsheet.xlsx --output output.json --pretty

# Parse a CSV file
python -m document_parser parse data.csv --output output.json

# Parse multiple files of different types
python -m document_parser parse *.pdf *.docx *.xlsx *.csv --output-dir results/
```

### Python API

```python
from document_parser import DocumentParser

parser = DocumentParser()

# Parse a PDF file
result = parser.parse_file("document.pdf")
print(result.to_json(pretty=True))

# Parse an Excel file
result = parser.parse_file("spreadsheet.xlsx")
print(f"Sheets: {result.document_info.total_pages}")

# Parse a CSV file  
result = parser.parse_file("data.csv")
print(result.to_json(pretty=True))
```

## JSON Output Schema

```json
{
  "document_info": {
    "filename": "example.pdf",
    "file_type": "pdf",
    "total_pages": 5,
    "created_at": "2025-06-30T12:00:00Z",
    "file_size": 1024000
  },
  "pages": [
    {
      "page_number": 1,
      "content": {
        "text": "Page content here...",
        "paragraphs": ["Paragraph 1", "Paragraph 2"],
        "headings": [
          {
            "level": 1,
            "text": "Main Heading"
          }
        ]
      },
      "metadata": {
        "word_count": 250,
        "char_count": 1500
      }
    }
  ]
}
```

## Development

### Running Tests

```bash
pytest tests/ -v --cov=document_parser
```

### Code Formatting

```bash
black document_parser/ tests/
flake8 document_parser/ tests/
mypy document_parser/
```

## Project Structure

```
DataIntegrationPipeline/
├── document_parser/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── parser.py
│   │   └── models.py
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── pdf_parser.py
│   │   └── docx_parser.py
│   ├── cli/
│   │   ├── __init__.py
│   │   └── main.py
│   └── utils/
│       ├── __init__.py
│       ├── exceptions.py
│       └── logging.py
├── tests/
├── sample_files/
├── requirements.txt
└── README.md
```

## License

MIT License

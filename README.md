# Document Parser

A simple python project that makes the file parsing mechanism easier to bind to
your Jinja template files.

## Features

- **Multi-format parsing**: Parse PDF, DOCX, Excel (XLSX/XLS), and CSV files with page-by-page content extraction
- **Document structure preservation**: Maintain paragraphs, headings, tables, and formatting
- **Jinja2 template rendering**: Render parsed data into customizable templates (strings and files)
- **Standardized JSON output**: Consistent schema for all document types
- **Template binding**: Easy data binding from parsed documents to Jinja2 templates
- **Multiple output formats**: Generate reports, summaries, and custom formats using templates
- **Command-line interface and importable package**: Use as CLI tool or Python library
- **Comprehensive error handling and logging**: Robust error management
- **Unit tests with pytest**: Full test coverage

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

# Initialize with template directory
parser = DocumentParser({'template_dir': 'sample_files'})

# Parse a PDF file
result = parser.parse_file("document.pdf")
print(result.to_json(pretty=True))

# Parse an Excel file
result = parser.parse_file("spreadsheet.xlsx")
print(f"Sheets: {result.document_info.total_pages}")

# Parse a CSV file  
result = parser.parse_file("data.csv")
print(result.to_json(pretty=True))

# Render parsed data with templates
# Method 1: Render with template string
template_string = "File: {{ document_info.filename }}, Pages: {{ document_info.total_pages }}"
rendered = parser.render_template(template_string, result)
print(rendered)

# Method 2: Render with template file
rendered = parser.render_template_file("document_summary.j2", result)
print(rendered)

# Method 3: Parse and render in one step
rendered = parser.render_data_file_to_template(
    "document.pdf", 
    "document_summary.j2",
    extra_context={'processing_date': '2025-07-02'}
)
print(rendered)

# Method 4: Simple template rendering (no document parsing)
simple_result = parser.render_simple_template_file(
    "simple_template.j2",
    context={'content': 'Hello World!'}
)
print(simple_result)
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

## Template Rendering

The Document Parser includes powerful Jinja2 template rendering capabilities for generating custom reports and outputs.

### Available Template Methods

```python
parser = DocumentParser({'template_dir': 'templates'})

# 1. Render with template string
rendered = parser.render_template(template_string, document_result, extra_context={})

# 2. Render with template file
rendered = parser.render_template_file(template_filename, document_result, extra_context={})

# 3. Parse file and render in one step
rendered = parser.render_data_file_to_template(file_path, template_filename, extra_context={})

# 4. Simple template rendering (no document required)
rendered = parser.render_simple_template(template_string, context={})
rendered = parser.render_simple_template_file(template_filename, context={})

# 5. Render and save to file
parser.render_data_file_to_template_with_save(file_path, template_filename, output_path, extra_context={})
```

### Template Context Variables

When rendering document templates, the following variables are available:

- `document_info`: Document metadata (filename, file_type, total_pages, file_size, etc.)
- `document`: Dictionary version of document_info for easier template access
- `pages`: List of document pages with content and metadata
- `total_words`: Total word count across all pages
- `total_chars`: Total character count across all pages
- `all_headings`: Combined list of all headings from all pages
- Any additional variables passed via `extra_context`

### Sample Templates

#### PDF/Document Summary Template (document_summary.j2)
```jinja2
# Document Summary: {{ document_info.filename }}

**File Details:**
- Type: {{ document_info.file_type | upper }}
- Pages: {{ document_info.total_pages }}
- Size: {{ "%.2f KB" | format(document_info.file_size / 1024) }}

**Content Analysis:**
- Total Words: {{ total_words }}
- Total Characters: {{ total_chars }}

{% if all_headings %}
**Headings Found:**
{% for heading in all_headings[:5] %}
- {{ heading.text }}
{% endfor %}
{% endif %}
```

#### CSV Report Template (csv_report.j2)
```jinja2
# CSV Data Summary: {{ document_info.filename }}

**File Details:**
- Size: {{ "%.2f KB" | format(document_info.file_size / 1024) }}
- Estimated Rows: {{ pages[0].content.text.split('\n')|length if pages }}

**Sample Data:**
```csv
{{ pages[0].content.text.split('\n')[:5] | join('\n') if pages }}
```
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
│   ├── __main__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── parser.py          # Main DocumentParser class
│   │   └── models.py          # Data models (DocumentResult, PageContent, etc.)
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── base.py           # Base parser interface
│   │   ├── pdf_parser.py     # PDF parsing (pdfplumber)
│   │   ├── docx_parser.py    # DOCX parsing (python-docx)
│   │   ├── excel_parser.py   # Excel parsing (pandas, openpyxl)
│   │   └── csv_parser.py     # CSV parsing (pandas)
│   ├── cli/
│   │   ├── __init__.py
│   │   └── main.py          # Command-line interface
│   └── utils/
│       ├── __init__.py
│       ├── exceptions.py    # Custom exceptions
│       ├── logging.py       # Logging utilities
│       └── templates.py     # Jinja2 template processing
├── sample_files/
│   ├── *.j2                 # Jinja2 template files
│   ├── sample-local-pdf.pdf # Sample PDF for testing
│   └── customers-100.csv    # Sample CSV for testing
├── output/                  # Generated reports and outputs
├── tests/
│   ├── conftest.py
│   ├── test_*.py           # Comprehensive test suite
├── csv_simple_test.py      # Simple CSV parsing example
├── pdf_simple_test.py      # Simple PDF parsing example
├── parsing_test.py         # Comprehensive parsing examples
├── requirements.txt
├── pyproject.toml
└── README.md
```

### Quick Start Examples

For quick testing, use the simple example files:

```bash
# Test CSV parsing with template rendering
python csv_simple_test.py

# Test PDF parsing with template rendering  
python pdf_simple_test.py

# Run comprehensive parsing tests
python parsing_test.py
```

## License

MIT License

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

> **💡 Pro Tip**: We recommend using [UV](https://github.com/astral-sh/uv) for faster dependency management and automatic virtual environment handling. UV is 10-100x faster than pip and automatically manages virtual environments.

### Method 1: Using UV (Recommended - Fast & Modern)

[UV](https://github.com/astral-sh/uv) is a fast Python package installer and dependency resolver with automatic virtual environment management. Install it first:

```bash
# Install uv (choose your method)
curl -LsSf https://astral.sh/uv/install.sh | sh  # Unix/macOS
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows PowerShell
pip install uv  # Alternative: install via pip
```

Then install the Document Parser:

```bash
# Install directly from git repository (creates virtual env automatically)
uv add git+https://github.com/yourusername/DataIntegrationPipeline.git

# Install from specific branch
uv add git+https://github.com/yourusername/DataIntegrationPipeline.git@main

# For development: clone and install in editable mode
git clone <repository-url>
cd DataIntegrationPipeline
uv sync  # Creates venv and installs all dependencies from pyproject.toml/uv.lock
uv add -e .  # Install in editable mode

# Run scripts directly with uv (no need to activate virtual env)
uv run python samples/csv_simple_test.py
uv run python -m document_parser parse file.pdf
```

### Method 2: Using UV for Local Development (Recommended)

UV automatically manages virtual environments and dependencies, making development setup effortless:

1. Clone the repository:
```bash
git clone <repository-url>
cd DataIntegrationPipeline
```

2. Use UV to manage dependencies:
```bash
# Sync dependencies (creates virtual environment automatically from pyproject.toml)
uv sync

# Or manually create venv and install (if needed)
uv venv
uv pip install -e .

# UV automatically uses the virtual environment for all commands
# No need to manually activate the environment!
```

3. Run commands with UV (automatic virtual environment activation):
```bash
# Run scripts directly with uv (virtual env activated automatically)
uv run python samples/csv_simple_test.py
uv run python -m document_parser parse file.pdf
uv run pytest  # Run tests

# Or manually activate venv if needed for other tools
# On Windows: .venv\Scripts\activate
# On Unix/macOS: source .venv/bin/activate
```

### Method 3: Traditional pip Installation

```bash
# Install directly from git repository
pip install git+https://github.com/jojodev-insight/DataIntegrationPipeline.git

# Install from specific branch
pip install git+https://github.com/jojodev-insight/DataIntegrationPipeline.git@master

# For local development
git clone <repository-url>
cd DataIntegrationPipeline
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

### Method 4: Add to pyproject.toml/requirements.txt

**For UV users (recommended):**

Add to your project's `pyproject.toml`:
```toml
[project]
dependencies = [
    "document-parser @ git+https://github.com/yourusername/DataIntegrationPipeline.git"
]

# Or for development dependencies
[tool.uv]
dev-dependencies = [
    "document-parser @ git+https://github.com/yourusername/DataIntegrationPipeline.git"
]

# For local development
[tool.uv]
dev-dependencies = [
    "document-parser @ file:///path/to/DataIntegrationPipeline"
]
```

**For traditional pip users:**

Add to your project's `pyproject.toml`:
```toml
[project]
dependencies = [
    "document-parser @ git+https://github.com/yourusername/DataIntegrationPipeline.git"
]
```

Or add to `requirements.txt`:
```txt
# Install from git repository
git+https://github.com/yourusername/DataIntegrationPipeline.git

# Or for local development
-e /path/to/DataIntegrationPipeline
```

Then install:
```bash
# With uv (recommended - automatically manages virtual environment)
uv sync

# With pip (manual virtual environment management)
pip install -r requirements.txt
```

### Verification

Test the installation:
```python
from document_parser import DocumentParser
parser = DocumentParser()
print("✅ Document Parser installed successfully!")
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
result = parser.parse_file("sample_files/sample-local-pdf.pdf")
print(result.to_json(pretty=True))

# Parse an Excel file
result = parser.parse_file("sample_files/sample-data.xlsx")
print(f"Sheets: {result.document_info.total_pages}")

# Parse a CSV file  
result = parser.parse_file("sample_files/customers-100.csv")
print(result.to_json(pretty=True))

# Parse a DOCX file
result = parser.parse_file("sample_files/sample-document.docx")
print(f"Pages: {result.document_info.total_pages}")

# Render parsed data with templates
# Method 1: Render with template string
template_string = "File: {{ document_info.filename }}, Pages: {{ document_info.total_pages }}"
rendered = parser.render_template(template_string, result)
print(rendered)

# Method 2: Render with template file
rendered = parser.render_template_file("document_summary.j2", result)
print(rendered)

# Method 3: Parse and render in one step (recommended)
csv_report = parser.render_data_file_to_template(
    "sample_files/customers-100.csv", 
    "csv_report.j2",
    extra_context={'processing_date': '2025-07-02'}
)
print(csv_report)

pdf_summary = parser.render_data_file_to_template(
    "sample_files/sample-local-pdf.pdf",
    "document_summary.j2",
    extra_context={'processing_date': '2025-07-02'}
)
print(pdf_summary)

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
```

## Sample Files and Templates

### Available Sample Scripts

The `samples/` directory contains simple, focused examples for each file type:

| Script | File Type | Sample File Required | Template Used |
|--------|-----------|---------------------|---------------|
| `csv_simple_test.py` | CSV | `customers-100.csv` | `csv_report.j2` |
| `pdf_simple_test.py` | PDF | `sample-local-pdf.pdf` | `document_summary.j2` |
| `excel_simple_test.py` | Excel | `sample-data.xlsx` | `document_summary.j2` |
| `docx_simple_test.py` | DOCX | `sample-document.docx` | `document_summary.j2` |

### Available Templates

The `sample_files/` directory includes several pre-built Jinja2 templates:

| Template | Purpose | Best For |
|----------|---------|----------|
| `document_summary.j2` | General document summary | PDF, DOCX, Excel files |
| `csv_report.j2` | Detailed CSV analysis | CSV files with data statistics |
| `csv_custom_report.j2` | Custom CSV report | CSV files with custom formatting |
| `document_content.j2` | Simple content display | Any file type |
| `simple_template.j2` | Basic text template | Simple text rendering |
| `title_message.j2` | Title and message | Basic notifications |

### Adding Your Own Sample Files

To use the sample scripts, add these files to the `sample_files/` directory:

1. **CSV File**: Any CSV with headers (e.g., `customers-100.csv`)
2. **PDF File**: Any readable PDF document (e.g., `sample-local-pdf.pdf`)
3. **Excel File**: Any .xlsx or .xls file (e.g., `sample-data.xlsx`)
4. **DOCX File**: Any Word document (e.g., `sample-document.docx`)

### Creating Custom Templates

Templates use standard Jinja2 syntax with access to document data:

```jinja2
# Custom Report: {{ document_info.filename }}

## File Information
- **Type**: {{ document_info.file_type | upper }}
- **Size**: {{ "%.2f KB" | format(document_info.file_size / 1024) }}
- **Pages/Sheets**: {{ document_info.total_pages }}

## Content Summary
{% if pages %}
{% for page in pages[:3] %}
### Page {{ page.page_number }}
{{ page.content.text[:200] }}...
{% endfor %}
{% endif %}

*Generated on {{ processing_date }}*
```

## Development

### Running Tests

```bash
# Using UV (recommended - automatic virtual environment)
uv run pytest tests/ -v --cov=document_parser

# Traditional method (activate virtual environment first)
pytest tests/ -v --cov=document_parser
```

### Code Formatting

```bash
# Using UV (recommended)
uv run black document_parser/ tests/
uv run flake8 document_parser/ tests/
uv run mypy document_parser/

# Traditional method (activate virtual environment first)
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
│   │   ├── document_summary.j2    # General document summary
│   │   ├── csv_report.j2          # CSV-specific report
│   │   ├── csv_custom_report.j2   # Custom CSV report
│   │   ├── document_content.j2    # Document content template
│   │   ├── simple_template.j2     # Simple text template
│   │   └── title_message.j2       # Title/message template
│   ├── sample-local-pdf.pdf # Sample PDF for testing
│   ├── customers-100.csv    # Sample CSV for testing
│   ├── sample-data.xlsx     # Sample Excel for testing (add your own)
│   └── sample-document.docx # Sample DOCX for testing (add your own)
├── samples/                 # Simple example scripts
│   ├── csv_simple_test.py   # CSV parsing example
│   ├── pdf_simple_test.py   # PDF parsing example
│   ├── excel_simple_test.py # Excel parsing example
│   └── docx_simple_test.py  # DOCX parsing example
├── output/                  # Generated reports and outputs
├── tests/
│   ├── conftest.py
│   ├── test_*.py           # Comprehensive test suite
│   ├── test_pdf_docx_parsers.py    # PDF and DOCX parser tests
│   └── test_excel_csv_parsers.py   # Excel and CSV parser tests
├── parsing_test.py         # Comprehensive parsing examples
├── requirements.txt
├── pyproject.toml
└── README.md
```

### Quick Start Examples

The project includes simple example files in the `samples/` folder for immediate testing:

```bash
# Using UV (recommended - no need to activate virtual environment)
uv run python samples/csv_simple_test.py
uv run python samples/pdf_simple_test.py
uv run python samples/excel_simple_test.py
uv run python samples/docx_simple_test.py
uv run python samples/combined_test.py

# Or traditional method (activate virtual environment first)
cd samples
python csv_simple_test.py
python pdf_simple_test.py

# Test Excel parsing with template rendering
python excel_simple_test.py

# Test DOCX parsing with template rendering
python docx_simple_test.py
```

For comprehensive testing and examples:
```bash
# Run comprehensive parsing tests with all file types
python parsing_test.py
```

#### Sample Files Required

Place the following sample files in the `sample_files/` directory:

- **CSV**: `customers-100.csv` (customer data)
- **PDF**: `sample-local-pdf.pdf` (any PDF document)
- **Excel**: `sample-data.xlsx` (spreadsheet with data)
- **DOCX**: `sample-document.docx` (Word document)

#### Example Usage Pattern

Each simple test follows the same pattern:
```python
from document_parser import DocumentParser

# Initialize parser with template directory
parser = DocumentParser({"template_dir": "../sample_files"})

# Parse file and render with template in one step
result = parser.render_data_file_to_template(
    file_path,
    "document_summary.j2",
    extra_context={
        "processing_date": "2025-07-02",
        "parser_version": "1.0.0"
    }
)

print(result)
```

## License

MIT License

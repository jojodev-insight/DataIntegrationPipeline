# Document Parser - Technical Documentation

## Overview

The Document Parser is a professional Python package designed to extract content from PDF and DOCX files and convert them into structured JSON format. It follows Python coding standards and best practices, including PEP 8 style guidelines, comprehensive type hints, and modular architecture.

## Architecture

### Package Structure

```
document_parser/
├── __init__.py              # Package entry point with delayed imports
├── __main__.py              # CLI module entry point
├── core/                    # Core functionality
│   ├── __init__.py
│   ├── models.py           # Data models using dataclasses
│   └── parser.py           # Main DocumentParser class
├── parsers/                 # Document parser implementations
│   ├── __init__.py
│   ├── base.py            # Abstract base parser
│   ├── pdf_parser.py      # PDF parsing implementation
│   └── docx_parser.py     # DOCX parsing implementation
├── cli/                    # Command-line interface
│   ├── __init__.py
│   └── main.py            # Click-based CLI implementation
└── utils/                  # Utility modules
    ├── __init__.py
    ├── exceptions.py      # Custom exception classes
    └── logging.py         # Logging configuration
```

### Design Patterns

1. **Strategy Pattern**: Different parsers (PDF, DOCX) implement the same interface
2. **Factory Pattern**: DocumentParser automatically selects appropriate parser
3. **Facade Pattern**: DocumentParser provides simplified interface to complex parsing logic
4. **Template Method Pattern**: BaseParser defines common parsing workflow

## Core Components

### Data Models (`core/models.py`)

All data models use Python dataclasses for clean, typed data structures:

- `HeadingInfo`: Represents document headings with level and text
- `PageContent`: Contains extracted text, paragraphs, and headings
- `PageMetadata`: Stores statistics like word and character counts
- `PageResult`: Complete page information combining content and metadata
- `DocumentInfo`: Document-level metadata (filename, type, size, etc.)
- `DocumentResult`: Final result containing document info and all pages

### Parser Architecture (`parsers/`)

#### Base Parser (`base.py`)
- Abstract base class defining parser interface
- Common metadata calculation methods
- Enforces consistent API across different document types

#### PDF Parser (`pdf_parser.py`)
- Uses `pdfplumber` library for robust PDF text extraction
- Handles password-protected documents
- Implements basic heading detection using heuristics
- Provides page-by-page processing

#### DOCX Parser (`docx_parser.py`)
- Uses `python-docx` library for Word document processing
- Handles document structure (headings, paragraphs)
- Creates logical pages since DOCX doesn't have explicit page breaks
- Preserves formatting information where possible

### Error Handling (`utils/exceptions.py`)

Comprehensive exception hierarchy:
- `DocumentParsingError`: Base exception for all parsing errors
- `UnsupportedFileTypeError`: Unsupported file format
- `CorruptedFileError`: Damaged or unreadable files
- `PasswordProtectedError`: Password-required documents
- `FileNotFoundError`: Missing files
- `InvalidConfigurationError`: Configuration problems

### Command-Line Interface (`cli/main.py`)

Built with Click framework:
- `parse`: Main command for document parsing
- `info`: Display supported file types and usage examples
- Supports single and batch file processing
- Configurable output formats (stdout, file, directory)
- Verbose logging and error handling

## JSON Output Schema

The parser produces consistent JSON output regardless of input format:

```json
{
  "document_info": {
    "filename": "document.pdf",
    "file_type": "pdf",
    "total_pages": 3,
    "created_at": "2025-06-30T18:00:00Z",
    "file_size": 1024000
  },
  "pages": [
    {
      "page_number": 1,
      "content": {
        "text": "Full page text content...",
        "paragraphs": [
          "First paragraph text...",
          "Second paragraph text..."
        ],
        "headings": [
          {
            "level": 1,
            "text": "Chapter Title"
          }
        ]
      },
      "metadata": {
        "word_count": 245,
        "char_count": 1450
      }
    }
  ]
}
```

## Quality Assurance

### Testing Strategy

1. **Unit Tests**: Comprehensive test coverage for all components
2. **Integration Tests**: End-to-end testing of parsing workflows
3. **Mocking**: External dependencies mocked for reliable testing
4. **Fixtures**: Reusable test data and temporary file handling

### Code Quality Tools

1. **Black**: Code formatting (PEP 8 compliance)
2. **Flake8**: Linting and style checking
3. **MyPy**: Static type checking
4. **Pytest**: Testing framework with coverage reporting

### Continuous Integration

GitHub Actions workflow includes:
- Multi-Python version testing (3.8-3.11)
- Security scanning with Bandit and Safety
- Code quality checks
- Automated package building

## Performance Considerations

### Memory Management
- Streaming processing for large files
- Lazy loading of parser modules
- Efficient text processing algorithms

### Scalability
- Page-by-page processing prevents memory overload
- Support for batch file processing
- Configurable processing options

### Error Recovery
- Graceful handling of corrupted files
- Continued processing when individual files fail
- Detailed error reporting and logging

## Extension Points

### Adding New Document Types

1. Create new parser class inheriting from `BaseParser`
2. Implement required methods: `parse()` and `supports_file_type()`
3. Register parser in `DocumentParser.__init__()`
4. Add appropriate tests

### Custom Output Formats

1. Extend `DocumentResult` with new serialization methods
2. Add CLI options for new formats
3. Implement format-specific writers

### Advanced Features

1. **OCR Support**: Add image-to-text processing
2. **Table Extraction**: Enhanced structured data extraction
3. **Metadata Enrichment**: Additional document properties
4. **Language Detection**: Automatic language identification

## Configuration Options

The parser supports configuration through:
- Constructor parameters
- Environment variables
- Configuration files (future enhancement)
- CLI arguments

## Dependencies

### Core Dependencies
- `pdfplumber`: PDF text extraction
- `python-docx`: DOCX document processing
- `click`: CLI framework
- `pydantic`: Data validation (future use)

### Development Dependencies
- `pytest`: Testing framework
- `pytest-cov`: Coverage reporting
- `black`: Code formatting
- `flake8`: Linting
- `mypy`: Type checking

## Installation and Usage

### Development Setup

```bash
# Clone repository
git clone <repository-url>
cd DataIntegrationPipeline

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Run tests
pytest tests/ -v --cov=document_parser

# Run quality checks
flake8 document_parser/ tests/
black document_parser/ tests/
mypy document_parser/
```

### Production Usage

```python
from document_parser import DocumentParser

# Initialize parser
parser = DocumentParser()

# Parse document
result = parser.parse_file("document.pdf")

# Access structured data
print(f"Pages: {result.document_info.total_pages}")
for page in result.pages:
    print(f"Page {page.page_number}: {page.metadata.word_count} words")

# Export to JSON
result.save_to_file("output.json", pretty=True)
```

## Future Enhancements

1. **Performance Optimization**: Parallel processing, caching
2. **Advanced Text Processing**: NLP integration, entity extraction
3. **Cloud Integration**: S3, Azure Blob, Google Cloud support
4. **Web Interface**: REST API, web dashboard
5. **Database Integration**: Direct database output
6. **Machine Learning**: Intelligent document classification

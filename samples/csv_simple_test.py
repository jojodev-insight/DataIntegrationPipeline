import sys
from pathlib import Path

# Add parent directory (project root) to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from document_parser import DocumentParser

# Initialize parser
parser = DocumentParser({"template_dir": "sample_files"})

# Parse CSV and render template
csv_path = "sample_files/customers-100.csv"
result = parser.render_data_file_to_template(
    csv_path,
    "csv_report.j2",
    extra_context={"processing_date": "2025-07-02", "parser_version": "1.0.0"},
)

print(result)

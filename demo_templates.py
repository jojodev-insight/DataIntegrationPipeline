"""
Demonstration script for using Jinja2 templates with the document parser.

This script shows how to parse documents and render them using Jinja2 templates
to create formatted reports and summaries.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from document_parser import DocumentParser
from document_parser.utils.exceptions import DocumentParsingError


def demo_template_rendering():
    """Demonstrate template rendering with parsed document data."""
    print("=== Jinja2 Template Rendering Demo ===")
    
    # Initialize parser with template directory
    config = {'template_dir': 'sample_files'}
    parser = DocumentParser(config)
    
    # Sample template strings for demonstration
    simple_template = """
Document: {{ document_info.filename }}
Type: {{ document_info.file_type | upper }}
Pages: {{ document_info.total_pages }}
Total Words: {{ total_words }}
""".strip()
    
    detailed_template = """
# {{ document_info.filename }} Analysis

**File Information:**
- Type: {{ document_info.file_type | upper }}
- Size: {{ "%.2f KB" | format(document_info.file_size / 1024) }}
- Pages/Sheets: {{ document_info.total_pages }}
- Created: {{ document_info.created_at.strftime('%Y-%m-%d %H:%M:%S') }}

{% if document_info.file_type in ['pdf', 'docx'] %}
**Content Statistics:**
- Total Words: {{ total_words }}
- Total Characters: {{ total_chars }}
- Average Words per Page: {{ "%.1f" | format(total_words / document_info.total_pages) if document_info.total_pages > 0 else 0 }}

{% if all_headings %}
**Document Structure:**
{% for heading in all_headings %}
{{ "  " * (heading.level - 1) }}- {{ heading.text }}
{% endfor %}
{% endif %}

{% elif document_info.file_type in ['xlsx', 'xls', 'csv'] %}
**Data Statistics:**
- Total Rows: {{ total_rows }}
- Total Columns: {{ total_columns }}
- Estimated Cells: {{ total_cells }}

{% endif %}
**Page/Sheet Breakdown:**
{% for page in pages %}
{{ loop.index }}. {% if document_info.file_type in ['xlsx', 'xls'] %}Sheet {{ page.page_number }}{% else %}Page {{ page.page_number }}{% endif %}
   - Content length: {{ page.metadata.char_count }} characters
   {% if page.content.text %}
   - Preview: {{ page.content.text[:100] | replace('\\n', ' ') }}{% if page.content.text | length > 100 %}...{% endif %}
   {% endif %}

{% endfor %}
""".strip()
    
    # Create sample files for demonstration
    create_demo_files()
    
    # Sample files to process
    sample_files = [
        "sample_files/sample_products.xlsx",
        "sample_files/sample_employees.csv",
    ]
    
    # Add any existing PDF/DOCX files
    for ext in ['.pdf', '.docx']:
        sample_files.extend([
            f for f in Path('sample_files').glob(f'*{ext}') 
            if f.exists()
        ])
    
    for file_path in sample_files:
        if not os.path.exists(file_path):
            continue
            
        try:
            print(f"\n{'='*50}")
            print(f"Processing: {file_path}")
            print('='*50)
            
            # Parse the document
            result = parser.parse_file(str(file_path))
            
            # Render with simple template
            print("\n--- Simple Template Output ---")
            simple_output = parser.render_template(simple_template, result)
            print(simple_output)
            
            # Render with detailed template
            print("\n--- Detailed Template Output ---")
            detailed_output = parser.render_template(
                detailed_template, 
                result,
                extra_context={
                    'processing_date': '2025-07-02',
                    'parser_version': '1.0.0'
                }
            )
            print(detailed_output)
            
            # Render using template files if they exist
            template_files = ['document_summary.j2', 'document_report.html.j2']
            for template_file in template_files:
                template_path = Path('sample_files') / template_file
                if template_path.exists():
                    print(f"\n--- Template File: {template_file} ---")
                    try:
                        file_output = parser.render_template_file(
                            template_file,
                            result,
                            extra_context={
                                'processing_date': '2025-07-02',
                                'parser_version': '1.0.0',
                                'notes': 'This is a demonstration of template rendering.'
                            }
                        )
                        
                        # Save output to file
                        output_ext = '.html' if template_file.endswith('.html.j2') else '.md'
                        output_filename = f"rendered_{Path(file_path).stem}_{template_file.replace('.j2', '')}{output_ext}"
                        output_path = Path('output') / output_filename
                        
                        with open(output_path, 'w', encoding='utf-8') as f:
                            f.write(file_output)
                        
                        print(f"✅ Rendered template saved to: {output_path}")
                        
                        # Show preview of file template output
                        preview = file_output[:300] + "..." if len(file_output) > 300 else file_output
                        print(f"Preview:\n{preview}")
                        
                    except Exception as e:
                        print(f"❌ Error rendering template file: {e}")
                        
        except DocumentParsingError as e:
            print(f"❌ Parsing error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")


def demo_multiple_templates():
    """Demonstrate rendering multiple templates at once."""
    print("\n=== Multiple Template Rendering Demo ===")
    
    parser = DocumentParser({'template_dir': 'sample_files'})
    
    # Find first available file
    sample_files = [
        "sample_files/sample_products.xlsx",
        "sample_files/sample_employees.csv",
    ]
    
    sample_file = None
    for file_path in sample_files:
        if os.path.exists(file_path):
            sample_file = file_path
            break
    
    if not sample_file:
        print("No sample files found for demonstration")
        return
    
    # Define multiple templates
    templates = [
        {
            "name": "summary",
            "string": "{{ document_info.filename }}: {{ document_info.total_pages }} pages, {{ total_words }} words"
        },
        {
            "name": "statistics",
            "string": """
Stats for {{ document_info.filename }}:
- Type: {{ document_info.file_type }}
- Size: {{ document_info.file_size }} bytes
- Pages: {{ document_info.total_pages }}
{% if document_info.file_type in ['xlsx', 'xls', 'csv'] %}
- Rows: {{ total_rows }}
- Columns: {{ total_columns }}
{% endif %}
""".strip()
        }
    ]
    
    # Add file-based template if available
    if os.path.exists('sample_files/document_summary.j2'):
        templates.append({
            "name": "detailed_report",
            "file": "document_summary.j2"
        })
    
    try:
        print(f"Processing: {sample_file}")
        results = parser.parse_and_render_multiple(
            sample_file,
            templates,
            extra_context={'processing_date': '2025-07-02'}
        )
        
        for name, output in results.items():
            print(f"\n--- Template: {name} ---")
            print(output[:300] + "..." if len(output) > 300 else output)
            
    except Exception as e:
        print(f"❌ Error: {e}")


def create_demo_files():
    """Create demo files for testing."""
    try:
        import pandas as pd
        
        # Create directories
        os.makedirs('sample_files', exist_ok=True)
        os.makedirs('output', exist_ok=True)
        
        # Create sample Excel file
        if not os.path.exists('sample_files/sample_products.xlsx'):
            excel_data = {
                'Product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones'],
                'Price': [999.99, 25.50, 75.00, 299.99, 149.99],
                'Stock': [10, 100, 50, 25, 30],
                'Category': ['Electronics', 'Accessories', 'Accessories', 'Electronics', 'Audio']
            }
            df_excel = pd.DataFrame(excel_data)
            df_excel.to_excel('sample_files/sample_products.xlsx', index=False, sheet_name='Products')
            print("📊 Created sample Excel file")
        
        # Create sample CSV file
        if not os.path.exists('sample_files/sample_employees.csv'):
            csv_data = {
                'Employee': ['Alice Johnson', 'Bob Smith', 'Carol Davis', 'David Wilson'],
                'Department': ['Engineering', 'Marketing', 'HR', 'Engineering'],
                'Salary': [75000, 65000, 70000, 80000],
                'Years': [3, 5, 8, 2]
            }
            df_csv = pd.DataFrame(csv_data)
            df_csv.to_csv('sample_files/sample_employees.csv', index=False)
            print("📈 Created sample CSV file")
            
    except ImportError:
        print("⚠️  pandas not available - install requirements.txt to create sample files")


def main():
    """Main function to run the template demonstration."""
    print("Document Parser - Jinja2 Template Rendering Demo")
    print("=" * 60)
    
    # Ensure sample files exist
    create_demo_files()
    
    # Run demonstrations
    demo_template_rendering()
    demo_multiple_templates()
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("\nTemplate files created:")
    print("- sample_files/document_summary.j2 (Markdown report)")
    print("- sample_files/document_report.html.j2 (HTML report)")
    print("\nTo use these templates:")
    print("1. parser.render_template_file('document_summary.j2', result)")
    print("2. parser.render_template_file('document_report.html.j2', result)")


if __name__ == "__main__":
    main()

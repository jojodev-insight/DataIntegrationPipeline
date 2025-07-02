"""
Example usage script for the document parser.

This script demonstrates how to use the document parser both as a library
and via command line interface.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from document_parser import DocumentParser
from document_parser.utils.exceptions import DocumentParsingError


def example_library_usage():
    """Demonstrate using the parser as a library."""
    print("=== Library Usage Example ===")
    
    # Initialize parser
    parser = DocumentParser()
    
    # Show supported file types
    extensions = parser.get_supported_extensions()
    print(f"Supported file types: {', '.join(extensions)}")
    
    # Example file paths (you would replace these with real files)
    sample_files = [
        "sample_files/document.pdf",
        "sample_files/report.docx",
        "sample_files/data.xlsx",
        "sample_files/sales.csv",
    ]
    
    for file_path in sample_files:
        if os.path.exists(file_path):
            try:
                print(f"\nParsing: {file_path}")
                
                # Check if file is supported
                if not parser.supports_file(file_path):
                    print(f"  ❌ Unsupported file type")
                    continue
                
                # Parse the file
                result = parser.parse_file(file_path)
                
                # Display results
                print(f"  ✅ Successfully parsed")
                print(f"  📄 Pages: {result.document_info.total_pages}")
                print(f"  📝 File type: {result.document_info.file_type}")
                print(f"  📏 File size: {result.document_info.file_size} bytes")
                
                # Show first page content (truncated)
                if result.pages:
                    first_page = result.pages[0]
                    text_preview = first_page.content.text[:100] + "..." if len(first_page.content.text) > 100 else first_page.content.text
                    print(f"  📖 First page preview: {text_preview}")
                    print(f"  🔢 Word count: {first_page.metadata.word_count}")
                
                # Save as JSON
                output_path = f"output_{Path(file_path).stem}.json"
                result.save_to_file(output_path, pretty=True)
                print(f"  💾 Saved to: {output_path}")
                
            except DocumentParsingError as e:
                print(f"  ❌ Parsing error: {e}")
            except Exception as e:
                print(f"  ❌ Unexpected error: {e}")
        else:
            print(f"\nFile not found: {file_path}")
            print("  💡 Create sample files in the 'sample_files/' directory to test")


def example_cli_usage():
    """Show CLI usage examples."""
    print("\n=== CLI Usage Examples ===")
    
    print("To use the command-line interface:")
    print()
    print("1. Parse a single file:")
    print("   python -m document_parser parse document.pdf --output result.json")
    print()
    print("2. Parse multiple files with pretty output:")
    print("   python -m document_parser parse *.pdf *.docx *.xlsx *.csv --output-dir results/ --pretty")
    print()
    print("3. Show information about supported formats:")
    print("   python -m document_parser info")
    print()
    print("4. Enable verbose logging:")
    print("   python -m document_parser --verbose parse document.pdf")


def create_sample_directory():
    """Create sample directory structure."""
    print("\n=== Setup ===")
    
    # Create directories
    dirs_to_create = ["sample_files", "output"]
    
    for dir_name in dirs_to_create:
        os.makedirs(dir_name, exist_ok=True)
        print(f"📁 Created directory: {dir_name}/")
    
    print("\n💡 Add your PDF, DOCX, Excel, and CSV files to the 'sample_files/' directory to test the parser")


def create_sample_files():
    """Create sample Excel and CSV files for testing."""
    print("\n=== Creating Sample Files ===")
    
    try:
        import pandas as pd
        
        # Create sample Excel file
        excel_data = {
            'Product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones'],
            'Price': [999.99, 25.50, 75.00, 299.99, 149.99],
            'Stock': [10, 100, 50, 25, 30],
            'Category': ['Electronics', 'Accessories', 'Accessories', 'Electronics', 'Audio']
        }
        df_excel = pd.DataFrame(excel_data)
        excel_path = "sample_files/sample_products.xlsx"
        df_excel.to_excel(excel_path, index=False, sheet_name='Products')
        print(f"📊 Created sample Excel file: {excel_path}")
        
        # Create sample CSV file
        csv_data = {
            'Employee': ['Alice Johnson', 'Bob Smith', 'Carol Davis', 'David Wilson'],
            'Department': ['Engineering', 'Marketing', 'HR', 'Engineering'],
            'Salary': [75000, 65000, 70000, 80000],
            'Years': [3, 5, 8, 2]
        }
        df_csv = pd.DataFrame(csv_data)
        csv_path = "sample_files/sample_employees.csv"
        df_csv.to_csv(csv_path, index=False)
        print(f"📈 Created sample CSV file: {csv_path}")
        
    except ImportError:
        print("⚠️  pandas not available - install requirements.txt to create sample files")
    except Exception as e:
        print(f"⚠️  Error creating sample files: {e}")


def main():
    """Main function to run examples."""
    print("Document Parser - Example Usage")
    print("=" * 50)
    
    # Create sample directory structure
    create_sample_directory()
    
    # Create sample files
    create_sample_files()
    
    # Demonstrate library usage
    example_library_usage()
    
    # Show CLI examples
    example_cli_usage()
    
    print("\n" + "=" * 50)
    print("Example completed!")


if __name__ == "__main__":
    main()

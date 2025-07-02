"""
Simple template binding demonstration.

This script shows how to use the simple placeholder template 
to bind parsed document data.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from document_parser import DocumentParser


def demo_simple_template():
    """Demonstrate simple template binding."""
    print("=== Simple Template Binding Demo ===")
    
    # Initialize parser with template directory
    config = {'template_dir': 'sample_files'}
    parser = DocumentParser(config)
    
    # Example 1: Bind simple text
    print("\n1. Binding simple text:")
    result = parser.render_template(
        template_name='simple_template.j2',
        content="Hello, World! This is a simple template binding example."
    )
    print(f"Result: {result}")
    
    # Example 2: Bind document data (mock)
    print("\n2. Binding document summary:")
    document_summary = """
Document: sample.pdf
Pages: 5
Words: 1,250
Status: Successfully parsed
"""
    result = parser.render_template(
        template_name='simple_template.j2',
        content=document_summary.strip()
    )
    print(f"Result:\n{result}")
    
    # Example 3: Bind JSON-like content
    print("\n3. Binding structured content:")
    structured_content = """
DOCUMENT ANALYSIS REPORT
========================
File: report.docx
Type: Word Document
Size: 45.2 KB
Content: 
  - 3 chapters
  - 12 sections
  - 8 tables
  - 15 images
Analysis complete ✓
"""
    result = parser.render_template(
        template_name='simple_template.j2',
        content=structured_content.strip()
    )
    print(f"Result:\n{result}")
    
    print("\n" + "="*50)
    print("Demo completed!")
    print("\nThe simple_template.j2 file contains just: {{ content }}")
    print("You can replace 'content' with any variable name you want.")
    print("For example, change it to {{ text }} and use text='your data'")


if __name__ == "__main__":
    demo_simple_template()

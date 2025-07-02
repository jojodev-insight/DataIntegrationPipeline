import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from document_parser import DocumentParser

parser = DocumentParser({"template_dir": "sample_files"})

# Method 1: Simple template string (easiest way)
# print("\n1. Simple template string:")
# result = parser.render_simple_template(
#     template_string="{{ content }}",
#     context={'content': "Hello, World! This is a simple template binding example."}
# )
# print(f"Result: {result}")

# # Method 2: Simple template file (using the simple_template.j2 file)
# print("\n2. Simple template file:")
# result = parser.render_simple_template_file(
#     template_filename='simple_template.j2',
#     context={'content': "Hello, World! This is a simple template binding example."}
# )
# print(f"Result: {result}")

# # Method 3: Using other simple templates
# print("\n3. Title-message template:")
# result = parser.render_simple_template_file(
#     template_filename='title_message.j2',
#     context={
#         'title': "DOCUMENT PARSER",
#         'message': "Successfully processed your file!"
#     }
# )
# print(f"Result: {result}")

# Method 4: Document content template
print("\n4. Document content template:")
result = parser.render_simple_template_file(
    template_filename="document_content.j2",
    context={
        "filename": "sample_document.pdf",
        "text": "This is the extracted content from the document...",
    },
)
print(f"Result: {result}")

# Method 5: JSON output template
# print("\n5. JSON output template:")
# sample_data = {
#     "document": "report.pdf",
#     "pages": 5,
#     "words": 1250,
#     "status": "success"
# }
# result = parser.render_simple_template_file(
#     template_filename='json_output.j2',
#     context={'data': sample_data}
# )
# print(f"Result: {result}")

# Method 6: Test loading and parsing the sample PDF file
print("\n6. Loading and parsing sample PDF:")
try:
    pdf_path = "sample_files/sample-local-pdf.pdf"

    # Check if file exists
    import os

    if os.path.exists(pdf_path):
        print(f"✅ Found PDF file: {pdf_path}")

        # Parse the PDF file
        document_result = parser.parse_file(pdf_path)

        print("📄 Document Info:")
        print(f"   - Filename: {document_result.document_info.filename}")
        print(f"   - File Type: {document_result.document_info.file_type}")
        print(f"   - Total Pages: {document_result.document_info.total_pages}")
        print(f"   - File Size: {document_result.document_info.file_size} bytes")

        # Show content from first page
        if document_result.pages:
            first_page = document_result.pages[0]
            print("\n📖 First Page Content:")
            print(f"   - Words: {first_page.metadata.word_count}")
            print(f"   - Characters: {first_page.metadata.char_count}")

            # Show text preview (first 200 characters)
            text_preview = (
                first_page.content.text[:200]
                if first_page.content.text
                else "No text extracted"
            )
            print(f"   - Text Preview: {text_preview}...")

            # Show headings if any
            if first_page.content.headings:
                print(
                    f"   - Headings on first page: {len(first_page.content.headings)}"
                )
                for heading in first_page.content.headings[:3]:  # Show first 3 headings
                    print(f"     * Level {heading.level}: {heading.text}")

        # Test rendering with a simple template
        print("\n🎨 Template Rendering Test:")
        simple_template = """
PDF Document Analysis
=====================
File: {{ document_info.filename }}
Pages: {{ document_info.total_pages }}
Total Words: {{ total_words }}
Total Characters: {{ total_chars }}

{% if all_headings %}
Headings Found:
{% for heading in all_headings[:5] %}
  {{ loop.index }}. {{ heading.text }}
{% endfor %}
{% if all_headings|length > 5 %}
  ... and {{ all_headings|length - 5 }} more headings
{% endif %}
{% endif %}

First Page Preview:
{{ pages[0].content.text[:300] if pages and pages[0].content.text else "No text content" }}...
""".strip()

        rendered = parser.render_template(
            simple_template,
            document_result,
            extra_context={"analysis_date": "2025-07-02"},
        )
        print(rendered)

        # Test with template file if document_summary.j2 exists
        print("\n📋 Testing with document_summary.j2 template:")
        try:
            summary_result = parser.render_data_file_to_template(
                pdf_path,
                "document_summary.j2",
                extra_context={
                    "processing_date": "2025-07-02",
                    "parser_version": "1.0.0",
                    "notes": "Parsed using the document parser test script",
                },
            )

            # Save the result to a file
            output_path = "output/pdf_summary_report.md"
            os.makedirs("output", exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(summary_result)

            print(f"✅ Summary report generated and saved to: {output_path}")
            print("📝 Preview of summary (first 300 chars):")
            print(summary_result[:300] + "...")

        except Exception as e:
            print(f"❌ Error with document_summary.j2 template: {e}")

    else:
        print(f"❌ PDF file not found: {pdf_path}")
        print(
            "💡 Please place a PDF file named 'sample-local-pdf.pdf' in the 'sample_files/' directory"
        )

except Exception as e:
    print(f"❌ Error processing PDF: {e}")
    import traceback

    traceback.print_exc()

# Method 7: Test loading and parsing CSV file
print("\n7. Loading and parsing sample CSV:")
try:
    csv_path = "sample_files/customers-100.csv"

    # Check if file exists
    import os

    if os.path.exists(csv_path):
        print(f"✅ Found CSV file: {csv_path}")

        # Parse the CSV file
        document_result = parser.parse_file(csv_path)

        print("📊 CSV Document Info:")
        print(f"   - Filename: {document_result.document_info.filename}")
        print(f"   - File Type: {document_result.document_info.file_type}")
        print(f"   - Total Sections: {document_result.document_info.total_pages}")
        print(f"   - File Size: {document_result.document_info.file_size} bytes")

        # Show content from first section
        if document_result.pages:
            first_section = document_result.pages[0]
            print("\n📈 CSV Data Analysis:")
            print(f"   - Estimated Rows: {first_section.metadata.word_count}")
            print(f"   - Total Characters: {first_section.metadata.char_count}")

            # Show CSV preview (first 300 characters)
            csv_preview = (
                first_section.content.text[:300]
                if first_section.content.text
                else "No data extracted"
            )
            print(f"   - Data Preview:\n{csv_preview}...")

            # Count estimated columns from first row
            if first_section.content.text:
                lines = first_section.content.text.split("\n")
                if lines:
                    first_row = lines[0]
                    estimated_columns = len(first_row.split(","))
                    print(f"   - Estimated Columns: {estimated_columns}")

                    # Show column headers if available
                    print(f"   - Column Headers: {first_row}")

        # Test rendering with a CSV-specific template from file
        print("\n📊 CSV Template Rendering Test (using csv_report.j2):")
        try:
            rendered = parser.render_data_file_to_template(
                csv_path, "csv_report.j2", extra_context={"analysis_date": "2025-07-02"}
            )
            print(rendered)
        except Exception as e:
            print(f"❌ Error rendering csv_report.j2 template: {e}")

        # Test with document_summary.j2 template for CSV
        print("\n📋 Testing CSV with document_summary.j2 template:")
        try:
            summary_result = parser.render_data_file_to_template(
                csv_path,
                "document_summary.j2",
                extra_context={
                    "processing_date": "2025-07-02",
                    "parser_version": "1.0.0",
                    "notes": "CSV file parsed using the document parser test script",
                },
            )

            # Save the result to a file
            output_path = "output/csv_summary_report.md"
            os.makedirs("output", exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(summary_result)

            print(f"✅ CSV summary report generated and saved to: {output_path}")
            print("📝 Preview of CSV summary (first 300 chars):")
            print(summary_result[:300] + "...")

        except Exception as e:
            print(f"❌ Error with document_summary.j2 template for CSV: {e}")

        # Test creating a custom CSV report from template file
        print("\n📊 Creating custom CSV report (using csv_custom_report.j2):")
        try:
            custom_result = parser.render_data_file_to_template(
                csv_path,
                "csv_custom_report.j2",
                extra_context={
                    "processing_date": "2025-07-02",
                    "total_rows": first_section.metadata.word_count,
                    "notes": "This CSV file contains customer data with multiple columns.",
                },
            )

            # Save custom report
            custom_output_path = "output/csv_custom_report.md"
            with open(custom_output_path, "w", encoding="utf-8") as f:
                f.write(custom_result)

            print(f"✅ Custom CSV report saved to: {custom_output_path}")
            print("📄 Custom report preview:")
            print(custom_result[:400] + "...")

        except Exception as e:
            print(f"❌ Error creating custom CSV report: {e}")

        # Test with dedicated CSV template
        print("\n📊 Testing with dedicated csv_report.j2 template:")
        try:
            csv_template_result = parser.render_data_file_to_template(
                csv_path,
                "csv_report.j2",
                extra_context={
                    "processing_date": "2025-07-02",
                    "parser_version": "1.0.0",
                },
            )

            # Save the result
            csv_template_output = "output/csv_template_report.md"
            with open(csv_template_output, "w", encoding="utf-8") as f:
                f.write(csv_template_result)

            print(f"✅ CSV template report saved to: {csv_template_output}")
            print("📊 Template report preview:")
            print(csv_template_result[:400] + "...")

        except Exception as e:
            print(f"❌ Error with csv_report.j2 template: {e}")

    else:
        print(f"❌ CSV file not found: {csv_path}")
        print(
            "💡 Please place a CSV file named 'customers-100.csv' in the 'sample_files/' directory"
        )

except Exception as e:
    print(f"❌ Error processing CSV: {e}")
    import traceback

    traceback.print_exc()

import sys
from pathlib import Path

# Add parent directory (project root) to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from document_parser import DocumentParser


def test_all_formats():
    """Test all supported document formats with template rendering."""

    # Initialize parser
    parser = DocumentParser({"template_dir": "sample_files"})

    # Define test files and their corresponding templates
    test_cases = [
        {
            "name": "CSV",
            "file_path": "sample_files/customers-100.csv",
            "template": "csv_report.j2",
            "icon": "📊",
        },
        {
            "name": "PDF",
            "file_path": "sample_files/sample-local-pdf.pdf",
            "template": "document_summary.j2",
            "icon": "📄",
        },
        {
            "name": "Excel",
            "file_path": "sample_files/sample-data.xlsx",
            "template": "document_summary.j2",
            "icon": "📈",
        },
        {
            "name": "DOCX",
            "file_path": "sample_files/sample-document.docx",
            "template": "document_summary.j2",
            "icon": "📝",
        },
    ]

    print("🚀 Document Parser - All Formats Test")
    print("=" * 50)

    successful_tests = 0
    total_tests = len(test_cases)

    for test_case in test_cases:
        name = test_case["name"]
        file_path = test_case["file_path"]
        template = test_case["template"]
        icon = test_case["icon"]

        print(f"\n{icon} Testing {name} format...")
        print(f"   File: {file_path}")
        print(f"   Template: {template}")

        try:
            # Check if file exists
            import os

            if not os.path.exists(file_path):
                print(f"   ⚠️  File not found: {file_path}")
                print(
                    f"   💡 Please add a sample {name.lower()} file to the sample_files directory"
                )
                continue

            # Parse and render
            result = parser.render_data_file_to_template(
                file_path,
                template,
                extra_context={
                    "processing_date": "2025-07-02",
                    "parser_version": "1.0.0",
                    "test_run": f"{name} format test",
                },
            )

            # Display results
            print(f"   ✅ Successfully processed {name} file")
            print(f"   📝 Generated report ({len(result)} characters)")

            # Show preview of rendered output
            preview = result[:200] + "..." if len(result) > 200 else result
            print(f"   🔍 Preview:")
            for line in preview.split("\n")[:3]:
                if line.strip():
                    print(f"      {line}")

            successful_tests += 1

        except Exception as e:
            print(f"   ❌ Error processing {name}: {str(e)}")
            print(f"      Type: {type(e).__name__}")

    # Summary
    print("\n" + "=" * 50)
    print(f"📋 Test Summary:")
    print(f"   ✅ Successful: {successful_tests}/{total_tests}")
    print(f"   ❌ Failed: {total_tests - successful_tests}/{total_tests}")

    if successful_tests == total_tests:
        print("   🎉 All tests passed!")
    elif successful_tests > 0:
        print("   ⚠️  Some tests passed, check missing files above")
    else:
        print("   🚨 All tests failed, check configuration and file paths")


def test_template_variations():
    """Test different template rendering approaches."""

    print("\n🎨 Template Variations Test")
    print("=" * 50)

    parser = DocumentParser({"template_dir": "sample_files"})

    # Test simple template rendering (no document required)
    print("\n🔧 Testing simple template rendering...")
    try:
        simple_result = parser.render_simple_template_file(
            "simple_template.j2", context={"content": "Hello from combined test!"}
        )
        print(f"   ✅ Simple template: {simple_result.strip()}")
    except Exception as e:
        print(f"   ❌ Simple template error: {e}")

    # Test title/message template
    print("\n📢 Testing title/message template...")
    try:
        title_result = parser.render_simple_template_file(
            "title_message.j2",
            context={
                "title": "COMBINED TEST RESULTS",
                "message": "All document formats tested successfully!",
            },
        )
        print(f"   ✅ Title template: {title_result.strip()}")
    except Exception as e:
        print(f"   ❌ Title template error: {e}")


def main():
    """Main function to run all combined tests."""

    print("🧪 Document Parser - Combined Test Suite")
    print("Testing all sample files and templates together")
    print("Date: 2025-07-02")

    try:
        # Run format tests
        test_all_formats()

        # Run template variation tests
        test_template_variations()

        print("\n🏁 Combined test suite completed!")

    except Exception as e:
        print(f"\n💥 Unexpected error in combined test: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()

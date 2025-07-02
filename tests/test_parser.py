"""
Tests for the core DocumentParser class.
"""

import pytest
import os
from unittest.mock import Mock, patch

from document_parser.core.parser import DocumentParser
from document_parser.utils.exceptions import (
    UnsupportedFileTypeError,
    FileNotFoundError as CustomFileNotFoundError,
)


class TestDocumentParser:
    """Test cases for DocumentParser class."""

    def test_init(self):
        """Test parser initialization."""
        parser = DocumentParser()
        assert parser is not None
        assert len(parser._parsers) == 4  # PDF, DOCX, Excel, and CSV parsers

    def test_init_with_config(self):
        """Test parser initialization with config."""
        config = {"some_option": "value"}
        parser = DocumentParser(config)
        assert parser.config == config

    def test_supports_file_pdf(self):
        """Test file support detection for PDF."""
        parser = DocumentParser()
        assert parser.supports_file("test.pdf") is True
        assert parser.supports_file("test.PDF") is True

    def test_supports_file_docx(self):
        """Test file support detection for DOCX."""
        parser = DocumentParser()
        assert parser.supports_file("test.docx") is True
        assert parser.supports_file("test.DOCX") is True

    def test_supports_file_excel(self):
        """Test file support detection for Excel."""
        parser = DocumentParser()
        assert parser.supports_file("test.xlsx") is True
        assert parser.supports_file("test.xls") is True
        assert parser.supports_file("test.xlsm") is True
        assert parser.supports_file("test.XLSX") is True

    def test_supports_file_csv(self):
        """Test file support detection for CSV."""
        parser = DocumentParser()
        assert parser.supports_file("test.csv") is True
        assert parser.supports_file("test.CSV") is True

    def test_supports_file_unsupported(self):
        """Test file support detection for unsupported types."""
        parser = DocumentParser()
        assert parser.supports_file("test.txt") is False
        assert parser.supports_file("test.pptx") is False
        assert parser.supports_file("test.doc") is False

    def test_get_supported_extensions(self):
        """Test getting supported extensions."""
        parser = DocumentParser()
        extensions = parser.get_supported_extensions()
        assert ".pdf" in extensions
        assert ".docx" in extensions
        assert ".xlsx" in extensions
        assert ".xls" in extensions
        assert ".csv" in extensions
        # Should contain all 5 supported extensions
        assert len(extensions) >= 5

    def test_parse_file_not_found(self):
        """Test parsing non-existent file."""
        parser = DocumentParser()

        with pytest.raises(CustomFileNotFoundError) as exc_info:
            parser.parse_file("nonexistent.pdf")

        assert "File not found" in str(exc_info.value)
        assert exc_info.value.filename == "nonexistent.pdf"

    def test_parse_file_unsupported_type(self, temp_dir):
        """Test parsing unsupported file type."""
        parser = DocumentParser()

        # Create a text file
        txt_file = os.path.join(temp_dir, "test.txt")
        with open(txt_file, "w") as f:
            f.write("Some text content")

        with pytest.raises(UnsupportedFileTypeError) as exc_info:
            parser.parse_file(txt_file)

        assert "Unsupported file type" in str(exc_info.value)

    @patch("document_parser.core.parser.os.path.exists")
    @patch("document_parser.core.parser.os.stat")
    def test_parse_files_some_fail(self, mock_stat, mock_exists):
        """Test parsing multiple files where some fail."""
        parser = DocumentParser()

        # Mock file existence and stats
        mock_exists.return_value = True
        mock_stat.return_value.st_size = 1000

        # Mock parser to fail on second file
        with (
            patch.object(parser._parsers[0], "supports_file_type", return_value=True),
            patch.object(parser._parsers[0], "parse") as mock_parse,
        ):
            mock_parse.side_effect = [
                [Mock()],  # Success for first file
                Exception("Parse error"),  # Failure for second file
            ]

            files = ["test1.pdf", "test2.pdf"]
            results = parser.parse_files(files)

            # Should have one successful result
            assert len(results) == 1

    def test_create_document_info(self, temp_dir):
        """Test document info creation."""
        parser = DocumentParser()

        # Create a test file
        test_file = os.path.join(temp_dir, "test.pdf")
        with open(test_file, "w") as f:
            f.write("test content")

        doc_info = parser._create_document_info(test_file, 5)

        assert doc_info.filename == "test.pdf"
        assert doc_info.file_type == "pdf"
        assert doc_info.total_pages == 5
        assert doc_info.file_size > 0
        assert doc_info.created_at is not None

    def test_batch_processing_multiple_files(self, temp_dir):
        """Test batch processing of multiple files."""
        parser = DocumentParser()

        # Create multiple test files
        test_files = []
        for i, ext in enumerate([".pdf", ".docx", ".csv", ".xlsx"], 1):
            test_file = os.path.join(temp_dir, f"test{i}{ext}")
            with open(test_file, "w") as f:
                f.write(f"test content {i}")
            test_files.append(test_file)

        # Mock all parsers to return successful results
        mock_page_result = Mock()
        mock_page_result.page_number = 1
        mock_page_result.content.text = "Mock content"
        mock_page_result.metadata.word_count = 10

        with patch.object(parser, "_get_parser_for_file") as mock_get_parser:
            mock_parser = Mock()
            mock_parser.parse.return_value = [mock_page_result]
            mock_get_parser.return_value = mock_parser

            results = parser.parse_files(test_files)

            # Should have results for all files
            assert len(results) == 4

            # Check that each result has proper structure
            for result in results:
                assert result.document_info is not None
                assert len(result.pages) > 0
                assert result.pages[0].content.text == "Mock content"

    def test_batch_processing_mixed_success_failure(self, temp_dir):
        """Test batch processing with some files failing."""
        parser = DocumentParser()

        # Create test files
        success_file = os.path.join(temp_dir, "success.pdf")
        failure_file = os.path.join(temp_dir, "failure.pdf")
        unsupported_file = os.path.join(temp_dir, "unsupported.txt")

        with open(success_file, "w") as f:
            f.write("success content")
        with open(failure_file, "w") as f:
            f.write("failure content")
        with open(unsupported_file, "w") as f:
            f.write("unsupported content")

        test_files = [success_file, failure_file, unsupported_file]

        # Mock parser behavior
        mock_page_result = Mock()
        mock_page_result.page_number = 1
        mock_page_result.content.text = "Success content"
        mock_page_result.metadata.word_count = 10

        with patch.object(parser, "_get_parser_for_file") as mock_get_parser:

            def parser_side_effect(file_path):
                if "success" in file_path:
                    mock_parser = Mock()
                    mock_parser.parse.return_value = [mock_page_result]
                    return mock_parser
                elif "failure" in file_path:
                    mock_parser = Mock()
                    mock_parser.parse.side_effect = Exception("Parse error")
                    return mock_parser
                else:  # unsupported
                    return None

            mock_get_parser.side_effect = parser_side_effect

            results = parser.parse_files(test_files)

            # Should only have successful results
            assert len(results) == 1
            assert results[0].document_info.filename == "success.pdf"

    def test_batch_processing_empty_list(self):
        """Test batch processing with empty file list."""
        parser = DocumentParser()

        results = parser.parse_files([])

        assert len(results) == 0
        assert isinstance(results, list)

    def test_batch_processing_nonexistent_files(self):
        """Test batch processing with non-existent files."""
        parser = DocumentParser()

        nonexistent_files = ["nonexistent1.pdf", "nonexistent2.docx"]
        results = parser.parse_files(nonexistent_files)

        # Should return empty list as files don't exist
        assert len(results) == 0

    @patch("document_parser.core.parser.logger")
    def test_batch_processing_logs_errors(self, mock_logger, temp_dir):
        """Test that batch processing logs errors appropriately."""
        parser = DocumentParser()

        # Create a file that will cause parsing to fail
        failing_file = os.path.join(temp_dir, "failing.pdf")
        with open(failing_file, "w") as f:
            f.write("content that will fail")

        with patch.object(parser, "_get_parser_for_file") as mock_get_parser:
            mock_parser = Mock()
            mock_parser.parse.side_effect = Exception("Parsing failed")
            mock_get_parser.return_value = mock_parser

            results = parser.parse_files([failing_file])

            # Should log the error
            mock_logger.error.assert_called()
            error_call_args = mock_logger.error.call_args[0][0]
            assert "Failed to parse" in error_call_args
            assert "failing.pdf" in error_call_args

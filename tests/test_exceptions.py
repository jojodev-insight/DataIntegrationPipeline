"""
Tests for exception classes.
"""

from document_parser.utils.exceptions import (
    DocumentParsingError,
    UnsupportedFileTypeError,
    CorruptedFileError,
    PasswordProtectedError,
    FileNotFoundError,
    InvalidConfigurationError,
)


class TestExceptions:
    """Test cases for custom exceptions."""

    def test_document_parsing_error(self):
        """Test base DocumentParsingError."""
        error = DocumentParsingError("Test error", "test.pdf")

        assert str(error) == "Test error"
        assert error.filename == "test.pdf"

    def test_document_parsing_error_no_filename(self):
        """Test DocumentParsingError without filename."""
        error = DocumentParsingError("Test error")

        assert str(error) == "Test error"
        assert error.filename is None

    def test_unsupported_file_type_error(self):
        """Test UnsupportedFileTypeError."""
        error = UnsupportedFileTypeError("Unsupported", "test.txt")

        assert isinstance(error, DocumentParsingError)
        assert str(error) == "Unsupported"
        assert error.filename == "test.txt"

    def test_corrupted_file_error(self):
        """Test CorruptedFileError."""
        error = CorruptedFileError("File corrupted", "test.pdf")

        assert isinstance(error, DocumentParsingError)
        assert str(error) == "File corrupted"
        assert error.filename == "test.pdf"

    def test_password_protected_error(self):
        """Test PasswordProtectedError."""
        error = PasswordProtectedError("Password required", "secret.pdf")

        assert isinstance(error, DocumentParsingError)
        assert str(error) == "Password required"
        assert error.filename == "secret.pdf"

    def test_file_not_found_error(self):
        """Test custom FileNotFoundError."""
        error = FileNotFoundError("File missing", "missing.pdf")

        assert isinstance(error, DocumentParsingError)
        assert str(error) == "File missing"
        assert error.filename == "missing.pdf"

    def test_invalid_configuration_error(self):
        """Test InvalidConfigurationError."""
        error = InvalidConfigurationError("Bad config")

        assert str(error) == "Bad config"
        # Should not inherit from DocumentParsingError
        assert not isinstance(error, DocumentParsingError)

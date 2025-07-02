"""
Tests for the core DocumentParser class.
"""

import pytest
import os
from unittest.mock import Mock, patch

from document_parser.core.parser import DocumentParser
from document_parser.core.models import DocumentResult, DocumentInfo, PageResult
from document_parser.utils.exceptions import (
    UnsupportedFileTypeError,
    FileNotFoundError as CustomFileNotFoundError
)


class TestDocumentParser:
    """Test cases for DocumentParser class."""
    
    def test_init(self):
        """Test parser initialization."""
        parser = DocumentParser()
        assert parser is not None
        assert len(parser._parsers) == 2  # PDF and DOCX parsers
    
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
    
    def test_supports_file_unsupported(self):
        """Test file support detection for unsupported types."""
        parser = DocumentParser()
        assert parser.supports_file("test.txt") is False
        assert parser.supports_file("test.xlsx") is False
    
    def test_get_supported_extensions(self):
        """Test getting supported extensions."""
        parser = DocumentParser()
        extensions = parser.get_supported_extensions()
        assert '.pdf' in extensions
        assert '.docx' in extensions
    
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
        with open(txt_file, 'w') as f:
            f.write("Some text content")
        
        with pytest.raises(UnsupportedFileTypeError) as exc_info:
            parser.parse_file(txt_file)
        
        assert "Unsupported file type" in str(exc_info.value)
    
    @patch('document_parser.core.parser.os.path.exists')
    @patch('document_parser.core.parser.os.stat')
    def test_parse_files_some_fail(self, mock_stat, mock_exists):
        """Test parsing multiple files where some fail."""
        parser = DocumentParser()
        
        # Mock file existence and stats
        mock_exists.return_value = True
        mock_stat.return_value.st_size = 1000
        
        # Mock parser to fail on second file
        with patch.object(parser._parsers[0], 'supports_file_type', return_value=True), \
             patch.object(parser._parsers[0], 'parse') as mock_parse:
            
            mock_parse.side_effect = [
                [Mock()],  # Success for first file
                Exception("Parse error")  # Failure for second file
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
        with open(test_file, 'w') as f:
            f.write("test content")
        
        doc_info = parser._create_document_info(test_file, 5)
        
        assert doc_info.filename == "test.pdf"
        assert doc_info.file_type == "pdf"
        assert doc_info.total_pages == 5
        assert doc_info.file_size > 0
        assert doc_info.created_at is not None

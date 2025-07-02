"""
Tests for data models.
"""

import pytest
import json
from datetime import datetime

from document_parser.core.models import (
    HeadingInfo, PageContent, PageMetadata, PageResult, 
    DocumentInfo, DocumentResult
)


class TestModels:
    """Test cases for data models."""
    
    def test_heading_info(self):
        """Test HeadingInfo model."""
        heading = HeadingInfo(level=1, text="Chapter 1")
        assert heading.level == 1
        assert heading.text == "Chapter 1"
    
    def test_page_content(self):
        """Test PageContent model."""
        headings = [HeadingInfo(level=1, text="Title")]
        content = PageContent(
            text="Some text",
            paragraphs=["Para 1", "Para 2"],
            headings=headings
        )
        
        assert content.text == "Some text"
        assert len(content.paragraphs) == 2
        assert len(content.headings) == 1
        
        # Test to_dict
        data = content.to_dict()
        assert data['text'] == "Some text"
        assert len(data['paragraphs']) == 2
    
    def test_page_metadata(self):
        """Test PageMetadata model."""
        metadata = PageMetadata(word_count=100, char_count=500)
        
        assert metadata.word_count == 100
        assert metadata.char_count == 500
        
        # Test to_dict
        data = metadata.to_dict()
        assert data['word_count'] == 100
        assert data['char_count'] == 500
    
    def test_page_result(self):
        """Test PageResult model."""
        content = PageContent(
            text="Test", 
            paragraphs=["Test"], 
            headings=[]
        )
        metadata = PageMetadata(word_count=1, char_count=4)
        
        page = PageResult(
            page_number=1,
            content=content,
            metadata=metadata
        )
        
        assert page.page_number == 1
        assert page.content.text == "Test"
        assert page.metadata.word_count == 1
        
        # Test to_dict
        data = page.to_dict()
        assert data['page_number'] == 1
        assert 'content' in data
        assert 'metadata' in data
    
    def test_document_info(self):
        """Test DocumentInfo model."""
        now = datetime.now()
        info = DocumentInfo(
            filename="test.pdf",
            file_type="pdf",
            total_pages=5,
            created_at=now,
            file_size=1000
        )
        
        assert info.filename == "test.pdf"
        assert info.file_type == "pdf"
        assert info.total_pages == 5
        assert info.created_at == now
        assert info.file_size == 1000
        
        # Test to_dict
        data = info.to_dict()
        assert data['filename'] == "test.pdf"
        assert data['total_pages'] == 5
        assert 'created_at' in data
    
    def test_document_result(self):
        """Test DocumentResult model."""
        # Create test data
        info = DocumentInfo(
            filename="test.pdf",
            file_type="pdf",
            total_pages=1,
            created_at=datetime.now(),
            file_size=1000
        )
        
        content = PageContent(text="Test", paragraphs=["Test"], headings=[])
        metadata = PageMetadata(word_count=1, char_count=4)
        page = PageResult(page_number=1, content=content, metadata=metadata)
        
        result = DocumentResult(document_info=info, pages=[page])
        
        assert result.document_info.filename == "test.pdf"
        assert len(result.pages) == 1
        
        # Test to_dict
        data = result.to_dict()
        assert 'document_info' in data
        assert 'pages' in data
        assert len(data['pages']) == 1
    
    def test_document_result_json(self):
        """Test DocumentResult JSON serialization."""
        info = DocumentInfo(
            filename="test.pdf",
            file_type="pdf", 
            total_pages=1,
            created_at=datetime.now(),
            file_size=1000
        )
        
        content = PageContent(text="Test", paragraphs=["Test"], headings=[])
        metadata = PageMetadata(word_count=1, char_count=4)
        page = PageResult(page_number=1, content=content, metadata=metadata)
        
        result = DocumentResult(document_info=info, pages=[page])
        
        # Test compact JSON
        json_str = result.to_json(pretty=False)
        assert isinstance(json_str, str)
        data = json.loads(json_str)
        assert 'document_info' in data
        
        # Test pretty JSON
        pretty_json = result.to_json(pretty=True)
        assert isinstance(pretty_json, str)
        assert len(pretty_json) > len(json_str)  # Pretty should be longer
    
    def test_document_result_save_to_file(self, temp_dir):
        """Test saving DocumentResult to file."""
        import os
        
        info = DocumentInfo(
            filename="test.pdf",
            file_type="pdf",
            total_pages=1, 
            created_at=datetime.now(),
            file_size=1000
        )
        
        content = PageContent(text="Test", paragraphs=["Test"], headings=[])
        metadata = PageMetadata(word_count=1, char_count=4)
        page = PageResult(page_number=1, content=content, metadata=metadata)
        
        result = DocumentResult(document_info=info, pages=[page])
        
        # Save to file
        output_path = os.path.join(temp_dir, "result.json")
        result.save_to_file(output_path)
        
        # Verify file was created and contains valid JSON
        assert os.path.exists(output_path)
        
        with open(output_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert 'document_info' in data
        assert 'pages' in data

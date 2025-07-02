"""
Tests for Excel and CSV parsers.
"""

import pytest
import pandas as pd
import os
import tempfile
from unittest.mock import Mock, patch

from document_parser.parsers.excel_parser import ExcelParser
from document_parser.parsers.csv_parser import CSVParser
from document_parser.utils.exceptions import CorruptedFileError


class TestExcelParser:
    """Test cases for ExcelParser class."""
    
    def test_supports_file_type(self):
        """Test file type support detection."""
        parser = ExcelParser()
        assert parser.supports_file_type("test.xlsx") is True
        assert parser.supports_file_type("test.xls") is True
        assert parser.supports_file_type("test.xlsm") is True
        assert parser.supports_file_type("test.XLSX") is True
        assert parser.supports_file_type("test.pdf") is False
        assert parser.supports_file_type("test.csv") is False
    
    @patch('pandas.ExcelFile')
    @patch('pandas.read_excel')
    def test_parse_success(self, mock_read_excel, mock_excel_file):
        """Test successful Excel parsing."""
        parser = ExcelParser()
        
        # Mock Excel file with two sheets
        mock_file = Mock()
        mock_file.sheet_names = ['Sheet1', 'Sheet2']
        mock_excel_file.return_value = mock_file
        
        # Mock DataFrames
        df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        df2 = pd.DataFrame({'X': ['a', 'b'], 'Y': ['c', 'd']})
        mock_read_excel.side_effect = [df1, df2]
        
        results = parser.parse("test.xlsx")
        
        assert len(results) == 2
        assert results[0].page_number == 1
        assert results[1].page_number == 2
        assert "Sheet1" in results[0].content.text
        assert "Sheet2" in results[1].content.text
    
    def test_dataframe_to_content(self):
        """Test DataFrame to PageContent conversion."""
        parser = ExcelParser()
        df = pd.DataFrame({
            'Name': ['Alice', 'Bob'],
            'Age': [25, 30],
            'City': ['New York', 'London']
        })
        
        content = parser._dataframe_to_content(df, 'TestSheet')
        
        assert 'TestSheet' in content.text
        assert 'Name' in content.text
        assert 'Alice' in content.text
        assert len(content.paragraphs) > 0
        assert len(content.headings) > 0
        assert content.headings[0].text == 'Sheet: TestSheet'
    
    def test_dataframe_to_content_empty(self):
        """Test empty DataFrame conversion."""
        parser = ExcelParser()
        df = pd.DataFrame()
        
        content = parser._dataframe_to_content(df, 'EmptySheet')
        
        assert 'EmptySheet' in content.text
        assert '(Empty sheet)' in content.text
        assert len(content.headings) == 1


class TestCSVParser:
    """Test cases for CSVParser class."""
    
    def test_supports_file_type(self):
        """Test file type support detection."""
        parser = CSVParser()
        assert parser.supports_file_type("test.csv") is True
        assert parser.supports_file_type("test.CSV") is True
        assert parser.supports_file_type("test.xlsx") is False
        assert parser.supports_file_type("test.pdf") is False
    
    @patch('pandas.read_csv')
    def test_parse_success(self, mock_read_csv):
        """Test successful CSV parsing."""
        parser = CSVParser()
        
        # Mock DataFrame
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        mock_read_csv.return_value = df
        
        results = parser.parse("test.csv")
        
        assert len(results) == 1
        assert results[0].page_number == 1
        assert "test.csv" in results[0].content.text
        assert "3" in results[0].content.text  # Should contain row count
    
    def test_dataframe_to_content(self):
        """Test DataFrame to PageContent conversion."""
        parser = CSVParser()
        df = pd.DataFrame({
            'Product': ['Apple', 'Banana', 'Orange'],
            'Price': [1.20, 0.80, 1.50],
            'Stock': [100, 50, 75]
        })
        
        content = parser._dataframe_to_content(df, '/path/to/products.csv')
        
        assert 'products.csv' in content.text
        assert 'Product' in content.text
        assert 'Apple' in content.text
        assert '3' in content.text  # Row count
        assert len(content.paragraphs) > 0
        assert len(content.headings) > 0
    
    def test_dataframe_to_content_with_statistics(self):
        """Test DataFrame conversion includes statistics for numeric columns."""
        parser = CSVParser()
        df = pd.DataFrame({
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Score': [85, 92, 78],
            'Percentage': [85.5, 92.3, 78.1]
        })
        
        content = parser._dataframe_to_content(df, '/path/to/scores.csv')
        
        assert 'Numeric Column Statistics' in content.text
        assert 'Score:' in content.text
        assert 'mean=' in content.text
    
    def test_read_csv_with_fallback(self, temp_dir):
        """Test CSV reading with encoding fallback."""
        parser = CSVParser()
        
        # Create a test CSV file
        csv_content = "Name,Age,City\nAlice,25,New York\nBob,30,London"
        csv_path = os.path.join(temp_dir, "test.csv")
        
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write(csv_content)
        
        df = parser._read_csv_with_fallback(csv_path)
        
        assert len(df) == 2
        assert 'Name' in df.columns
        assert 'Alice' in df['Name'].values
    
    @patch('pandas.read_csv')
    def test_parse_corrupted_file(self, mock_read_csv):
        """Test parsing corrupted CSV file."""
        parser = CSVParser()
        mock_read_csv.side_effect = Exception("File corrupted")
        
        with pytest.raises(CorruptedFileError) as exc_info:
            parser.parse("corrupted.csv")
        
        assert "Failed to parse CSV file" in str(exc_info.value)
        assert exc_info.value.filename == "corrupted.csv"


class TestIntegration:
    """Integration tests for Excel and CSV parsers."""
    
    def test_create_sample_excel_file(self, temp_dir):
        """Test creating and parsing a real Excel file."""
        # Create sample data
        data = {
            'Product': ['Laptop', 'Mouse', 'Keyboard'],
            'Price': [999.99, 25.50, 75.00],
            'Stock': [10, 100, 50]
        }
        df = pd.DataFrame(data)
        
        # Save to Excel file
        excel_path = os.path.join(temp_dir, "products.xlsx")
        df.to_excel(excel_path, index=False, sheet_name='Products')
        
        # Parse with our parser
        parser = ExcelParser()
        results = parser.parse(excel_path)
        
        assert len(results) == 1
        assert 'Laptop' in results[0].content.text
        assert 'Products' in results[0].content.text
    
    def test_create_sample_csv_file(self, temp_dir):
        """Test creating and parsing a real CSV file."""
        # Create sample CSV
        csv_content = "Name,Age,Department,Salary\nAlice Johnson,28,Engineering,75000\nBob Smith,35,Marketing,65000\nCarol Davis,42,HR,70000"
        csv_path = os.path.join(temp_dir, "employees.csv")
        
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write(csv_content)
        
        # Parse with our parser
        parser = CSVParser()
        results = parser.parse(csv_path)
        
        assert len(results) == 1
        assert 'Alice Johnson' in results[0].content.text
        assert 'employees.csv' in results[0].content.text
        assert '4' in results[0].content.text  # Column count

"""
Test configuration and fixtures.
"""

import pytest
import tempfile
import os
import sys
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir


@pytest.fixture
def sample_pdf_path(temp_dir):
    """Create a sample PDF file path (would need actual PDF for real tests)."""
    pdf_path = os.path.join(temp_dir, "sample.pdf")
    # In real implementation, you'd create or copy a real PDF file here
    return pdf_path


@pytest.fixture
def sample_docx_path(temp_dir):
    """Create a sample DOCX file path (would need actual DOCX for real tests)."""
    docx_path = os.path.join(temp_dir, "sample.docx")
    # In real implementation, you'd create or copy a real DOCX file here
    return docx_path

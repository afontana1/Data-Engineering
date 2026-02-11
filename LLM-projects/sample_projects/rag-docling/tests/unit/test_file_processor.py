import pytest
from src.utils.file_processor import process_file
from io import BytesIO
import os

def test_process_txt_file():
    # Create a mock text file
    content = "This is a test document."
    file = BytesIO(content.encode())
    file.name = "test.txt"
    
    # Process the file
    process_file(file)
    
    # Assert the file was processed (check if vectorstore was updated)
    # Note: This would require mocking the vectorstore in a real test

def test_process_unsupported_file():
    file = BytesIO(b"test content")
    file.name = "test.xyz"
    
    with pytest.raises(ValueError) as exc_info:
        process_file(file)
    
    assert "Unsupported file type" in str(exc_info.value)

def test_process_empty_file():
    file = BytesIO(b"")
    file.name = "test.txt"
    
    process_file(file)  # Should handle empty files gracefully 
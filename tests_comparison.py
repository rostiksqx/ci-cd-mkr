import pytest
import os
import tempfile
from file_comparison import read_file, write_to_file, compare_files, main


@pytest.fixture
def temp_directory():
    """Fixture that provides a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname


@pytest.fixture
def sample_files(temp_directory):
    """
    Fixture that creates sample text files for testing.
    
    Returns:
        tuple: (file1_path, file2_path, common_lines, unique_lines)
    """
    # Create test files
    file1_path = os.path.join(temp_directory, "test1.txt")
    file2_path = os.path.join(temp_directory, "test2.txt")
    
    # Sample data
    file1_content = ["line1", "line2", "line3", "line4"]
    file2_content = ["line2", "line3", "line5", "line6"]
    
    # Write content to files
    with open(file1_path, 'w', encoding='utf-8') as f1:
        f1.write('\n'.join(file1_content))
        
    with open(file2_path, 'w', encoding='utf-8') as f2:
        f2.write('\n'.join(file2_content))
    
    # Common lines and unique lines
    common_lines = ["line2", "line3"]
    unique_lines = ["line1", "line4", "line5", "line6"]
    
    return file1_path, file2_path, common_lines, unique_lines


def test_read_file(sample_files):
    """Test the read_file function."""
    file1_path, _, _, _ = sample_files
    
    # Test successful reading
    lines = read_file(file1_path)
    assert lines == ["line1", "line2", "line3", "line4"]
    
    # Test reading non-existent file
    non_existent_file = "non_existent_file.txt"
    lines = read_file(non_existent_file)
    assert lines == []


def test_write_to_file(temp_directory):
    """Test the write_to_file function."""
    test_file_path = os.path.join(temp_directory, "write_test.txt")
    content = ["test line 1", "test line 2", "test line 3"]
    
    # Test successful writing
    result = write_to_file(test_file_path, content)
    assert result is True
    
    # Verify content was written correctly
    with open(test_file_path, 'r', encoding='utf-8') as file:
        written_content = [line.strip() for line in file.readlines()]
    assert written_content == content


@pytest.mark.parametrize("file1_content,file2_content,expected_same,expected_diff", [
    (
        ["line1", "line2", "line3"], 
        ["line2", "line3", "line4"], 
        ["line2", "line3"], 
        ["line1", "line4"]
    ),
    (
        ["A", "B", "C"], 
        ["D", "E", "F"], 
        [], 
        ["A", "B", "C", "D", "E", "F"]
    ),
    (
        ["X", "Y", "Z"], 
        ["X", "Y", "Z"], 
        ["X", "Y", "Z"], 
        []
    ),
    (
        [], 
        ["something"], 
        [], 
        ["something"]
    ),
])
def test_compare_files_parametrized(temp_directory, file1_content, file2_content, expected_same, expected_diff):
    """Test the compare_files function with different test cases."""
    # Create test files
    file1_path = os.path.join(temp_directory, "param_test1.txt")
    file2_path = os.path.join(temp_directory, "param_test2.txt")
    
    # Write content to files
    with open(file1_path, 'w', encoding='utf-8') as f1:
        f1.write('\n'.join(file1_content))
        
    with open(file2_path, 'w', encoding='utf-8') as f2:
        f2.write('\n'.join(file2_content))
    
    # Call the function
    same_lines, diff_lines = compare_files(file1_path, file2_path)
    
    # Sort the results for reliable comparison
    same_lines.sort()
    diff_lines.sort()
    expected_same.sort()
    expected_diff.sort()
    
    # Assert results
    assert same_lines == expected_same
    assert diff_lines == expected_diff


def test_main_function(sample_files, temp_directory):
    """Test the main function."""
    file1_path, file2_path, expected_same, expected_diff = sample_files
    
    # Define output paths
    same_output_path = os.path.join(temp_directory, "same_output.txt")
    diff_output_path = os.path.join(temp_directory, "diff_output.txt")
    
    # Call the main function
    same_success, diff_success = main(
        file1_path, 
        file2_path, 
        same_output_path, 
        diff_output_path
    )
    
    # Check return values
    assert same_success is True
    assert diff_success is True
    
    # Check output file contents
    same_content = read_file(same_output_path)
    diff_content = read_file(diff_output_path)
    
    # Sort for reliable comparison
    same_content.sort()
    diff_content.sort()
    expected_same.sort()
    expected_diff.sort()
    
    assert same_content == expected_same
    assert diff_content == expected_diff


def test_edge_cases(temp_directory):
    """Test edge cases like empty files."""
    # Create empty files
    empty_file1 = os.path.join(temp_directory, "empty1.txt")
    empty_file2 = os.path.join(temp_directory, "empty2.txt")
    
    with open(empty_file1, 'w', encoding='utf-8') as f1:
        pass
    
    with open(empty_file2, 'w', encoding='utf-8') as f2:
        pass
    
    # Output paths
    same_output_path = os.path.join(temp_directory, "same_empty.txt")
    diff_output_path = os.path.join(temp_directory, "diff_empty.txt")
    
    # Test with empty files
    same_success, diff_success = main(
        empty_file1,
        empty_file2,
        same_output_path,
        diff_output_path
    )
    
    # Check results
    assert same_success is True
    assert diff_success is True
    
    # Both files should be empty
    same_content = read_file(same_output_path)
    diff_content = read_file(diff_output_path)
    
    assert same_content == []
    assert diff_content == []
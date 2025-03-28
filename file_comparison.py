def read_file(file_path):
    """
    Reads a text file and returns its content as a list of lines.
    
    Args:
        file_path (str): Path to the text file to be read
        
    Returns:
        list: List of strings, each representing a line from the file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return []
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []

def write_to_file(file_path, content):
    """
    Writes a list of strings to a text file, each string as a separate line.
    
    Args:
        file_path (str): Path to the file where content will be written
        content (list): List of strings to write to the file
    
    Returns:
        bool: True if writing was successful, False otherwise
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            for line in content:
                file.write(line + '\n')
        return True
    except Exception as e:
        print(f"Error writing to file {file_path}: {e}")
        return False
    
def compare_files(file1_path, file2_path):
    """
    Compares the content of two text files.
    
    Args:
        file1_path (str): Path to the first text file
        file2_path (str): Path to the second text file
        
    Returns:
        tuple: (same_lines, diff_lines) where:
            - same_lines is a list of lines that exist in both files
            - diff_lines is a list of lines that exist in only one of the files
    """
    lines1 = read_file(file1_path)
    lines2 = read_file(file2_path)
    
    set1 = set(lines1)
    set2 = set(lines2)
    
    same_lines = list(set1.intersection(set2))
    
    diff_lines = list(set1.symmetric_difference(set2))
    
    return same_lines, diff_lines

def main(file1_path, file2_path, same_output_path="same.txt", diff_output_path="diff.txt"):
    """
    Main function that:
    1. Reads content from two text files
    2. Compares their content
    3. Writes common lines to "same.txt"
    4. Writes lines that exist in only one file to "diff.txt"
    
    Args:
        file1_path (str): Path to the first text file
        file2_path (str): Path to the second text file
        same_output_path (str): Path where common lines will be written
        diff_output_path (str): Path where different lines will be written
        
    Returns:
        tuple: (same_success, diff_success) indicating whether writing to
               respective output files was successful
    """
    # Compare files
    same_lines, diff_lines = compare_files(file1_path, file2_path)
    
    # Write results to output files
    same_success = write_to_file(same_output_path, same_lines)
    diff_success = write_to_file(diff_output_path, diff_lines)
    
    return same_success, diff_success

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python file_comparison.py <file1_path> <file2_path>")
        sys.exit(1)
    
    file1_path = sys.argv[1]
    file2_path = sys.argv[2]
    
    same_success, diff_success = main(file1_path, file2_path)
    
    if same_success and diff_success:
        print("Comparison completed successfully.")
        print(f"Common lines written to 'same.txt'")
        print(f"Different lines written to 'diff.txt'")
    else:
        print("Comparison completed with errors.")
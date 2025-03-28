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

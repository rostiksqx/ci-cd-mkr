# File Comparison Tool

A Python script that compares two text files and outputs:
- Common lines to `same.txt`
- Unique lines to `diff.txt`

## Features

- Reads two text files and compares their content line by line
- Identifies lines that are common to both files
- Identifies lines that are unique to either file
- Writes results to separate output files
- Comprehensive error handling
- Fully tested with pytest

## Installation

1. Clone this repository
2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

```
python file_comparison.py <file1_path> <file2_path>
```

Example:
```
python file_comparison.py sample1.txt sample2.txt
```

This will:
1. Read the content of `sample1.txt` and `sample2.txt`
2. Compare their contents
3. Write common lines to `same.txt`
4. Write unique lines to `diff.txt`

## Testing

Run the tests with:

```
pytest
```

Generate an HTML test report with:

```
pytest testing/ --html=report.html --self-contained-html
```

## CI/CD

This project uses GitHub Actions for continuous integration:
- Runs tests on push to main/master branches
- Validates code against PEP8 standards using flake8
- Generates and uploads test reports
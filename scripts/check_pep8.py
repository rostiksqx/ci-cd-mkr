import os
import sys
import subprocess
import glob


def run_command(command):
    """Run shell command and return output"""
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Command '{command}' failed with error: {stderr}")
    return stdout, stderr, process.returncode


def check_with_flake8():
    """Check code with flake8 and generate HTML report"""
    print("Running flake8 checks...")
    
    # Create directory for reports if it doesn't exist
    os.makedirs("flake-report", exist_ok=True)
    
    # Run flake8 with HTML report
    cmd = "flake8 . --count --max-line-length=100 --format=html --htmldir=flake-report"
    stdout, stderr, return_code = run_command(cmd)
    
    # Get summary count
    count_cmd = "flake8 . --count"
    count_out, _, _ = run_command(count_cmd)
    
    violations = sum(int(line) for line in count_out.strip().split('\n') if line.isdigit())
    
    print(f"Found {violations} PEP8 violations.")
    print(f"HTML report generated in flake-report/index.html")
    
    return violations


def check_with_black():
    """Check if code would be reformatted by black"""
    print("\nRunning black format checks...")
    
    # Get all Python files
    python_files = glob.glob("**/*.py", recursive=True)
    
    # Filter out directories to ignore
    ignore_dirs = [".git", "__pycache__", "venv", "build", "dist"]
    python_files = [
        f for f in python_files 
        if not any(ignore_dir in f for ignore_dir in ignore_dirs)
    ]
    
    if not python_files:
        print("No Python files found to check.")
        return 0
    
    # Run black in check mode
    files_arg = " ".join(python_files)
    cmd = f"black --check --line-length 100 {files_arg}"
    stdout, stderr, return_code = run_command(cmd)
    
    would_change = "would be reformatted" in stdout
    files_to_format = stdout.count("would be reformatted")
    
    if would_change:
        print(f"{files_to_format} files would be reformatted by black.")
        print("To format files, run: black --line-length 100 .")
    else:
        print("All files are properly formatted according to black.")
    
    return files_to_format


def main():
    """Main function to run all checks"""
    print("PEP8 Code Compliance Check")
    print("=" * 30)
    
    flake8_violations = check_with_flake8()
    black_files = check_with_black()
    
    print("\nSummary:")
    print(f"- Flake8: {flake8_violations} PEP8 violations")
    print(f"- Black: {black_files} files would be reformatted")
    
    total_issues = flake8_violations + black_files
    print(f"\nTotal issues: {total_issues}")
    
    if total_issues > 0:
        print("\nRecommendation: Fix PEP8 issues and run black formatter before committing.")
        return 1
    else:
        print("\nCode complies with PEP8 standards! ✅")
        return 0


if __name__ == "__main__":
    sys.exit(main())
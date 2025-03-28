import os
import sys
import pytest

# Add root directory to path so that tests can import the main module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
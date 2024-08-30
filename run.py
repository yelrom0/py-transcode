"""
run.py
This is the main entry point for the application.
"""

# Local Imports
from src.fs import FS

if __name__ == "__main__":
    files = FS.get_files("/Users/yelrom0/Movies")
    # files = FS.get_files("~/Movies")
    print(f"Files: {files}")

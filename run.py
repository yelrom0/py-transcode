"""
run.py
This is the main entry point for the application.
"""

# Package Imports
from anyio import run

# Local Imports
from src.fs import get_files
from src.cli import parse_args
from src.media import transcode_files


async def main():
    # No check for args, as an error is raised if
    # required args not provided
    args = parse_args()

    # print(f"Path: {args.path}")
    # print(f"Recursive: {args.recursive}")

    files = get_files(args.path, args.recursive)
    await transcode_files(files)


if __name__ == "__main__":
    run(main)

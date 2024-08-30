"""
run.py
This is the main entry point for the application.
"""

# Package Imports
from anyio import run

# Local Imports
from src.cli import parse_args
from src.fs import get_files
from src.media import transcode_files
from src.observer import create_watch_dir


async def main():
    # No check for args, as an error is raised if
    # required args not provided
    args = parse_args()

    # print(f"Path: {args.path}")
    # print(f"Recursive: {args.recursive}")

    if args.watch:
        print("Watching for new files")
        await create_watch_dir(args.path, args.recursive)

    files = get_files(args.path, args.recursive)
    await transcode_files(files)


if __name__ == "__main__":
    run(main)

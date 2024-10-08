"""
cli.py

Module for handling command line arguments.
"""

# System Imports
from argparse import ArgumentParser, Namespace


def parse_args() -> Namespace:
    """
    Parse command line arguments given to the application.
    """

    parser = ArgumentParser(description="A simple CLI application.")

    parser.add_argument(
        "path",
        help="The path to the file or directory to transcode.",
        type=str,
    )

    parser.add_argument(
        "-r",
        "--recursive",
        help="Recursively find and transcode files in child directories.",
        action="store_true",
    )

    parser.add_argument(
        "-w",
        "--watch",
        help="Watch the directory(ies) for new files to transcode.",
        action="store_true",
    )

    return parser.parse_args()

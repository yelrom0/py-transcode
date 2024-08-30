"""
cli.py

Module for handling command line arguments.
"""

# System Imports
from argparse import ArgumentParser


def parse_args():
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
    )

    return parser.parse_args()

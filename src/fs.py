"""
fs.py
Module for file system operations.
"""

# System Imports
from os import path as ospath, walk as dirwalk

# Local Imports
from src.meta import FILE_EXTENSIONS


def _format_path(
    path: str,
) -> str:
    """
    Format the path to be absolute and correct even if relative.
    """
    if path[0] == "~":
        return ospath.expanduser(path)

    if path[0] == ".":
        return ospath.realpath(path)

    return path


def get_files(
    path: str,
    recursive: bool = False,
) -> list[str]:
    """
    Given a path to a file or folder, return a list of all
    subfiles/dirs - **yelrom0**

    Args:
        path (str): The path to the top file or folder
        recursive (bool, optional): Whether to recursively
        search for files. Defaults to False.
    Returns:
        list[str]: A list of all subfiles/dirs
    """

    # format path
    path = _format_path(path)

    if not ospath.exists(path):
        raise FileNotFoundError(f"Path {path} does not exist")

    # Check if file, if so, check if it is of the correct type
    # otherwise, return the file
    if ospath.isfile(path):
        if not path.split(".")[-1] in FILE_EXTENSIONS:
            raise ValueError(
                f"File {path} is not of type {FILE_EXTENSIONS}",
            )
        return [path]

    files = []
    for root, _, filenames in dirwalk(path):
        for filename in filenames:
            file = ospath.join(root, filename)
            if file.split(".")[-1] in FILE_EXTENSIONS:
                files.append(file)
            else:
                continue

        if not recursive:
            break
            # print(f"Dirs: {subdirs}")

    return files

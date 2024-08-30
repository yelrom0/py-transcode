"""
fs.py
Module for file system operations.
"""

# System Imports
from os import path as ospath, walk as dirwalk


class FS:

    def __init__(self):
        pass

    @staticmethod
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

    @staticmethod
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

        path = FS._format_path(path)

        if not ospath.exists(path):
            raise FileNotFoundError(f"Path {path} does not exist")

        if ospath.isfile(path):
            return [path]

        files = []
        for root, _, filenames in dirwalk(path):
            for filename in filenames:
                files.append(ospath.join(root, filename))

            if not recursive:
                break

        return files

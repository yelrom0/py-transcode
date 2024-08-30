"""
observer.py

This was created in order to deal with the circular dependancy between
fs.py and media.py. It handles watching a directory for new files/folders and
handling the events that occur.
"""

# System Imports
from time import sleep

# Package Imports
from anyio import create_task_group
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from watchdog.observers import Observer

recurse: bool = False


class FileHandler(FileSystemEventHandler):
    def on_created(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            global recurse
            print(f"Directory created {recurse}")
            return
        # print(f"New file {event.src_path} has been added")
        print(f"event: {event}")


async def _watch_dir(
    path: str,
    recursive: bool = False,
) -> None:
    """
    Watch a directory for new files.
    If a new file is added, return the path.
    """
    global recurse
    recurse = recursive
    handler = FileHandler()
    observer = Observer()
    observer.schedule(handler, path, recursive=recursive)
    observer.start()
    try:
        while True:
            sleep(1)
    finally:
        observer.stop()
        observer.join()


async def create_watch_dir(
    path: str,
    recursive: bool = False,
) -> None:
    async with create_task_group() as tg:
        tg.start_soon(_watch_dir, path, recursive)

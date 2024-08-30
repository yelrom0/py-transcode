"""
media.py

Module for media operations, currently using python-ffmpeg.
"""

# Package Imports
from ffmpeg.asyncio import FFmpeg

# Local Imports
from src.fs import get_out_path


async def transcode_file(path: str) -> None:
    """
    Transcode a video file to av1 format - **yelrom0**
    Args:
        path (str): Path to the video file
    """
    out_path = get_out_path(path)
    # print(out_path)
    ffmpeg = (
        FFmpeg()
        .option("y")
        .input(path)
        .output(
            out_path,
            {"codec:v": "librav1e"},
        )
    )

    await ffmpeg.execute()


async def transcode_files(paths: list[str]) -> None:
    """
    Transcode a list of video files to av1 format this is really
    just a wrapper around `transcode_file` - **yelrom0**
    """
    for path in paths:
        await transcode_file(path)


# class Media:
#     _ffmpeg: FFmpeg

#     def __init__(self) -> None:
#         # option("y") enables experimental features
#         self._ffmpeg = FFmpeg().option("y")

#     async def _add_path(self, )

#     @staticmethod
#     async def transcode_files(paths: list[str]) -> type[FFmpeg]:
#         """
#         Transcode a video file to av1 format - **yelrom0**
#         Args:
#             paths (list[str]): List of paths to the video files
#         """
#         pass

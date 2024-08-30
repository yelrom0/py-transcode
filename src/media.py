"""
media.py

Module for media operations, currently using python-ffmpeg.
"""

# Package Imports
from ffmpeg import Progress
from ffmpeg.asyncio import FFmpeg

# Local Imports
from src.fs import get_out_path, write_file


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

    @ffmpeg.on("progress")
    def progress_handler(progress: Progress):
        """
        Display progress of ffmpeg transcoding.
        """
        print(f"Progress: {progress}")

    data = await ffmpeg.execute()
    await write_file(out_path, data)
    print(f"File {out_path} successfully transcoded")


async def transcode_files(paths: list[str]) -> None:
    """
    Transcode a list of video files to av1 format this is really
    just a wrapper around `transcode_file` - **yelrom0**
    """
    for path in paths:
        await transcode_file(path)

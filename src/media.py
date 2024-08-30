"""
media.py

Module for media operations, currently using python-ffmpeg.
"""

# Package Imports
from ffmpeg import Progress
from ffmpeg.asyncio import FFmpeg
from ffmpeg.errors import FFmpegUnsupportedCodec

# Local Imports
from src.fs import get_out_path, write_file
from src.meta import FileEncodings


async def transcode_file(path: str, codec: str = "librav1e") -> None:
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
            vcodec=codec,
        )
    )

    @ffmpeg.on("progress")
    def progress_handler(progress: Progress):
        """
        Display progress of ffmpeg transcoding.
        """
        print(f"Progress: {progress}")

    try:
        data = await ffmpeg.execute()
    except FFmpegUnsupportedCodec:
        if codec == "libaom-av1":
            print("Error: libaom-av1 codec is not installed.")
            return
        # this exception is thrown if the codec is not installed
        # I'll fall back to libaom-av1
        await transcode_file(path, "libaom-av1")
        return
    await write_file(out_path, data)
    print(f"File {out_path} successfully transcoded")


async def transcode_files(paths: list[str]) -> None:
    """
    Transcode a list of video files to av1 format this is really
    just a wrapper around `transcode_file` - **yelrom0**
    """
    for path in paths:
        await transcode_file(path)


async def check_file_encoding(path: str) -> FileEncodings:
    """
    Check the encoding of a file - **yelrom0**
    Args:
        path (str): Path to the video file
    Returns:
        FileEncodings: The encoding of the file
    """

    pass

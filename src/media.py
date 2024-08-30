"""
media.py

Module for media operations, currently using python-ffmpeg.
"""

# Package Imports
from ffmpeg import Progress
from ffmpeg.asyncio import FFmpeg
from ffmpeg.errors import FFmpegUnsupportedCodec
from ffprobe3.ffprobe import FFProbe, FFStream
from rich.progress import Progress as RichProgress

# Local Imports
from src.fs import get_out_path, write_file
from src.meta import FileEncodings

# Global Variables
prev_frame: int = 0


class VideoInfo(object):
    """
    Denotes information about a video file

    encoding: The encoding of the file
    size: the size of the file (in frame count)
    path: the file path
    """

    encoding: FileEncodings
    size: any
    path: str

    def _duration_to_seconds(self, duration: str) -> int:
        """
        Convert a duration string to seconds
        """
        h, m, s = map(int, duration[:8].split(":"))
        us = float(duration[8:])
        return (h * 3600) + (m * 60) + s + (us / 1e6)

    def _frame_rate_to_float(self, frame_rate: str) -> float:
        """
        Convert a frame rate string to a float
        """
        n, d = map(int, frame_rate.split("/"))
        return n / d

    def __init__(self, path: str) -> None:
        self.path = path
        metadata = FFProbe(path)

        video_stream: FFStream = metadata.video[0]
        self.encoding = video_stream.codec()
        tags = video_stream.dstream.get("tags")
        duration_str = tags.get("DURATION")
        duration = self._duration_to_seconds(duration_str)
        frame_rate = video_stream.dstream.get("avg_frame_rate")
        self.size = int(duration * self._frame_rate_to_float(frame_rate))

    def __repr__(self):
        ret = f"Path: {self.path}"
        ret += f"\nFrame Count: {self.size}"
        ret += f"\nEncoding: {self.encoding}"
        return ret


async def transcode_file(path: str, codec: str = "librav1e") -> None:
    """
    Transcode a video file to av1 format - **yelrom0**
    Args:
        path (str): Path to the video file
    """

    # get the video info from the path
    info = VideoInfo(path)

    # set up the progress bar
    with RichProgress(expand=True) as progress_bar:
        # print(info)
        transcode_task = progress_bar.add_task(
            f"Transcoding {path.split("/")[-1]}",
            total=info.size,
        )
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

            We get the difference in frames
            and update the progress bar accordingly.
            """
            global prev_frame
            # print(f"prev_frame after global: {prev_frame}")

            current_frame = progress.frame
            # print(f"current_frame: {current_frame}")
            frame_delta = current_frame - prev_frame
            # print(f"frame_delta: {frame_delta}")
            prev_frame = current_frame
            # print(f"prev_frame: {prev_frame}")

            progress_bar.update(transcode_task, advance=frame_delta)
            # print(f"Progress: {progress}")

        try:
            data = await ffmpeg.execute()
        except FFmpegUnsupportedCodec:
            # This exception is thrown if the codec is not installed
            # I'll fall back to libaom-av1, but will fail if ffpeg
            # is too old to support it
            if codec == "libaom-av1":
                print("Error: libaom-av1 codec is not installed.")
                return

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

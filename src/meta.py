"""
meta.py

Metadata for the project.
"""

# System Imports
from enum import Enum


class FileExtensions(Enum):
    WAV = "wav"
    MP4 = "mp4"
    MKV = "mkv"
    AVI = "avi"
    WEBM = "webm"


class FileEncodings(Enum):
    AV1 = "av1"
    H264 = "h264"
    H265 = "h265"
    VP8 = "vp8"
    VP9 = "vp9"
    THEORA = "theora"
    VP9 = "vp9"

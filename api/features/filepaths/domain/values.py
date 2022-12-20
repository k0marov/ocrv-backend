import dataclasses
import pathlib


@dataclasses.dataclass
class RecordingMeta:
    text_id: str
    by_user_id: str
    is_video: bool

@dataclasses.dataclass
class RecordingPaths:
    audio_path: pathlib.Path
    video_path: pathlib.Path

@dataclasses.dataclass
class CompletionStatus:
    url: str
    is_video: bool


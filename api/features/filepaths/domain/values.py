import dataclasses


@dataclasses.dataclass
class RecordingMeta:
    text_id: str
    by_user_id: str
    is_video: bool

@dataclasses.dataclass
class RecordingPaths:
    audio_path: str
    video_path: str


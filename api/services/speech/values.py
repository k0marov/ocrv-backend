import dataclasses

from django.core.files.uploadedfile import UploadedFile


@dataclasses.dataclass
class Recording:
    user_id: str
    text_id: str
    retries: int
    speech: UploadedFile
    is_video: bool


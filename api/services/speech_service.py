import dataclasses

from django.core.files.uploadedfile import UploadedFile

from api.services import api_logger

VIDEO_EXT = 'mp4'
AUDIO_EXT = 'wav'

@dataclasses.dataclass
class Recording:
    user_id: int
    text_id: str
    retries: int
    speech: UploadedFile
    is_video: bool

def save_recording(rec: Recording) -> None:
    base_filename = f'{rec.user_id}_{rec.text_id}.'
    ext = VIDEO_EXT if rec.is_video else AUDIO_EXT
    filename = base_filename + ext
    _save_speech_file(filename, rec.speech)
    api_logger.logger.info(f"Success text id: {rec.text_id}; retries: {rec.retries}; user {rec.user_id}")

def _save_speech_file(filename: str, speech: UploadedFile) -> None:
    with open(filename, 'wb+') as destination:
        for chunk in speech.chunks():
            destination.write(chunk)


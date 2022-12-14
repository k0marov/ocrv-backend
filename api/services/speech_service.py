import dataclasses
from django.conf import settings

from django.core.files.uploadedfile import UploadedFile

from . import api_logger

@dataclasses.dataclass
class Recording:
    user_id: int
    text_id: str
    retries: int
    speech: UploadedFile
    is_video: bool

VIDEO_EXT = 'mp4'
AUDIO_EXT = 'wav'
def save_recording(rec: Recording) -> None:
    base_filename = f'{rec.user_id}_{rec.text_id}.'
    ext = VIDEO_EXT if rec.is_video else AUDIO_EXT
    filename = base_filename + ext

    path = _save_speech_file(filename, rec.speech)
    if rec.is_video:
        # also overrides the path to point to the audio file
        path = _save_audio_from_video(path, base_filename)
    _check_duration(rec.text_id, path)

    api_logger.logger.info(f"Success text id: {rec.text_id}; retries: {rec.retries}; user {rec.user_id}")

def _save_speech_file(filename: str, speech: UploadedFile) -> str:
    path = str(settings.RECORDINGS_DIR / filename)
    with open(path, 'wb+') as destination:
        for chunk in speech.chunks():
            destination.write(chunk)
    return path

def _save_audio_from_video(video_path: str, base_filename: str) -> str:
    pass

def _check_duration(text_id: str, audio_path: str) -> None:
    pass


import pathlib

import ffmpeg
from django.conf import settings

from django.core.files.uploadedfile import UploadedFile

from . import values
from .. import logging_helpers

VIDEO_EXT = 'mp4'
AUDIO_EXT = 'wav'
def save_recording(rec: values.Recording) -> None:
    print(rec.is_video)
    base_filename = f'{rec.user_id}_{rec.text_id}.'
    ext = VIDEO_EXT if rec.is_video else AUDIO_EXT
    filename = base_filename + ext

    path = _save_speech_file(filename, rec.speech)
    if rec.is_video:
        # also overrides the path to point to the audio file
        path = _save_audio_from_video(path, base_filename)
    _check_duration(rec.text_id, path)
    logging_helpers.log_success(rec)


def _save_speech_file(filename: str, speech: UploadedFile) -> pathlib.Path:
    path = settings.RECORDINGS_DIR / filename
    with path.open('wb+') as destination:
        for chunk in speech.chunks():
            destination.write(chunk)
    return path

def _save_audio_from_video(video_path: pathlib.Path, base_filename: str) -> pathlib.Path:
    audio_filename = base_filename + AUDIO_EXT
    audio_path = video_path.parent / audio_filename
    print(audio_path)
    (
        ffmpeg
        .input(str(video_path))
        .output(str(audio_path))
        .run()
    )
    return audio_path

def _check_duration(text_id: str, audio_path: pathlib.Path) -> None:
    pass


import math
import os
import pathlib
import uuid
from typing import List

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

from . import values, log, media
from .exceptions import MinDurationException, MaxDurationException
from ..text import find_text, TextNotFound


VIDEO_EXT = 'mp4'
AUDIO_EXT = 'wav'
def save_recording(rec: values.Recording) -> None:
    base_filename = f'{rec.user_id}_{rec.text_id}.'

    paths = []
    try:
        speech_path = _save_speech_file(rec, base_filename)
        paths += speech_path
        _validate_duration_and_log(rec, speech_path)
        if rec.is_video:
            paths += _save_audio_from_video(speech_path, base_filename)
        log.log_success(rec)
    except Exception as e:
        map(os.remove, paths)
        raise e


def _save_speech_file(rec: values.Recording, base_filename: str) -> pathlib.Path:
    filename = base_filename + (VIDEO_EXT if rec.is_video else AUDIO_EXT)
    path = settings.RECORDINGS_DIR / filename
    tmp_path = settings.RECORDINGS_DIR / ("tmp_" + filename)

    try:
        _save_input(rec.speech, tmp_path)
        media.reencode(str(tmp_path), str(path))
    finally:
        os.remove(tmp_path)
    return path

def _save_input(file: UploadedFile, path: str):
    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def _save_audio_from_video(video_path: pathlib.Path, base_filename: str) -> None:
    audio_filename = base_filename + AUDIO_EXT
    audio_path = video_path.parent / audio_filename
    media.extract_audio(str(video_path), str(audio_path))

def _validate_duration_and_log(rec: values.Recording, path: pathlib.Path):
    try:
        validate_duration(rec.text_id, path)
    except MinDurationException as e:
        log.log_min_duration_exception(rec, e)
        raise e
    except MaxDurationException as e:
        log.log_max_duration_exception(rec, e)
        raise e

def validate_duration(text_id: str, media_path: pathlib.Path) -> None:
    text = find_text(text_id)
    if text is None: raise TextNotFound()
    duration = media.get_duration(str(media_path))
    if text.min_duration and duration < text.min_duration:
        raise MinDurationException(got=math.floor(duration), want=text.min_duration)
    elif text.max_duration and duration > text.max_duration:
        raise MaxDurationException(got=math.ceil(duration), want=text.max_duration)


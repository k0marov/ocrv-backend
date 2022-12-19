import math
import os
import pathlib

from django.core.files.uploadedfile import UploadedFile

from ocrvBackendV2 import settings
from .service import SpeechService
from .exceptions import MinDurationException, MaxDurationException
from . import values, log
from api.features.speech.domain.external.mediaencoding import MediaEncoding
from ...text import TextNotFound, TextService

_VIDEO_EXT = 'mp4'
_AUDIO_EXT = 'wav'


class SpeechServiceImpl(SpeechService):
    def __init__(self, media: MediaEncoding, text: TextService):
        self.media = media
        self.text = text
    def save_recording(self, rec: values.Recording) -> None:
        base_filename = _get_base_filename(rec.user_id, rec.text_id)

        paths = []
        try:
            speech_path = self._save_speech_file(rec, base_filename)
            paths += speech_path
            self._validate_duration_and_log(rec, speech_path)
            if rec.is_video:
                paths += self._save_audio_from_video(speech_path, base_filename)
            log.log_success(rec)
        except Exception as e:
            map(os.remove, paths)
            raise e

    def has_recorded(self, user_id: str, text_id: str) -> bool:
        filename = _get_base_filename(user_id, text_id) + _AUDIO_EXT
        path = settings.RECORDINGS_DIR / filename
        return os.path.exists(path)

    def _validate_duration_and_log(self, rec: values.Recording, path: pathlib.Path):
        try:
            self._validate_duration(rec.text_id, path)
        except MinDurationException as e:
            log.log_min_duration_exception(rec, e)
            raise e
        except MaxDurationException as e:
            log.log_max_duration_exception(rec, e)
            raise e

    def _validate_duration(self, text_id: str, media_path: pathlib.Path) -> None:
        text = self.text.find_text(text_id)
        if text is None: raise TextNotFound()
        duration = self.media.get_duration(str(media_path))
        if text.min_duration and duration < text.min_duration:
            raise MinDurationException(got=math.floor(duration), want=text.min_duration)
        elif text.max_duration and duration > text.max_duration:
            raise MaxDurationException(got=math.ceil(duration), want=text.max_duration)


    def _save_speech_file(self, rec: values.Recording, base_filename: str) -> pathlib.Path:
        filename = base_filename + (_VIDEO_EXT if rec.is_video else _AUDIO_EXT)
        path = settings.RECORDINGS_DIR / filename
        tmp_path = settings.RECORDINGS_DIR / ("tmp_" + filename)

        try:
            _save_input(rec.speech, tmp_path)
            self.media.re_encode(str(tmp_path), str(path))
        finally:
            os.remove(tmp_path)
        return path

    def _save_audio_from_video(self, video_path: pathlib.Path, base_filename: str) -> None:
        audio_filename = base_filename + _AUDIO_EXT
        audio_path = video_path.parent / audio_filename
        self.media.extract_audio(str(video_path), str(audio_path))

def _get_base_filename(user_id: str, text_id: str) -> str:
    return f'{user_id}_{text_id}.'


def _save_input(file: UploadedFile, path: str):
    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)



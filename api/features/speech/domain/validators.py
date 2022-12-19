import math

from . import exceptions, log, values
from .external.mediaencoder import MediaEncoder
from ... import text
from ...text import TextNotFound


class DurationValidator:
    def __init__(self, text: text.TextService, media: MediaEncoder):
        self._text = text
        self._media = media

    def validate_duration_and_log(self, rec: values.Recording, audio_path: str):
        try:
            self._validate_duration(rec.meta.text_id, audio_path)
        except exceptions.MinDurationException as e:
            log.log_min_duration_exception(rec, e)
            raise e
        except exceptions.MaxDurationException as e:
            log.log_max_duration_exception(rec, e)
            raise e

    def _validate_duration(self, text_id: str, media_path: str) -> None:
        text = self._text.find_text(text_id)
        if text is None: raise TextNotFound()
        duration = self._media.get_duration(media_path)
        if text.min_duration and duration < text.min_duration:
            raise exceptions.MinDurationException(got=math.floor(duration), want=text.min_duration)
        elif text.max_duration and duration > text.max_duration:
            raise exceptions.MaxDurationException(got=math.ceil(duration), want=text.max_duration)

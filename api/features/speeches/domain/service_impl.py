import os
from .service import SpeechesService
from . import values, log, validators
from api.features.speeches.domain.external.mediaencoder import MediaEncoder
from ...filepaths.domain.service import FilepathsService
from ...filepaths.domain.values import RecordingPaths, CompletionStatus


class SpeechesServiceImpl(SpeechesService):
    def __init__(self, filepaths: FilepathsService, media: MediaEncoder, validator: validators.DurationValidator):
        self._filepaths = filepaths
        self._media = media
        self._validator = validator

    def save_recording(self, rec: values.Recording) -> CompletionStatus:
        paths = self._filepaths.get_filepaths(rec.meta)
        self._cleanup(paths) # deletes the previous files
        try:
            self._encode_rec(rec, paths)
            self._validator.validate_duration_and_log(rec, str(paths.audio_path))
            log.log_success(rec)
        except Exception as e:
            self._cleanup(paths)
            raise e
        return self._filepaths.is_completed(rec.meta.text_id, rec.meta.by_user_id)

    def _encode_rec(self, rec: values.Recording, paths: RecordingPaths):
        self._media.re_encode(rec.tmp_blob_path, str(paths.audio_path))
        if rec.meta.is_video:
            self._media.re_encode(rec.tmp_blob_path, str(paths.video_path))

    def _cleanup(self, paths: RecordingPaths):
        try:
            os.remove(paths.audio_path)
            os.remove(paths.video_path)
        except FileNotFoundError:
            pass

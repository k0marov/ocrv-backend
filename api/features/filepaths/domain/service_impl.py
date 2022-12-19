import dataclasses
import os
import pathlib

from . import service, values

_VIDEO_EXT = 'mp4'
_AUDIO_EXT = 'wav'


@dataclasses.dataclass
class PathsConfig:
    texts_path: str
    recordings_dir: pathlib.Path

class FilepathsServiceImpl(service.FilepathsService):
    def __init__(self, paths: PathsConfig):
        self._paths = paths
    def get_texts_path(self) -> str:
        return self._paths.texts_path

    def get_filepaths(self, rec: values.RecordingMeta) -> values.RecordingPaths:
        return values.RecordingPaths(
            audio_path=self._get_filepath(dataclasses.replace(rec, is_video=False)),
            video_path=self._get_filepath(dataclasses.replace(rec, is_video=True)),
        )

    def is_completed(self, text_id: str, by_user_id: str):
        meta = values.RecordingMeta(
            text_id=text_id,
            by_user_id=by_user_id,
            is_video=False,
        )
        paths = self.get_filepaths(meta)
        return os.path.exists(paths.audio_path)

    def _get_filepath(self, rec: values.RecordingMeta) -> str:
        base = f'{rec.by_user_id}_{rec.text_id}.'
        filename = base + (_VIDEO_EXT if rec.is_video else _AUDIO_EXT)
        return str(self._paths.recordings_dir / filename)

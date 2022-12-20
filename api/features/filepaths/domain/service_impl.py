import dataclasses
import os
import pathlib
import typing

from . import service, values

_VIDEO_EXT = 'mp4'
_AUDIO_EXT = 'wav'


@dataclasses.dataclass
class PathsConfig:
    texts_path: str
    recordings_dir: pathlib.Path
    recordings_url: str

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

    def is_completed(self, text_id: str, by_user_id: str) -> typing.Optional[values.CompletionStatus]:
        meta = values.RecordingMeta(
            text_id=text_id,
            by_user_id=by_user_id,
            is_video=False,
        )
        paths = self.get_filepaths(meta)
        video_completion = self._get_completion(paths.video_path, is_video=True)
        if video_completion is not None: return video_completion
        return self._get_completion(paths.audio_path, is_video=False)

    def _get_completion(self, media_path: pathlib.Path, is_video: bool) -> typing.Optional[values.CompletionStatus]:
        exists = os.path.exists(media_path)
        if not exists: return None
        return values.CompletionStatus(
            url=self._get_url(media_path),
            is_video=True,
        )

    def _get_filepath(self, rec: values.RecordingMeta) -> pathlib.Path:
        base = f'{rec.by_user_id}_{rec.text_id}.'
        filename = base + (_VIDEO_EXT if rec.is_video else _AUDIO_EXT)
        return self._paths.recordings_dir / filename

    def _get_url(self, rec_path: pathlib.Path) -> str:
        return self._paths.recordings_url + str(rec_path.name)
import abc
import typing

from . import values


class FilepathsService(abc.ABC):
    @abc.abstractmethod
    def get_texts_path(self) -> str:
        pass

    @abc.abstractmethod
    def get_filepaths(self, rec: values.RecordingMeta) -> values.RecordingPaths:
        pass

    @abc.abstractmethod
    def is_completed(self, text_id: str, by_user_id: str) -> typing.Optional[values.CompletionStatus]:
        pass


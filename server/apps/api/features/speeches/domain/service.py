import abc

from .values import Recording


class SpeechesService(abc.ABC):
    @abc.abstractmethod
    def save_recording(self, rec: Recording) -> None:
        pass


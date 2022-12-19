import abc

from api.features.speech.domain import values


class SpeechService(abc.ABC):
    @abc.abstractmethod
    def save_recording(self, rec: values.Recording) -> None:
        pass


import abc

from api.features.speeches.domain import values


class SpeechesService(abc.ABC):
    @abc.abstractmethod
    def save_recording(self, rec: values.Recording) -> None:
        pass


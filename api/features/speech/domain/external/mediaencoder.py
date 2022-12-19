import abc


class MediaEncoder(abc.ABC):
    @abc.abstractmethod
    def re_encode(self, input: str, output: str): pass

    @abc.abstractmethod
    def get_duration(self, path: str) -> float: pass


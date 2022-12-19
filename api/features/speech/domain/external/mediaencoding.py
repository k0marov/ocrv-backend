import abc


class MediaEncoding(abc.ABC):
    @abc.abstractmethod
    def re_encode(self, input: str, output: str): pass

    @abc.abstractmethod
    def extract_audio(self, video_path: str, audio_path: str): pass

    @abc.abstractmethod
    def get_duration(self, path: str) -> float: pass


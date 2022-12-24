import ffmpeg

from ..domain.external.mediaencoder import MediaEncoder


class MediaEncoderImpl(MediaEncoder):
    def re_encode(self, input: str, output: str):
        ffmpeg.input(input).output(output).overwrite_output().run()

    def get_duration(self, path: str) -> float:
        meta = ffmpeg.probe(path)
        stream = meta['streams'][0]
        return float(stream['duration'])


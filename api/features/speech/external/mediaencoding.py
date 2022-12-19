import ffmpeg

from ..domain.external.mediaencoding import MediaEncoding


class MediaEncodingImpl(MediaEncoding):
    def re_encode(self, input: str, output: str):
        ffmpeg.input(input).output(output).overwrite_output().run()

    def extract_audio(self, video_path: str, audio_path: str):
        (
            ffmpeg
                .input(str(video_path))
                .output(str(audio_path))
                .overwrite_output()
                .run()
        )

    def get_duration(self, path: str) -> float:
        meta = ffmpeg.probe(path)
        stream = meta['streams'][0]
        return float(stream['duration'])


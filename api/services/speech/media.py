import ffmpeg
from django.core.files.uploadedfile import UploadedFile


def reencode(input: str, output: str):
    ffmpeg.input(input).output(output).overwrite_output().run()

def extract_audio(video_path: str, audio_path: str):
    (
        ffmpeg
            .input(str(video_path))
            .output(str(audio_path))
            .overwrite_output()
            .run()
    )

def get_duration(path: str) -> float:
    meta = ffmpeg.probe(path)
    stream = meta['streams'][0]
    return float(stream['duration'])


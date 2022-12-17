import os
import uuid

import ffmpeg
from django.core.files.uploadedfile import UploadedFile


def encode_and_save(media: UploadedFile, tmp_path: str, path: str):
    with open(tmp_path, 'wb+') as destination:
        for chunk in media.chunks():
            destination.write(chunk)
    ffmpeg.input(tmp_path).output(path).overwrite_output().run()
    os.remove(str(tmp_path))

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
    print(meta)
    stream = meta['streams'][0]
    return float(stream['duration'])


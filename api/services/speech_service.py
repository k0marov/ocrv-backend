from django.core.files.uploadedfile import UploadedFile

VIDEO_EXT = 'mp4'
AUDIO_EXT = 'wav'

def save_recording(user_id: int, text_id: str, speech: UploadedFile, is_video: bool) -> None:
    filename = f'{user_id}_{text_id}.' + VIDEO_EXT if is_video else AUDIO_EXT
    _save_speech_file(filename, speech)

def _save_speech_file(filename: str, speech: UploadedFile) -> None:
    with open(filename, 'wb+') as destination:
        for chunk in speech.chunks():
            destination.write(chunk)


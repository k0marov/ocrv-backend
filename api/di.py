import dataclasses

from ocrvBackendV2 import settings
from .features.filepaths.domain.service_impl import FilepathsServiceImpl, PathsConfig
from .features.speech import SpeechService
from .features.speech.domain.service_impl import SpeechServiceImpl
from .features.speech.domain.validators import DurationValidator
from .features.speech.external.mediaencoder import MediaEncoderImpl
from .features.text import TextService
from .features.text.domain.service_impl import TextServiceImpl
from .features.text.external.store import TextStoreImpl


@dataclasses.dataclass
class APIDependencies:
    text: TextService
    speech: SpeechService


def initialize():
    paths = PathsConfig(texts_path=settings.TEXTS_PATH, recordings_dir=settings.RECORDINGS_DIR)
    filepaths = FilepathsServiceImpl(paths)
    text = TextServiceImpl(filepaths, TextStoreImpl(settings.TEXTS_PATH))
    media = MediaEncoderImpl()
    speech = SpeechServiceImpl(filepaths, media, DurationValidator(text, media))
    return APIDependencies(
        text=text,
        speech=speech,
    )


deps = initialize()
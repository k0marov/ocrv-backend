import dataclasses

from ocrvBackendV2 import settings
from .features.filepaths.domain.service_impl import FilepathsServiceImpl, PathsConfig
from .features.speeches import SpeechesService
from .features.speeches.domain.service_impl import SpeechesServiceImpl
from .features.speeches.domain.validators import DurationValidator
from .features.speeches.external.mediaencoder import MediaEncoderImpl
from .features.texts import TextsService
from .features.texts.domain.service_impl import TextsServiceImpl
from .features.texts.external.store import TextsStoreImpl


@dataclasses.dataclass
class APIDependencies:
    text: TextsService
    speech: SpeechesService


def initialize():
    paths = PathsConfig(texts_path=settings.TEXTS_PATH, recordings_dir=settings.RECORDINGS_DIR)
    filepaths = FilepathsServiceImpl(paths)
    text = TextsServiceImpl(filepaths, TextsStoreImpl(settings.TEXTS_PATH))
    media = MediaEncoderImpl()
    speech = SpeechesServiceImpl(filepaths, media, DurationValidator(text, media))
    return APIDependencies(
        text=text,
        speech=speech,
    )


deps = initialize()
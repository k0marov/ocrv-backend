import dataclasses

from django.conf import settings
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
    texts: TextsService
    speeches: SpeechesService


def initialize() -> APIDependencies:
    paths = PathsConfig(texts_path=settings.TEXTS_PATH, recordings_dir=settings.RECORDINGS_DIR, recordings_url=settings.RECORDINGS_URL)
    filepaths = FilepathsServiceImpl(paths)
    text = TextsServiceImpl(filepaths, TextsStoreImpl(filepaths))
    media = MediaEncoderImpl()
    speech = SpeechesServiceImpl(filepaths, media, DurationValidator(text, media))
    return APIDependencies(
        texts=text,
        speeches=speech,
    )


deps = initialize()
import dataclasses

from .features.speech import SpeechService
from .features.text import TextService
from .features.text.domain.service_impl import TextServiceImpl


@dataclasses.dataclass
class Dependencies:
    text: TextService
    speech: SpeechService

import csv
import os
from typing import Optional, List

from api.features.speech import SpeechService
from api.features.text import TextService, TextsFileNotFound, NoTexts
from api.features.text.domain import values, log
from api.features.text.domain.external import models
from api.features.text.domain.external.store import TextStore
from ocrvBackendV2 import settings


class TextServiceImpl(TextService):
    def __init__(self, speech: SpeechService, store: TextStore):
        self.speech = speech
        self.store = store

    def get_texts(self, user_id: str) -> List[values.Text]:
        if not os.path.isfile(str(settings.TEXTS_PATH)):
            raise TextsFileNotFound()
        models_list = self.store.get_texts()
        if not models_list:
            raise NoTexts()
        return [values.Text(
            model=model,
            completed_by_caller=self.speech.has_recorded(user_id, model.id)
        ) for model in models_list]

    def find_text(self, text_id: str) -> Optional[models.TextModel]:
        texts = self.store.get_texts()
        text = None
        for t in texts:
            if t.id == text_id:
                text = t
        return text

    def skip_text(self, skip: values.SkipDTO) -> None:
        log.log_skip(skip)



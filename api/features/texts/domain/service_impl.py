from typing import Optional, List

from api.features.filepaths.domain.service import FilepathsService
from api.features.texts import TextsService, NoTexts
from api.features.texts.domain import values, log
from api.features.texts.domain.external import models
from api.features.texts.domain.external.store import TextsStore


class TextsServiceImpl(TextsService):
    def __init__(self, filepaths: FilepathsService, store: TextsStore):
        self._filepaths = filepaths
        self._store = store

    def get_texts(self, user_id: str) -> List[values.Text]:
        models_list = self._store.get_texts()
        if not models_list:
            raise NoTexts()
        return [values.Text(
            model=model,
            completed=self._filepaths.is_completed(text_id=model.id, by_user_id=user_id),
        ) for model in models_list]

    def find_text(self, text_id: str) -> Optional[models.TextModel]:
        texts = self._store.get_texts()
        for t in texts:
            if t.id == text_id:
                return t

    def skip_text(self, skip: values.SkipDTO) -> None:
        log.log_skip(skip)



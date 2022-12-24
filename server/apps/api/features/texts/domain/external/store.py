import abc
from typing import List

from apps.api.features.texts.domain.external import models


class TextsStore(abc.ABC):
    @abc.abstractmethod
    def get_texts(self) -> List[models.TextModel]: pass
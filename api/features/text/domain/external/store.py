import abc
from typing import List

from api.features.text.domain.external import models


class TextStore(abc.ABC):
    @abc.abstractmethod
    def get_texts(self) -> List[models.TextModel]: pass
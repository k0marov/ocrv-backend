import abc
from typing import List, Optional

from .external import models
from . import values

class TextsService(abc.ABC):
    @abc.abstractmethod
    def get_texts(self, user_id: str) -> List[values.Text]: pass
    @abc.abstractmethod
    def find_text(self, text_id: str) -> Optional[models.TextModel]: pass
    @abc.abstractmethod
    def skip_text(self, skip: values.SkipDTO) -> None: pass




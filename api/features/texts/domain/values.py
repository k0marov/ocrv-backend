import dataclasses

from .external import models
from ...filepaths.domain.values import CompletionStatus


@dataclasses.dataclass
class Text:
    model: models.TextModel
    completed: CompletionStatus

@dataclasses.dataclass
class SkipDTO:
    user_id: int
    text_id: str
    retries: int



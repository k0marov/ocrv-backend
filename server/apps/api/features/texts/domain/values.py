import dataclasses
import typing

from .external import models
from ...filepaths.domain.values import CompletionStatus


@dataclasses.dataclass
class Text:
    model: models.TextModel
    completed: typing.Optional[CompletionStatus]

@dataclasses.dataclass
class SkipDTO:
    user_id: int
    text_id: str
    retries: int



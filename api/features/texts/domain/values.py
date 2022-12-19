import dataclasses

from api.features.texts import models


@dataclasses.dataclass
class Text:
    model: models.TextModel
    completed_by_caller: bool

@dataclasses.dataclass
class SkipDTO:
    user_id: int
    text_id: str
    retries: int



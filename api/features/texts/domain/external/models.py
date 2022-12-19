import dataclasses
from typing import Optional


@dataclasses.dataclass
class TextModel:
    id: str
    text: str
    note: str
    min_duration: Optional[int] # in seconds
    max_duration: Optional[int] # in seconds

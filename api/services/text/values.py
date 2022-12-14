import dataclasses
from typing import List, Optional
@dataclasses.dataclass
class Text:
    id: str
    text: str
    note: str
    min_duration: Optional[int] # in seconds
    max_duration: Optional[int] # in seconds

@dataclasses.dataclass
class SkipDTO:
    user_id: int
    text_id: str
    retries: int



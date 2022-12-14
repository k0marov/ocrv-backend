import csv
import dataclasses
import os
from typing import List, Optional
from django.conf import settings
from . import api_logger

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


class TextsFileNotFound(Exception): pass
class NoTexts(Exception): pass

def get_texts() -> List[Text]:
    if not os.path.isfile(str(settings.TEXTS_PATH)):
        raise TextsFileNotFound()
    texts_list = _read_texts()
    if not texts_list:
        raise NoTexts()
    return texts_list

def _read_texts() -> List[Text]:
    texts_list = []
    with open(str(settings.TEXTS_PATH), 'r', encoding='utf-8', newline='') as file:
        texts_csv = csv.reader(file, delimiter='\t', skipinitialspace=True)
        next(texts_csv) # skip the header raw
        for row in texts_csv:
            texts_list.append(Text(
                id=row[0],
                text=row[1],
                note=row[2],
                min_duration=int(row[3]),
                max_duration=int(row[4]),
            ))
    return texts_list


def skip_text(skip: SkipDTO) -> None:
    api_logger.logger.info(f'Skipped text id: {skip.text_id}; retries: {skip.retries}; user: {skip.user_id}')
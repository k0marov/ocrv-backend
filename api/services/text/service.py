import csv
import os
from typing import List, Optional

from django.conf import settings

from . import values, log
from .exceptions import TextsFileNotFound, NoTexts


def get_texts() -> List[values.Text]:
    if not os.path.isfile(str(settings.TEXTS_PATH)):
        raise TextsFileNotFound()
    texts_list = _read_texts()
    if not texts_list:
        raise NoTexts()
    return texts_list

def find_text(text_id: str) -> Optional[values.Text]:
    texts = get_texts()
    text = None
    for t in texts:
        if t.id == text_id: text = t
    return text

def skip_text(skip: values.SkipDTO) -> None:
    log.log_skip(skip)

def _read_texts() -> List[values.Text]:
    texts_list = []
    with open(str(settings.TEXTS_PATH), 'r', encoding='utf-8', newline='') as file:
        texts_csv = csv.reader(file, delimiter='\t', skipinitialspace=True)
        next(texts_csv) # skip the header row
        for row in texts_csv:
            texts_list.append(_decode_csv_text(row))
    return texts_list

def _decode_csv_text(csv_row: List[str]) -> values.Text:
    min_duration = int(csv_row[3])
    max_duration = int(csv_row[4])

    return values.Text(
        id=csv_row[0],
        text=csv_row[1],
        note=csv_row[2],
        min_duration=min_duration if min_duration else None,
        max_duration=max_duration if max_duration else None,
    )


import csv
from typing import List

from api.features.filepaths.domain.service import FilepathsService
from api.features.text.domain.external import models
from api.features.text.domain.external.store import TextStore


class TextStoreImpl(TextStore):
    def __init__(self, filepaths: FilepathsService):
        self._filepaths = filepaths

    def get_texts(self) -> List[models.TextModel]:
        texts_list = []
        with open(self._filepaths.get_texts_path(), 'r', encoding='utf-8', newline='') as file:
            texts_csv = csv.reader(file, delimiter='\t', skipinitialspace=True)
            next(texts_csv)  # skip the header row
            for row in texts_csv:
                texts_list.append(_map_text(row))
        return texts_list

def _map_text(csv_row: List[str]) -> models.TextModel:
    min_duration = int(csv_row[3])
    max_duration = int(csv_row[4])

    return models.TextModel(
        id=csv_row[0],
        text=csv_row[1],
        note=csv_row[2],
        min_duration=min_duration if min_duration else None,
        max_duration=max_duration if max_duration else None,
    )


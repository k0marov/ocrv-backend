import csv
import os
from typing import Dict, List


class TextsFileNotFound(Exception): pass
class NoTexts(Exception): pass

def get_texts() -> List[Dict]:
    if not os.path.isfile('./texts.csv'):
        raise TextsFileNotFound()
    texts_list = _read_texts()
    if not texts_list:
        raise NoTexts()
    return texts_list

def _read_texts() -> List[Dict]:
    texts_list = []
    with open('texts.csv', 'r', encoding='utf-8', newline='') as file:
        texts_csv = csv.reader(file, delimiter='\t', skipinitialspace=True)
        for row in texts_csv[1:]:
            texts_list.append({'id': row[0], 'text': row[1], 'note': row[2]})
    return texts_list

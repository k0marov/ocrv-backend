import csv
import os
from typing import Dict, List

from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import UploadedFile


class TextsFileNotFound(Exception): pass
class NoTexts(Exception): pass


def get_texts() -> List[Dict]:
    texts_list = []
    if not os.path.isfile('./texts.csv'): raise TextsFileNotFound()

    with open('texts.csv', 'r', encoding='utf-8', newline='') as file:
        texts_csv = csv.reader(file, delimiter='\t', skipinitialspace=True)
        for row in texts_csv[1:]:
            texts_list.append({'id': row[0], 'text': row[1], 'note': row[2]})

    if not texts_list: raise NoTexts()

    return texts_list

def save_recording(text_id: str, speech: UploadedFile) -> None:
    filename = text_id + ".mp4"
    with open(filename) as f:
        FileSystemStorage(location="./recordings/").save(f, speech)

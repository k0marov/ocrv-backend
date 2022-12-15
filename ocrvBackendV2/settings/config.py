import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

load_dotenv()

def _get_env(key: str) -> str:
    val = os.getenv(key)
    if not val: raise ImproperlyConfigured(f'Please specify {key} as an environment variable.')
    return val

SECRET_KEY = _get_env('OCRV_RECORDER_SECRET_KEY')
TEXTS_PATH = Path(_get_env('OCRV_RECORDER_TEXTS_PATH')).resolve()
LOG_PATH = Path(_get_env('OCRV_RECORDER_LOG_PATH')).resolve()
RECORDINGS_DIR = Path(_get_env('OCRV_RECORDER_RECORDINGS_DIR')).resolve()
import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

load_dotenv()

def _get_env(key: str) -> str:
    val = os.getenv(key)
    print(key, '=', val)
    if not val: raise ImproperlyConfigured(f'Please specify {key} as an environment variable.')
    return val


DEBUG = _get_env("OCRV_RECORDER_DEBUG") == "1"

SECRET_KEY = _get_env('OCRV_RECORDER_SECRET_KEY')

TEXTS_PATH = Path(_get_env('OCRV_RECORDER_TEXTS_PATH')).resolve()
LOG_PATH = Path(_get_env('OCRV_RECORDER_LOG_PATH')).resolve()
RECORDINGS_DIR = Path(_get_env('OCRV_RECORDER_RECORDINGS_DIR')).resolve()
DB_PATH = Path(_get_env('OCRV_RECORDER_DB_PATH')).resolve()

RECORDINGS_URL = _get_env('OCRV_RECORDER_RECORDINGS_URL')

STATIC_URL = _get_env('OCRV_RECORDER_STATIC_URL')
STATIC_ROOT = Path(_get_env('OCRV_RECORDER_STATIC_ROOT')).resolve()

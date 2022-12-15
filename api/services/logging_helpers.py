from . import text, speech
from common.logger import logger


def log_success(rec: speech.Recording):
    logger.info(f"Success text id: {rec.text_id}; retries: {rec.retries}; user {rec.user_id}")

def log_skip(skip: text.SkipDTO):
    logger.info(f'Skipped text id: {skip.text_id}; retries: {skip.retries}; user: {skip.user_id}')

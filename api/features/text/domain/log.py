from api.features.text import SkipDTO
from common.logger import logger


def log_skip(skip: SkipDTO):
    logger.info(f'Skipped text id: {skip.text_id}; retries: {skip.retries}; user: {skip.user_id}')

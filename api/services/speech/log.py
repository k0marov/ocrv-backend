from api.services.speech import Recording
from common.logger import logger

def log_success(rec: Recording):
    logger.info(f"Success text id: {rec.text_id}; retries: {rec.retries}; user {rec.user_id}")

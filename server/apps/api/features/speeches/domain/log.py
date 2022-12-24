from apps.common.logger import logger
from .values import Recording
from .exceptions import MinDurationException, MaxDurationException

def log_success(rec: Recording):
    logger.info(f"Success text id: {rec.meta.text_id}; retries: {rec.retries}; user {rec.meta.by_user_id}")

def log_min_duration_exception(rec: Recording, e: MinDurationException):
    logger.info(f"MinDurationException got: {e.got}; want {e.want} text id: {rec.meta.text_id}; retries: {rec.retries}; user {rec.meta.by_user_id}")

def log_max_duration_exception(rec: Recording, e: MaxDurationException):
    logger.info(f"MaxDurationException got: {e.got}; want {e.want} text id: {rec.meta.text_id}; retries: {rec.retries}; user {rec.meta.by_user_id}")

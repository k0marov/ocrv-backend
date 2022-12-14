import logging

_log_format = f"%(asctime)s - %(message)s"


def _get_file_handler():
    file_handler = logging.FileHandler("./logs.log", 'w', 'utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(_log_format, datefmt='%Y-%m-%d %H:%M:%S'))
    return file_handler


def _get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(_log_format, datefmt='%Y-%m-%d %H:%M:%S'))
    return stream_handler


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(_get_file_handler())
    logger.addHandler(_get_stream_handler())
    return logger

logger = api_logger.get_logger(__name__)

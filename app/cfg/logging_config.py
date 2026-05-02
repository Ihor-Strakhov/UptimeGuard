import logging


LOG_FORMAT = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"

LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt=LOG_DATE_FORMAT,
    force=True,
)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

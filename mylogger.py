import logging
from datetime import date
from constants import (
    LOGGER_FILE_EXTENSION,
    LOGGER_DEFAULT_FORMAT,
    LOGGER_DEFAULT_DATETIME_FORMAT,
)


class MyLogger:
    @staticmethod
    def getLogger(logger_name: str) -> logging.Logger:
        logger = logging.getLogger(logger_name)
        return logger

    @staticmethod
    def setLoggingConfig(
        logger_format: str = LOGGER_DEFAULT_FORMAT,
        logger_level: int = logging.DEBUG,
        logger_datetime_format: str = LOGGER_DEFAULT_DATETIME_FORMAT,
        logger_file_path: str = "./logs/orh{}log.{}".format(
            date.today(), LOGGER_FILE_EXTENSION
        ),
    ) -> None:
        logging.basicConfig(
            filename=logger_file_path,
            level=logger_level,
            datefmt=logger_datetime_format,
            format=logger_format,
        )

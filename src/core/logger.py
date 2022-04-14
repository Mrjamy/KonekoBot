"""
Module to bootstrap the loggers.
"""

# Builtins
import logging
from logging.handlers import TimedRotatingFileHandler


LOGGER_FORMAT: str = '%(asctime)-15s - [%(process)-6s] %(levelname)-8s - %(name)s - %(message)s'


class Logger:
    """Logging class to setup logging for all used modules."""

    def __init__(self):
        for module, level in {
                'koneko': logging.DEBUG,
                'discord': logging.CRITICAL,
                'asyncio': logging.CRITICAL
        }.items():
            self.file_logger(module, level)
            self.std_err_logger(module, level)

    @staticmethod
    def file_logger(module: str, level: int):
        """Template function for all loggers."""
        logger = logging.getLogger(module)
        logger.setLevel(level)
        logger_handler = TimedRotatingFileHandler(f'logs/{module}.log', when='d', interval=1, backupCount=5)
        logger_format = LOGGER_FORMAT
        logger_formatter = logging.Formatter(logger_format)
        logger_handler.setFormatter(logger_formatter)
        logger.addHandler(logger_handler)

    @staticmethod
    def std_err_logger(module: str, level: int):
        """Template function for all loggers."""
        logger = logging.getLogger(module)
        logger.setLevel(level)
        logger_format = LOGGER_FORMAT
        logger_formatter = logging.Formatter(logger_format)
        logger_handler = logging.StreamHandler()
        logger_handler.setFormatter(logger_formatter)
        logger.addHandler(logger_handler)

"""
Module to bootstrap the loggers.
"""

# Builtins
import logging


class Logging:
    """Logging class to setup logging for all used modules."""

    def __init__(self):
        for module, level in {
                'koneko': logging.DEBUG,
                'discord': logging.CRITICAL,
                'asyncio': logging.CRITICAL
        }.items():
            self.file_logger(module, level)

    @staticmethod
    def file_logger(module: str, level: int):
        """Template function for all loggers."""
        logger = logging.getLogger(module)
        logger.setLevel(level)
        logger_file_handler = logging.FileHandler(f'logs/{module}.log')
        logger_format = '%(asctime)-15s - [%(process)-6s] %(levelname)-8s - %(name)s - %(message)s'
        logger_formatter = logging.Formatter(logger_format)
        logger_file_handler.setFormatter(logger_formatter)
        logger.addHandler(logger_file_handler)

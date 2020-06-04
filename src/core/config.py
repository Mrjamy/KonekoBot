"""
Module containing config related entries.
"""

# Builtins
import logging
from typing import List

module_logger = logging.getLogger('koneko.Settings')


class Settings:
    """Settings class"""
    __slots__ = ('_toggle_extensions', '_core_extensions')

    @property
    def toggle_extensions(self) -> List[str]:
        """Optional extensions for Koneko."""
        return [
            "admin",
            # "adminstration",
            # "alert",
            "currency",
            # "dnd",
            "gambling",
            "games",
            "general",
            "help",
            "level",
            # "stats",
            "utility",
        ]

    @property
    def core_extensions(self) -> List[str]:
        """Core extensions for Koneko."""
        return [
            "ErrorHandler",
            "EventListener",
            "HotReload"
        ]

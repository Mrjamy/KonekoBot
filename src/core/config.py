"""
Module containing config related entries.
"""

# Builtins
import logging

module_logger = logging.getLogger('koneko.Settings')


class Settings:
    """Settings class"""
    __slots__ = 'dry_run', 'toggle_extensions', 'core_extensions'

    def __init__(self):
        self.toggle_extensions = [
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
        self.core_extensions = [
            "ErrorHandler",
            "EventListener",
            "HotReload"
        ]

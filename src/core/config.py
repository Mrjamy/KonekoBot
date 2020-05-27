"""
Module containing config related entries.
"""

# Builtins
import logging
import argparse

module_logger = logging.getLogger('koneko.Settings')


class Settings:
    """Settings class"""
    __slots__ = 'dry_run', 'toggle_extensions', 'core_extensions'

    def __init__(self):
        parser = argparse.ArgumentParser()

        parser.add_argument("-d", "--dry-run", dest="boot_only", default=0)

        args = parser.parse_args()

        self.dry_run = bool(int(args.boot_only))
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

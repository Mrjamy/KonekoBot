"""
Util module to generate somewhat random images.
"""

# Builtins
import logging
import os
import random

module_logger = logging.getLogger('koneko.Games')


class ImageProvider:
    """Image provider"""
    __slots__ = 'local_dir', 'external_dir'

    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), '..', '..')

        self.local_dir = os.path.join(rf'{path}', 'core', 'images')
        self.external_dir = r'https://raw.githubusercontent.com/mrjamy/KonekoBot/master/src/core/images/'

    def image(self, query: str) -> str:
        """Provide an absolute link to an image in str format."""
        local_dir = os.path.join(self.local_dir, query)
        remote_dir = rf'{self.external_dir}{query}'

        filename = random.choice([
            file for file in os.listdir(local_dir)
            if os.path.isfile(os.path.join(local_dir, file))
        ])

        return rf'{remote_dir}/{filename}'

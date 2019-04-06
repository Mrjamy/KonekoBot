# Builtins
import os
import random


class ImageGenerator:
    __slots__ = ['local_dir', 'external_dir', 'tag']

    def __init__(self, tag: str):
        path = os.path.join(os.path.dirname(__file__), '..', '..')

        self.local_dir = os.path.join(rf'{path}', 'core', 'images')
        self.external_dir = rf'https://raw.githubusercontent.com/jmuilwijk/KonekoBot/development/src/core/images/'
        self.tag = tag

    def to_image(self):
        return self.__image(self.tag)

    def __image(self, query: str):
        local_dir = os.path.join(self.local_dir, query)
        remote_dir = rf'{self.external_dir}{query}'

        filename = random.choice([
            file for file in os.listdir(local_dir)
            if os.path.isfile(os.path.join(local_dir, file))
        ])

        return rf'{remote_dir}/{filename}'

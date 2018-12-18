import os
import random


class ImageGenerator:
    __slots__ = 'data_dir'

    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), '..', '..')
        self.data_dir = os.path.join(rf'{path}', 'core', 'images')

    def pat(self):
        return self.__image(query='pat')

    def hug(self):
        return self.__image(query='hug')

    def __image(self, query: str):
        path = os.path.join(self.data_dir, query)
        r_dir = rf'https://raw.githubusercontent.com/jmuilwijk/KonekoBot/development/src/core/images/{query}'

        random_filename = random.choice([
            x for x in os.listdir(path)
            if os.path.isfile(os.path.join(path, x))
        ])

        return rf'{r_dir}/{random_filename}'

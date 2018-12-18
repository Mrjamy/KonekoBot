import os
import random


class ImageGenerator:
    __slots__ = 'data_dir'

    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), '..', '..')
        self.data_dir = os.path.join(rf'{path}', 'core', 'images')

    def pat(self):
        path = os.path.join(self.data_dir, 'pat')

        random_filename = random.choice([
            x for x in os.listdir(path)
            if os.path.isfile(os.path.join(path, x))
        ])

        return os.path.join(path, random_filename)

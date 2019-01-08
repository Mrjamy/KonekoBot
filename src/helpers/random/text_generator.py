import os
import json
import random


class TextGenerator:
    __slots__ = ['dir', 'tag']

    def __init__(self, tag: str):
        self.dir = os.path.join(os.path.dirname(__file__), 'data')
        self.tag = tag

    def to_str(self):
        return self.__string(self.tag)

    def __string(self, query: str):
        try:
            with open(os.path.join(self.dir, f'{query}.json'), 'r') as f:
                phrases = json.load(f)
            return random.choice(phrases)
        except (IOError, FileNotFoundError):
            return 'Not found :sob:'

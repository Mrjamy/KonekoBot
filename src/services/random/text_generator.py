import os
import json
import random


class TextGenerator:
    __slots__ = 'data_dir'

    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')

    def greet(self):
        with open(os.path.join(self.data_dir, 'greet_phrases.json'), 'r') as f:
            phrases = json.load(f)

        return random.choice(phrases)

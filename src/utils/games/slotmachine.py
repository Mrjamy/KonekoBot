# Builtins
import os
import random
import time
from collections import Counter, namedtuple


Fruit = namedtuple('Fruit', ['name', 'weight', 'reward', 'pos'])


class Slots:

    __slots__ = 'slots', 'bet', 'fruits', 'msg', 'win'

    def __init__(self, bet: int = 10):
        self.bet = bet
        self.fruits = [
            Fruit(name='apple', weight=10000, reward=1, pos=0),
            Fruit(name='banana', weight=7000, reward=1.5, pos=1),
            Fruit(name='lemon', weight=5000, reward=2, pos=2),
            Fruit(name='grapes', weight=4000, reward=4, pos=3),
            Fruit(name='cherries', weight=3000, reward=6, pos=4),
            Fruit(name='bell', weight=2000, reward=10, pos=5),
            Fruit(name='seven', weight=500, reward=100, pos=6),
        ]

    def _play_round(self):
        weights = [fruit.weight for fruit in self.fruits]
        selected_fruits = random.choices(self.fruits, k=3, weights=weights)
        fruit_a, fruit_b, fruit_c = selected_fruits
        self.slots = f":{self.fruits[fruit_a.pos].name}: :{self.fruits[fruit_b.pos].name}: :{self.fruits[fruit_c.pos].name}:"
        return self._pay_out(selected_fruits)

    def _pay_out(self, fruits: list):
        most_common, count = (Counter(fruits).most_common(n=1)[0])
        if count == 1:
            self.win = 0
            self.msg = f"You lost {self.bet} <:neko:521458388513849344>"
        elif count == 2:
            self.win = (self.bet * most_common.reward) / 5
            self.msg = f"You won {self.win} <:neko:521458388513849344>"
        else:
            self.win = self.bet * most_common.reward
            self.msg = f"You won {self.win} <:neko:521458388513849344>"

    def play(self, credit: int, bet: int = 1):
        slotMachine = Slots(bet=bet)

        credit -= bet
        slotMachine._play_round()
        credit += slotMachine.win

        print(slotMachine.slots)
        print(slotMachine.msg)
        print(f"credit is {credit}")


if __name__ == '__main__':
    round = Slots().play(1000000, 1000000)

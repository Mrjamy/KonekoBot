# Builtins
import logging
import random
from collections import Counter, namedtuple

module_logger = logging.getLogger('koneko.Slots')
Fruit = namedtuple('Fruit', ['name', 'weight', 'reward', 'pos'])


class Slots(object):
    """Slotmachine class"""

    __slots__ = 'slots', 'bet', 'fruits', 'msg', 'win'

    def __init__(self, bet: int = 10):
        self.bet = bet
        self.fruits = [
            Fruit(name='apple', weight=100, reward=1.1, pos=0),
            Fruit(name='lemon', weight=50, reward=2.2, pos=1),
            Fruit(name='grapes', weight=40, reward=4.4, pos=2),
            Fruit(name='cherries', weight=30, reward=6.6, pos=3),
            Fruit(name='bell', weight=20, reward=11, pos=4),
            Fruit(name='seven', weight=5, reward=110, pos=5),
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
            self.win = self.bet * most_common.reward * 0.8
            self.msg = f"You won {self.win} <:neko:521458388513849344>"
        else:
            self.win = self.bet * most_common.reward
            self.msg = f"You won {self.win} <:neko:521458388513849344>"
        self.win = round(self.win, 2)

    @staticmethod
    def play(credit: int, bet: int = 1):
        slot_machine = Slots(bet=bet)

        credit -= bet
        slot_machine._play_round()
        credit += slot_machine.win

        module_logger.debug(slot_machine.slots)
        module_logger.debug(slot_machine.msg)
        module_logger.debug(f"credit is {credit}")


if __name__ == '__main__':
    Slots().play(1000000, 1000000)

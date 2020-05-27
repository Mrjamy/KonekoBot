"""
Slotmachine module.
"""

# Builtins
import logging
import random
from collections import Counter, namedtuple

module_logger = logging.getLogger('koneko.Slots')
Fruit = namedtuple('Fruit', ['name', 'weight', 'reward', 'pos'])


class Slots:
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
        self.slots = ""

    def play_round(self) -> None:
        """Play a round of slots"""
        weights = [fruit.weight for fruit in self.fruits]
        selected_fruits = random.choices(self.fruits, k=3, weights=weights)
        fruit_a, fruit_b, fruit_c = selected_fruits
        self.slots = f":{self.fruits[fruit_a.pos].name}: :{self.fruits[fruit_b.pos].name}: :{self.fruits[fruit_c.pos].name}:"
        return self._pay_out(selected_fruits)

    def _pay_out(self, fruits: list) -> None:
        """Payout helper function"""
        most_common, count = (Counter(fruits).most_common(n=1)[0])
        if count == 1:
            self.win = 0
            self.msg = f"You lost {self.bet} <:neko:521458388513849344>"
        elif count == 2:
            self.win = round(self.bet * most_common.reward * 0.8)
            self.msg = f"You won {self.win} <:neko:521458388513849344>"
        else:
            self.win = round(self.bet * most_common.reward)
            self.msg = f"You won {self.win} <:neko:521458388513849344>"


if __name__ == '__main__':
    credit = 100

    slot_machine = Slots(bet=10)

    credit -= slot_machine.bet
    slot_machine.play_round()
    credit += slot_machine.win

    print(slot_machine.slots)
    print(slot_machine.msg)
    print(f"credit is {credit}")

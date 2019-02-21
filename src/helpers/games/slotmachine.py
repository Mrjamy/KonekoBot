import random
import time
import os
from enum import Enum


class SlotMachine:

    __slots__ = 'current_stake', 'current_jackpot'

    class Reel(Enum):
        CHERRY = 1
        LEMON = 2
        ORANGE = 3
        PLUM = 4
        BELL = 5
        BAR = 6
        SEVEN = 7

    _values = list(Reel)
    payout = {
        Reel.CHERRY: 7,
        Reel.LEMON: 7,
        Reel.ORANGE: 10,
        Reel.PLUM: 14,
        Reel.BELL: 20,
        Reel.BAR: 250,
        Reel.SEVEN: 'jackpot'
    }

    message = list()

    def __init__(self):
        self.current_jackpot = 1000  # TODO: get jackpot from cache or DB

    def _play_round(self):
        first, second, third = random.choice(SlotMachine._values), random.choice(SlotMachine._values), random.choice(SlotMachine._values)
        return self._adjust_score(first, second, third)

    def _adjust_score(self, first, second, third):
        if first == SlotMachine.Reel.CHERRY:
            if second == SlotMachine.Reel.CHERRY:
                return 7 if third == SlotMachine.Reel.CHERRY else 5
            else:
                return 2
        else:
            if first == second == third:
                win = SlotMachine.payout[first]
                return self.current_jackpot if win == 'jackpot' else win
            else:
                return -1

        if win == self.current_jackpot:
            self.message.append("You won the JACKPOT!!")
        else:
            self.message.append('\t'.join(map(lambda x: x.name.center(6), (first, second, third))))
            self.message.append("You {} £{}".format("won" if win > 0 else "lost", win))
            self.current_jackpot -= win

    def play(self, credit: int, bet: int = 1):
        credit += bet * self._play_round()

        for _ in self.message:
            print(_)
        print(f"credit is {credit}")


if __name__ == '__main__':
    SlotMachine().play(1000, 10)

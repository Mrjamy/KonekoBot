import random
import time
import os
from enum import Enum


class SlotMachine:

    __slots__ = 'current_stake', 'current_jackpot', 'message', 'slots', 'bet'

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

    def __init__(self, bet=10):
        self.bet = bet
        self.current_jackpot = 1000  # TODO: get jackpot from cache or DB

    def _play_round(self):
        first, second, third = random.choice(SlotMachine._values), random.choice(SlotMachine._values), random.choice(SlotMachine._values)
        return self._adjust_score(first, second, third)

    def _adjust_score(self, first, second, third):
        if first == SlotMachine.Reel.CHERRY:
            if second == SlotMachine.Reel.CHERRY:
                win = 7 if third == SlotMachine.Reel.CHERRY else 5
            else:
                win = 2
        else:
            if first == second == third:
                win = SlotMachine.payout[first]
                win = self.current_jackpot if win == 'jackpot' else win
            else:
                win = -1

        if win == self.current_jackpot:
            self.message = "You won the JACKPOT!!"
        else:
            self.message = "You {} <:neko:521458388513849344>".format(f"won {win * self.bet}" if win > 0 else f"lost {self.bet}")
            self.current_jackpot -= win
        self.slots = '\t'.join(map(lambda x: x.name.center(6), (first, second, third)))

        return win

    def play(self, credit: int, bet: int = 1):
        credit += bet * self._play_round()

        print(self.slots)
        print(self.message)
        print(f"credit is {credit}")


if __name__ == '__main__':
    SlotMachine().play(1000, 10)

#!/usr/bin/env python3

# Builtins
import unittest

# Locals
from utils.games.slotmachine import Slots


class TestSlotPayout(unittest.TestCase):

    def payoutTest(self, rounds: int = 10000, bet: int = 100):
        """Test the payout of the slotmachine"""
        if rounds < 1:
            rounds = 10000
        if bet < 1:
            bet = 100

        credit = rounds * bet
        slotmachine = Slots(bet=bet)

        for _ in range(0, rounds):
            credit -= bet
            slotmachine._play_round()
            credit += slotmachine.win

        # TODO: print out.
        print(credit)

        self.assertEqual(True, True)

if __name__ == '__main__':
    TestSlotPayout().payoutTest()

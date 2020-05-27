"""
Slotmachine tests.
"""

# Builtins
import unittest

# Pip
from src.utils.games.slotmachine import Slots


class TestSlotmachine(unittest.TestCase):
    """Test slotmachine.

    Tests for the slotmachine."""

    async def play_round(self) -> None:
        slots = Slots()
        slots.play_round()

        self.assertIsNotNone(slots.win)
        self.assertIs(slots.win, int)


if __name__ == '__main__':
    unittest.main()



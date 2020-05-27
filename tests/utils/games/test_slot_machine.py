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

    def test_play_round(self) -> None:
        """Tests playing a round of slots."""
        slots = Slots()
        slots.play_round()

        self.assertIsNotNone(slots.win)
        self.assertIs(type(slots.win), int)


if __name__ == '__main__':
    unittest.main()

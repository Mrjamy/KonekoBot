"""Module containing tests regarding src.cogs.general"""

# Builtins
import unittest

# Pip
import discord

# Locals
from src.cogs.general import General, setup
from tests import is_valid_url
from tests.mock_objects import MockBot, MockContext, MockUser


class GeneralCogTests(unittest.IsolatedAsyncioTestCase):
    """Tests for the general cog."""

    def setUp(self):
        self.bot = MockBot()
        self.cog = General(self.bot)
        self.ctx = MockContext()
        self.user = MockUser()

    async def test_ping(self):
        """Ping command test."""
        # Ensure the mock is clean.
        self.ctx.reset_mock()
        self.bot.latency = 0.1

        # pylint: disable=too-many-function-args
        await self.cog.ping(self.cog, self.ctx)

        self.ctx.channel.send.assert_called_once_with(
            f"{str(round(self.bot.latency * 1000))} ms")

    async def test_hug(self):
        """Multipurpose interaction command test."""
        for invoked_with in ["hug", "pat", "kiss", "slap", "lewd", "respect"]:
            self.ctx.reset_mock()
            with self.subTest(invoked_with=invoked_with):
                self.ctx.invoked_with = invoked_with

                # pylint: disable=too-many-function-args
                embed = await self.cog.hug(self.cog, self.ctx, [self.user])

                self.assertEqual(embed.colour, discord.Color.dark_purple())
                self.assertTrue(is_valid_url(embed.image.url))


class GeneralCogSetupTests(unittest.TestCase):
    """Tests setup of the `general` cog."""

    @staticmethod
    def test_setup():
        """Setup of the extension should call add_cog."""
        bot = MockBot()
        setup(bot)
        bot.add_cog.assert_called_once()

"""
Module containing event-listeners.
"""

# Builtins
import logging

# Pip
import configparser
import discord
from discord.ext import commands

config = configparser.ConfigParser()
config.read('config.ini')
module_logger = logging.getLogger('koneko.EventListener')


class EventListener(commands.Cog):
    """Class that listens to events dispatched by dpy."""

    __slots__ = ('bot',)

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """KonekoBot on_ready event."""
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{config.get('Koneko', 'prefix')}h for help"
            )
        )
        # Bot logged in.
        module_logger.debug('Logged in as {}', self.bot.user)
        module_logger.debug('I am in {} guilds.', len(self.bot.guilds))

    @commands.Cog.listener()
    async def on_command(self, _ctx):
        """on_command event to keep track of executed commands."""
        self.bot.command_count += 1


def setup(bot) -> None:
    """The setup function to add this cog to Koneko."""
    bot.add_cog(EventListener(bot))

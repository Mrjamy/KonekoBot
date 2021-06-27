"""
Module containing utility commands.
"""

# Builtins
import logging
from datetime import datetime, timedelta
from time import time

# Pip
from discord.ext import commands

# Locals
from src.utils.general import DiscordEmbed

module_logger = logging.getLogger('koneko.Games')


class Utility(commands.Cog):
    """Utility commands."""

    __slots__ = 'bot', 'prefix_repository'

    def __init__(self, bot):
        self.bot = bot

    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
    async def stats(self, ctx) -> None:
        """Returns current statistics of the bot."""

        seconds = round(time() - self.bot.uptime)

        sec = timedelta(seconds=seconds)
        d = datetime(1, 1, 1) + sec

        parts = []

        for stat, value in {
                'uptime': f"{d.day - 1:d}d {d.hour}h {d.minute}m {d.second}s",
                'guilds': str(len(self.bot.guilds)),
                'members': str(len(list(self.bot.get_all_members()))),
                'command_count': self.bot.command_count + 1
        }:
            parts.append({
                {
                    'name': stat,
                    'value': value,
                    'inline': True
                }
            })

        await DiscordEmbed.message(ctx, parts, title="Koneko's Statistics")


def setup(bot) -> None:
    """The setup function to add this cog to Koneko."""
    bot.add_cog(Utility(bot))

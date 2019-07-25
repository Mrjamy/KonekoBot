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
    __slots__ = 'bot'

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """KonekoBot on_ready event."""
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{config.get('Koneko', 'prefix')}h for help"
            )
        )
        # Bot logged in.
        module_logger.debug(f'Logged in as {self.bot.user}')
        module_logger.debug(f'I am in {len(self.bot.guilds)} guilds.')

    @commands.Cog.listener()
    async def on_command(self, ctx):
        self.bot.command_count += 1


def setup(bot):
    bot.add_cog(EventListener(bot))

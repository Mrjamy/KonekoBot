# Builtins
import aiohttp
import asyncio
import logging

# Pip
import configparser
import dbl
import discord
from discord.ext import commands

module_logger = logging.getLogger('koneko.DBL')


class DiscordBotsOrgAPI(commands.Cog):
    """Handles interactions with the discordbots.org API"""

    def __init__(self, bot):
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.bot = bot
        self.token = config.get('DBL', 'dbl_token')
        self.dblpy = dbl.Client(self.bot, self.token)
        self.bot.loop.create_task(self.update_stats())

    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count"""

        while True:
            module_logger.info('attempting to post server count')
            try:
                await self.dblpy.post_guild_count()
                module_logger.info('posted server count ({})'.format(len(self.bot.guilds)))
            except Exception as e:
                module_logger.exception(f"Failed to post server count\n {type(e).__name__}: {e}")
            await asyncio.sleep(1800)


def setup(bot):
    bot.add_cog(DiscordBotsOrgAPI(bot))

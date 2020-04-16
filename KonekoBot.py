#!/usr/bin/env python3

# Builtins
import asyncio
import sys
import time
import traceback
import logging

# Pip
import configparser
import discord
from discord.ext import commands

# Locals
from src.core.config import Settings
from src.utils.database.db import run
from src.utils.database.repositories.prefix_repository import PrefixRepository


if sys.version_info < (3, 6):
    raise ImportError("Python 3.6 or greater is required")


loop = asyncio.get_event_loop()
settings = Settings()
config = configparser.ConfigParser()
config.read('config.ini')
# Add a file logger to koneko
logger = logging.getLogger('koneko')
logger.setLevel(logging.DEBUG)
loggerFileHandler = logging.FileHandler('koneko.log')
loggerFormat = '%(asctime)-15s - [%(process)-6s] %(levelname)-8s - %(name)s - %(message)s'
loggerFormatter = logging.Formatter(loggerFormat)
loggerFileHandler.setFormatter(loggerFormatter)
logger.addHandler(loggerFileHandler)


async def _prefix(bot, msg):
    user_id = bot.user.id
    prefix = [f'<@!{user_id}> ', f'<@{user_id}> ']
    if msg.guild is None:
        prefix.append('$')
    else:
        guild_prefix = await PrefixRepository().get(msg.guild)
        prefix.extend(guild_prefix)
    return prefix


class Koneko(commands.AutoShardedBot):
    """Auto sharded discord bot."""

    __slots__ = 'uptime', 'command_count', 'dry_run', 'settings', 'db', 'logger'

    # Create an AutoSharded bot.
    def __init__(self):
        super().__init__(
            command_prefix=_prefix,
            owner_id=180640710217826304,
        )
        self.uptime = time.time()
        self.command_count = 0
        self.dry_run = settings.dry_run
        self.settings = settings
        self.db = loop.run_until_complete(run())

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if self.user in message.mentions:
            try:
                await message.add_reaction("\N{EYES}")
            except discord.HTTPException:
                pass
        await self.process_commands(message)

    async def start(self, token):
        await self.login(token, bot=True)
        await self.connect(reconnect=True)

    async def logout(self):
        await super().logout()
        exit(0)

    def run(self):
        try:
            self.loop.run_until_complete(self.start(config.get('Koneko', 'token')))
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.logout())


if __name__ == '__main__':
    KonekoBot = Koneko()

    try:
        for cog in KonekoBot.settings.toggle_extensions:
            KonekoBot.load_extension(f"src.cogs.{cog}")
        for cog in KonekoBot.settings.core_extensions:
            KonekoBot.load_extension(f"src.core.{cog}")
    except ImportError as error:
        logger.error(traceback.print_tb(error))
        exit(1)
    KonekoBot.load_extension("jishaku")

    # Dry run option for travis.
    if KonekoBot.dry_run is True:
        logger.debug("Quitting: dry run")
        exit(0)

    logger.debug("Logging into Discord...")
    KonekoBot.run()

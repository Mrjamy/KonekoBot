#!/usr/bin/env python3

# Builtins
import asyncio
import configparser
import logging
import sys
import time
import traceback
from typing import List

# Pip
import discord
from discord.ext import commands

# Locals
from src.core.config import Settings
from src.core.logging import Logging
from src.utils.database.db import run
from src.utils.database.repositories.prefix_repository import PrefixRepository

if sys.version_info < (3, 6):
    raise ImportError("Python 3.6 or greater is required")

# Setup module logging.
Logging()
module_logger = logging.getLogger('koneko')


async def _prefix(bot, msg) -> List[str]:
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

    __slots__ = 'uptime', 'command_count', 'dry_run', 'settings', 'db', \
                'logger', 'loop'

    # Create an AutoSharded bot.
    def __init__(self):
        super().__init__(
            command_prefix=_prefix,
            owner_id=180640710217826304,
            help_command=None,
        )
        self.uptime = time.time()
        self.command_count = 0
        self.dry_run = sys.argv[1] if len(sys.argv) > 1 else 0
        self.settings = Settings()

    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        if self.user in message.mentions:
            try:
                await message.add_reaction("\N{EYES}")
            except discord.HTTPException:
                pass
        await self.process_commands(message)

    async def start(self, token) -> None:
        await self.login(token, bot=True)
        await self.connect(reconnect=True)

    async def logout(self) -> None:
        await super().logout()
        exit(0)

    @property
    def config(self) -> configparser.ConfigParser:
        config = configparser.ConfigParser()
        config.read('config.ini')

        return config

    def run(self) -> None:
        try:
            self.loop.run_until_complete(self.start(config.get('Koneko',
                                                               'token')))
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.logout())


if __name__ == '__main__':
    # Get the current asyncio event loop.
    loop = asyncio.get_event_loop()
    # Add database connection to the event loop.
    loop.run_until_complete(run())

    KonekoBot = Koneko()

    try:
        for cog in KonekoBot.settings.toggle_extensions:
            KonekoBot.load_extension(f"src.cogs.{cog}")
        for cog in KonekoBot.settings.core_extensions:
            KonekoBot.load_extension(f"src.core.{cog}")
    except ImportError as error:
        module_logger.error(traceback.print_tb(error))
        exit(1)
    KonekoBot.load_extension("jishaku")

    # Dry run option for travis.
    if KonekoBot.dry_run is True:
        module_logger.debug("Quitting: dry run")
        exit(0)

    module_logger.debug("Logging into Discord...")
    KonekoBot.run()

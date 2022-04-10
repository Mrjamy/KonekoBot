#!/usr/bin/env python3

# Builtins
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
from src.core.logger import Logger

if sys.version_info < (3, 6):
    raise ImportError("Python 3.6 or greater is required")

# Setup module logging.
Logger()
module_logger = logging.getLogger('koneko')


async def _prefix(bot, msg) -> List[str]:
    user_id = bot.user.id
    return [f'<@!{user_id}> ', f'<@{user_id}> ', '$']


class Koneko(commands.AutoShardedBot):
    """Auto sharded discord bot."""

    __slots__ = 'uptime', 'command_count', 'settings', 'logger', 'loop'

    # Create an AutoSharded bot.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uptime = time.time()
        self.command_count = 0
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
            self.loop.run_until_complete(self.start(self.config.get('Koneko',
                                                                    'token')))
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.logout())


if __name__ == '__main__':
    intends = discord.Intents.default()
    intends.members = True

    KonekoBot = Koneko(command_prefix=_prefix, owner_id=180640710217826304,
                       help_command=None, intends=intends,
                       chunk_guilds_at_startup=False, heartbeat_timeout=150.0)

    try:
        for cog in KonekoBot.settings.toggle_extensions:
            KonekoBot.load_extension(f"src.cogs.{cog}")
        for cog in KonekoBot.settings.core_extensions:
            KonekoBot.load_extension(f"src.core.{cog}")
    except ImportError as error:
        module_logger.error(traceback.print_tb(error))
        exit(1)

    # Dry run option for travis.
    if sys.argv[1] if len(sys.argv) > 1 else 0:
        module_logger.debug("Quitting: dry run")
        exit(0)

    module_logger.debug("Logging into Discord...")
    KonekoBot.run()

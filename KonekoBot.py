#!/usr/bin/env python3

# Builtins
import logging
import sys
import time
from typing import List, Union

# Pip
import discord
import yaml
from discord.ext import commands

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

# Locals
from src.core.config import Settings
from src.core.logger import Logger

if sys.version_info < (3, 6):
    raise ImportError("Python 3.6 or greater is required")

# Setup module logging.
Logger()
module_logger = logging.getLogger('koneko')


async def _prefix(bot, _msg: discord.Message) -> List[str]:
    prefix: Union[str, None] = bot.config.get('prefix')
    if not prefix:
        prefix: str = '$'

    user_id: int = bot.user.id
    return [f'<@!{user_id}> ', f'<@{user_id}> ', prefix]


class Koneko(commands.AutoShardedBot):
    """Auto sharded discord bot."""

    __slots__ = 'uptime', 'command_count', 'settings', 'logger', 'loop',

    # Create an AutoSharded bot.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uptime: float = time.time()
        self.command_count: int = 0
        self.settings: Settings = Settings()

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
        await super().close()
        exit(0)

    @property
    def config(self) -> dict:
        try:
            with open('config.yaml', 'rb+') as file:
               config: dict = yaml.load(file, Loader)
        except FileNotFoundError:
            print('config.yaml not found.')
            exit(1)

        if config is None:
            print('config.yaml could not be opened and parsed')
            exit(1)

        return config.get('koneko')

    def run(self) -> None:
        try:
            self.loop.run_until_complete(self.start(self.config.get('token')))
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.logout())


if __name__ == '__main__':
    intends = discord.Intents.default()
    intends.members = True

    KonekoBot: Koneko = Koneko(command_prefix=_prefix, owner_id=180640710217826304,
                       intends=intends, chunk_guilds_at_startup=False,
                       heartbeat_timeout=150.0)

    try:
        for cog in KonekoBot.settings.toggle_extensions:
            KonekoBot.load_extension(f"src.cogs.{cog}")
        for cog in KonekoBot.settings.core_extensions:
            KonekoBot.load_extension(f"src.core.{cog}")
    except (ImportError, commands.ExtensionNotFound) as error:
        module_logger.error(error)
        exit(1)

    # Dry run option for travis.
    if sys.argv[1] if len(sys.argv) > 1 else 0:
        module_logger.debug("Quitting: dry run")
        exit(0)

    module_logger.debug("Logging into Discord...")
    KonekoBot.run()

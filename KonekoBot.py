#!/usr/bin/env python3

# Builtins
import asyncio
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

if sys.version_info < (3, 8):
    raise ImportError("Python 3.8 or greater is required")

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
        self.blacklist = self.config.get('blacklist')

        try:
            for cog in self.settings.toggle_extensions:
                asyncio.run(self.load_extension(f"src.cogs.{cog}"))
            for cog in self.settings.core_extensions:
                asyncio.run(self.load_extension(f"src.core.{cog}"))
        except (ImportError, commands.ExtensionNotFound) as error:
            module_logger.error(error)
            exit(1)

    async def on_message(self, message: discord.Message) -> None:
        ctx = await self.get_context(message, cls=commands.Context)

        if message.author.bot:
            return

        if self.user in message.mentions:
            try:
                await message.add_reaction("\N{EYES}")
            except discord.HTTPException:
                pass

        if ctx.command is None:
            return

        if self.blacklist:
            if ctx.author.id in self.blacklist:
                return

            if  ctx.guild is not None and ctx.guild.id in self.blacklist:
                return

        await self.invoke(ctx)

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
            super().run(self.config.get('token'), reconnect=True)
        except KeyboardInterrupt:
            exit(0)

    async def close(self) -> None:
        await super().close()

def main():
    intents: discord.Intents = discord.Intents.default()
    intents.__setattr__('members', True)

    kwargs = {
        'command_prefix': _prefix,
        'owner_id': 180640710217826304,
        'intents': intents,
        'chunk_guilds_at_startup': False,
        'heartbeat_timeout':150.0
    }

    koneko = Koneko(**kwargs)
    koneko.run()

if __name__ == '__main__':
    main()

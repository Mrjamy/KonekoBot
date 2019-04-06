#!/usr/bin/env python3

# Builtins
import time
import traceback
import asyncio

# Pip
import configparser
import discord
from discord.ext import commands

# Locals
from src.core.config import Settings
from src.helpers.database.db import run


loop = asyncio.get_event_loop()
settings = Settings()
config = configparser.ConfigParser()
config.read('config.ini')
# TODO : v1.1 Add a logger to the bot.


class Bot(commands.AutoShardedBot):
    # Create an AutoSharded bot.
    def __init__(self):
        super().__init__(
            # TODO : v1.1 allow different prefix on guilds.
            command_prefix=commands.when_mentioned_or(settings.prefix),
            owner_id=settings.owner_id,
        )
        self.uptime = time.time()
        self.command_count = 0
        self.dry_run = settings.dry_run
        self.settings = settings
        self.db = loop.run_until_complete(run())

    # TODO : v1.1 create a run function to call in __main__
    

if __name__ == '__main__':
    KonekoBot = Bot()

    try:
        for cog in KonekoBot.settings.toggle_extensions:
            KonekoBot.load_extension(f"src.cogs.{cog}")
        for cog in KonekoBot.settings.core_extensions:
            KonekoBot.load_extension(f"src.core.{cog}")
    except ImportError as error:
        traceback.print_exc()
        exit(1)

    # Dry run option for travis.
    if KonekoBot.dry_run is True:
        print("Quitting: dry run")
        exit(0)

    print("Logging into Discord...")
    KonekoBot.run(config.get('Koneko', 'token'))
    try:
        loop.run_until_complete(KonekoBot)
    except discord.LoginFailure:
        print("Could not login.")
    except Exception as e:
        loop.run_until_complete(KonekoBot.close())
    finally:
        loop.close()
        exit(1)

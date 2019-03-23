#!/usr/bin/env python3

import asyncio
import time
import discord
import configparser
from discord.ext import commands
from src.core.config import Settings
from src.core.setup import Setup

settings = Settings()
loop = asyncio.get_event_loop()
settings = Settings()
config = configparser.ConfigParser()
config.read('config.ini')

# Create an AutoSharded bot.
KonekoBot = commands.AutoShardedBot(
    # Customizable when running the bot using the "-c" or "--command-prefix" option.
    command_prefix=commands.when_mentioned_or(settings.prefix),
    # Customizable when running the bot using the "-p" or "--pm-help" option.
    pm_help=settings.pm_help,
    owner_id=settings.owner_id,
)

KonekoBot.uptime = time.time()
KonekoBot.command_count = 0
KonekoBot.dry_run = settings.dry_run
KonekoBot.settings = settings


# Function called when the bot is ready.
@KonekoBot.event
async def on_ready():
    """KonekoBot on_ready event."""
    game = settings.prefix + "help for help"
    activity = discord.Game(name=game)
    await KonekoBot.change_presence(status=discord.Status.online, activity=activity)
    # Bot logged in.
    print(f'Logged in as {KonekoBot.user}')
    print(f'I am in {len(KonekoBot.guilds)} guilds.')


@KonekoBot.event
async def on_command(ctx):
    KonekoBot.command_count += 1


if __name__ == '__main__':
    Setup().setup()

    for extension in settings.toggle_extensions:
        KonekoBot.load_extension("src.cogs." + extension)
    for extension in settings.core_extensions:
        KonekoBot.load_extension(extension)

    # Dry run option for travis.
    if KonekoBot.dry_run is True:
        print("Quitting: dry run")
        exit(0)

    KonekoBot.uptime = time.time()
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

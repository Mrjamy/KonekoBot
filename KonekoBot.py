#!/usr/bin/env python3

import asyncio
import logging
import time
import re
import discord
from discord.ext import commands
from src.core.config import Settings

logger = logging.getLogger('discord')
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

toggle_extensions = [
    "gambling.gambling",
    # "games.pokemon",
    "games.dnd",
    "games.rps",
    "general.general",
    # "general.goodbye",
    # "general.response",
    # "general.welcome",
    # "help.help",
    # "moderation.moderation",
    "music.music",
    # "nsfw.nsfw",
    "utility.utility",
    # "utility.stats",
]

core_extensions = [
    "src.core.ErrorHandler",
]


class KonekoBot(commands.Bot):
    __slots__ = ('uptime', '_shutdown_mode', 'settings')

    def __init__(self, *args, **kwargs):
        self.uptime = time.time()
        self._shutdown_mode = None
        self.settings = Settings()
        self._dry_run = None

        super().__init__(*args,
                         command_prefix=commands.when_mentioned_or(self.settings.prefix),
                         owner_id=self.settings.owner_id,
                         pm_help=self.settings.pm_help,
                         **kwargs)

    async def shutdown(self, *, restart=False):
        """Gracefully quits Red with exit code 0
        If restart is True, the exit code will be 26 instead
        The launcher automatically restarts Red when that happens"""
        self._shutdown_mode = not restart
        await self.close()


def initialize(bot_class=KonekoBot):
    bot = bot_class()
    
    # Function called when the bot is ready.
    @bot.event
    async def on_ready():
        game = bot.settings.prefix + "help for help"
        activity = discord.Game(name=game)
        await bot.change_presence(status=discord.Status.online, activity=activity)
        # Bot logged in.
        print(f'Logged in as {bot.user}')
        print(f'I am in {len(bot.guilds)} guilds.')

    return bot


def main(bot):
    for extension in toggle_extensions:
        bot.load_extension("src.modules." + extension)
    for extension in core_extensions:
        bot.load_extension(extension)

    if bot._dry_run:
        print("Quitting: dry run")
        bot._shutdown_mode = True
        exit(0)

    bot.uptime = time.time()
    print("Logging into Discord...")
    bot.run(bot.settings.token)


if __name__ == '__main__':
    bot = initialize()

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(bot))
    except discord.LoginFailure:
        print("Could not login.")
    except Exception as e:
        loop.run_until_complete(bot.close())
    finally:
        loop.close()
        if bot._shutdown_mode:
            exit(0)
        elif not bot._shutdown_mode:
            exit(26)  # Restart
        else:
            exit(1)

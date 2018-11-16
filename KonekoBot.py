#!/usr/bin/env python3

import discord
import logging
from discord.ext import commands
from src.core.config import Settings
import datetime
import asyncio
import sys
import traceback

logger = logging.getLogger('discord')
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

toggle_extensions = [
    "gambling.gambling",
    # "games.pokemon",
    "games.rps",
    "general.general",
    # "general.goodbye",
    # "general.response",
    # "general.welcome",
    # "help.commands",
    # "help.help",
    "music.music",
    # "nsfw.nsfw",
    # "utility.utility",
    # "utility.stats",
]

core_extensions = [
    # "src.modules.utility.CommandToggle",
]


class KonekoBot(commands.Bot):
    __slots__ = ('uptime', '_shutdown_mode', 'settings')

    def __init__(self, *args, **kwargs):
        self.uptime = datetime.datetime.utcnow()
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
        print('Logged in as {0.user}'.format(bot))

    @bot.event
    async def on_command_error(ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.CommandNotFound, commands.UserInputError)

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{bot.settings.prefix}{ctx.command} has been disabled.')
            return

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.channel.send(f'{bot.settings.prefix}{ctx.command} can not be used in Private Messages.')
            except:
                pass
            return

        elif isinstance(error, commands.BadArgument):
            await ctx.send(f'Refer to.{bot.settings.prefix}help {ctx.command}')
            return

        elif isinstance(error, commands.BotMissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            await ctx.send(f'I need the **{fmt}** permission(s) to run this command.')
            return

        if isinstance(error, commands.MissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            await ctx.send(f'You need the **{fmt}** permission(s) to use this command.')
            return

        # All other Errors not returned come here... And we can just print the default TraceBack.
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

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

    bot.uptime = datetime.datetime.utcnow()
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
        if bot._shutdown_mode is True:
            exit(0)
        elif bot._shutdown_mode is False:
            exit(26)  # Restart
        else:
            exit(1)

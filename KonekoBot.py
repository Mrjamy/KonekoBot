#!/usr/bin/env python3

import asyncio
import time
import discord
from discord.ext import commands
from src.core.config import Settings
from src.core.setup import Setup

settings = Settings()
loop = asyncio.get_event_loop()

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
KonekoBot.remove_command('help')


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


@KonekoBot.command(name='help', aliases=['h'], pass_context=True, hidden=True)
async def help_command(ctx, command: str = None):
    """Shows this message."""

    # If no commands are supplied help will return a brief summary of all commands.
    if command is None:
        pages = await KonekoBot.formatter.format_help_for(ctx, KonekoBot)
    # If one command is supplied attempt to show it description.
    else:
        # try to see if it is a cog name
        name = KonekoBot.get_command(command)
        if name is None:
            embed = discord.Embed(description=KonekoBot.command_not_found.format(command),
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed)
            return

        pages = await KonekoBot.formatter.format_help_for(ctx, name)

    for page in pages:
        embed = discord.Embed(description=page.strip("```").replace('<', '[').replace('>', ']'),
                              color=discord.Color.dark_purple())
        await ctx.channel.send(embed=embed)


@KonekoBot.event
async def on_command(ctx):
    KonekoBot.command_count += 1


if __name__ == '__main__':
    Setup().setup()

    for extension in settings.toggle_extensions:
        KonekoBot.load_extension("src.modules." + extension)
    for extension in settings.core_extensions:
        KonekoBot.load_extension(extension)

    # Dry run option for travis.
    if KonekoBot.dry_run is True:
        print("Quitting: dry run")
        close = loop.create_task(KonekoBot.close())
        loop.run_until_complete(close)
        loop.close()
        exit(0)

    KonekoBot.uptime = time.time()
    print("Logging into Discord...")
    KonekoBot.run(settings.token)

    try:
        loop.run_until_complete(KonekoBot)
    except discord.LoginFailure:
        print("Could not login.")
    except Exception as e:
        loop.run_until_complete(KonekoBot.close())
    finally:
        loop.close()
        exit(1)

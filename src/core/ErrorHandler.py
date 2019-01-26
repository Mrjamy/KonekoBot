import sys
import traceback
import discord
from discord.ext import commands
from src.core.exceptions import (
    DjOnly,
    NotInVoiceChannel
)
from datetime import datetime, timedelta
from src.modules.economy.currency import NotEnoughBalance


class ErrorHandler:
    __slots__ = 'bot'

    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
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
            embed = discord.Embed(title=f'`{ctx.prefix}{ctx.command}` has been disabled.',
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed)
            return

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                embed = discord.Embed(title=f'`{ctx.prefix}{ctx.command}` can not be used in Private Messages.',
                                      color=discord.Color.red())
                await ctx.channel.send(embed=embed)
            except (discord.Forbidden, discord.HTTPException):
                pass
            return

        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(title=f'Refer to `{ctx.prefix}help {ctx.command}`',
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed)
            return

        elif isinstance(error, commands.BotMissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            embed = discord.Embed(title=f'I need the **{fmt}** permission(s) to run this command.',
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed)
            return

        if isinstance(error, commands.MissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            embed = discord.Embed(title=f'You need the **{fmt}** permission(s) to use this command.',
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed)
            return

        if isinstance(error, DjOnly):
            embed = discord.Embed(title=f'This command requires you to have a role called DJ.',
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed)
            return

        if isinstance(error, NotInVoiceChannel):
            embed = discord.Embed(title=f'This command requires you to be in a voice channel.',
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed)
            return

        if isinstance(error, NotEnoughBalance):
            embed = discord.Embed(title=f'You can\'t. afford this right now.',
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed)
            return

        if isinstance(error, commands.CommandOnCooldown):
            seconds = round(error.retry_after)

            sec = timedelta(seconds=seconds)
            d = datetime(1, 1, 1) + sec

            cooldown = f"{d.hour}h {d.minute}m {d.second}s"
            embed = discord.Embed(title=f'You can\'t do this right now try again in {cooldown}.',
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed)
            return

        # All other Errors not returned come here... And we can just print the default TraceBack.
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    # TODO: properly intercept system errors
    async def on_error(self, ctx, event, *args, **kwargs):
        # TODO: catch discord.HTTPException
        # TODO: catch discord.Forbidden
        # TODO: catch discord.LoginFailure
        # TODO: catch discord.NotFound
        # TODO: catch generic errors
        return


def setup(bot):
    bot.add_cog(ErrorHandler(bot))

import sys
import traceback
import discord
from discord.ext import commands


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
            await ctx.send(f'`{ctx.prefix}{ctx.command}` has been disabled.')
            return

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.channel.send(f'`{ctx.prefix}{ctx.command}` can not be used in Private Messages.')
            except (discord.Forbidden, discord.HTTPException):
                pass
            return

        elif isinstance(error, commands.BadArgument):
            await ctx.send(f'Refer to `{ctx.prefix}help {ctx.command}`')
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

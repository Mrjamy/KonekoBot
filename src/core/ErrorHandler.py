# Builtins
import logging
from datetime import datetime, timedelta

# Pip
from discord.ext import commands

# locals
from src.core.exceptions import NotEnoughBalance
from src.utils.general import DiscordEmbed

module_logger = logging.getLogger('koneko.ErrorHandler')


class ErrorHandler(commands.Cog):
    """Class for error handling."""

    __slots__ = ('bot',)

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error) -> None:
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        # This prevents any commands with local handlers being handled here in
        # on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.CommandNotFound, commands.UserInputError,
                   commands.CheckFailure)

        # Allows us to check for original exceptions raised and sent to
        # CommandInvokeError. If nothing is found. We keep the exception passed
        # to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.DisabledCommand):
            await DiscordEmbed.error(ctx, title=f'`{ctx.prefix}{ctx.command}` has been disabled.')
            return

        elif isinstance(error, commands.NoPrivateMessage):
            await DiscordEmbed.error(ctx, title=f'`{ctx.prefix}{ctx.command}` can not be used in Private Messages.')
            return

        elif isinstance(error, commands.BadArgument):
            await DiscordEmbed.error(ctx, title=f'Refer to `{ctx.prefix}help {ctx.command}`')
            return

        elif isinstance(error, commands.BotMissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            await DiscordEmbed.error(ctx, title=f'I need the **{fmt}** permission(s) to run this command.')
            return

        if isinstance(error, commands.MissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            await DiscordEmbed.error(ctx, title=f'You need the **{fmt}** permission(s) to use this command.')
            return

        if isinstance(error, NotEnoughBalance):
            await DiscordEmbed.error(ctx, title=f'You can\'t. afford this right now.')
            return

        if isinstance(error, commands.CommandOnCooldown):
            seconds = round(error.retry_after)

            sec = timedelta(seconds=seconds)
            d = datetime(1, 1, 1) + sec

            cooldown = f"{d.hour}h {d.minute}m {d.second}s"
            await DiscordEmbed.error(ctx, title=f'You can\'t do this right now try again in {cooldown}.')
            return

        # All other Errors not returned come here... And we can just print the
        # default TraceBack.
        module_logger.error(f'Ignoring exception in command {ctx.command}:')
        module_logger.error(error)


def setup(bot) -> None:
    """The setup function to add this cog to Koneko."""
    bot.add_cog(ErrorHandler(bot))

"""
Module containing event-listener for all discord.py errors.
"""

import logging
from datetime import datetime, timedelta
# Pip
from discord.ext import commands

# locals
from typing import List

from src.core.exceptions import NotEnoughBalance
from src.utils.general import DiscordEmbed

module_logger = logging.getLogger('koneko.ErrorHandler')


class ErrorHandler(commands.Cog):
    """Class for error handling."""

    __slots__ = 'bot',

    def __init__(self, bot):
        self.bot = bot

    # pylint: disable=too-many-return-statements, too-many-branches
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        # This prevents any commands with local handlers being handled here in
        # on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.CommandNotFound, commands.CheckFailure)

        # Allows us to check for original exceptions raised and sent to
        # CommandInvokeError. If nothing is found. We keep the exception passed
        # to on_command_error.
        error: commands.CommandError = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        command: str = ctx.invoked_with or ctx.command
        prefix: str = ctx.prefix

        if isinstance(error, commands.DisabledCommand):
            await DiscordEmbed.error(ctx, title=f'`{prefix}{command}` has been disabled.')
            return

        if isinstance(error, commands.NoPrivateMessage):
            await DiscordEmbed.error(ctx, title=f'`{prefix}{command}` can not be used in Private Messages.')
            return

        # TODO send expected input instead
        if isinstance(error, (commands.BadArgument, commands.UserInputError)):
            await DiscordEmbed.error(ctx, title=f'Incorrect command usage, Refer to `{prefix}help {command}`')
            return

        if isinstance(error, commands.BotMissingPermissions):
            missing: List[str] = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_permissions]
            if len(missing) > 2:
                fmt: str = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt: str = ' and '.join(missing)
            await DiscordEmbed.error(ctx, title=f'I need the **{fmt}** permission(s) to run this command.')
            return

        if isinstance(error, commands.MissingPermissions):
            missing: List[str] = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_permissions]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            await DiscordEmbed.error(ctx, title=f'You need the **{fmt}** permission(s) to use this command.')
            return

        if isinstance(error, NotEnoughBalance):
            await DiscordEmbed.error(ctx, title='You can\'t. afford this right now.')
            return

        if isinstance(error, commands.CommandOnCooldown):
            seconds: int = round(error.retry_after)

            sec: timedelta = timedelta(seconds=seconds)
            d: datetime = datetime(1, 1, 1) + sec

            cooldown: str = f"{d.hour}h {d.minute}m {d.second}s"
            await DiscordEmbed.error(ctx, title=f'You can\'t do this right now try again in {cooldown}.')
            return

        # All other Errors not returned come here... And we can just print the
        # default TraceBack.
        module_logger.error('Ignoring %s in command %s:', type(error) or "exception", command)
        module_logger.error("error: %s", error)


async def setup(bot) -> None:
    """The setup function to add this cog to Koneko."""
    await bot.add_cog(ErrorHandler(bot))

# TODO: add option to customize prefix pre guild.

import src.core.checks as check
from discord.ext import commands
from KonekoBot import KonekoBot


class Utility:
    """Utility commands."""

    __slots__ = 'bot'

    def __init__(self, bot):
        self.bot = bot

    @check.is_owner()
    @commands.command(pass_context=True, alliases=["sp"])
    async def set_prefix(self, ctx, prefix: str):
        """Set the bots prefix."""
        KonekoBot.command_prefix = commands.when_mentioned_or(prefix)

        await ctx.channel.send(f"My prefix has been updated to {prefix}")


def setup(bot):
    bot.add_cog(Utility(bot))

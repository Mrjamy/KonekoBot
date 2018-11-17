import time
import src.core.checks as check

from datetime import datetime, timedelta
from discord.ext import commands


class Utility:
    """Utility commands."""

    __slots__ = 'bot'

    def __init__(self, bot):
        self.bot = bot

    @check.is_owner()
    @commands.command(pass_context=True, hidden=True)
    async def shutdown(self, ctx):
        """Shuts the bot down."""

        await ctx.channel.send(f"Don't kill me!")

    @commands.command(pass_context=True)
    async def uptime(self, ctx):
        """Get the bots uptime."""

        seconds = round(time.time() - self.bot.uptime)

        sec = timedelta(seconds=seconds)
        d = datetime(1, 1, 1) + sec

        await ctx.channel.send(f"I have been running for {d.day-1:d}d {d.hour}h {d.minute}m {d.second}s")


def setup(bot):
    bot.add_cog(Utility(bot))

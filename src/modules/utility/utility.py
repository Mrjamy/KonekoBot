import time
import discord
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
    async def stats(self, ctx):
        """Returns current statistics of the bot."""

        seconds = round(time.time() - self.bot.uptime)

        sec = timedelta(seconds=seconds)
        d = datetime(1, 1, 1) + sec

        uptime = f"{d.day-1:d}d {d.hour}h {d.minute}m {d.second}s"
        guilds = str(len(self.bot.guilds))

        embed = discord.Embed(title="Koneko's Statistics", description="", color=0x00ff00)
        embed.add_field(name="Uptime", value=uptime, inline=True)
        embed.add_field(name="Guilds", value=guilds, inline=True)

        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Utility(bot))

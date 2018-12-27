import time
from datetime import datetime, timedelta
import discord
from discord.ext import commands
from src.core.checks import Checks


class Utility:
    """Utility commands."""

    __slots__ = 'bot'

    def __init__(self, bot):
        self.bot = bot

    @Checks.is_owner()
    @commands.command(pass_context=True, hidden=True)
    async def shutdown(self, ctx):
        """Shuts the bot down."""

        await ctx.channel.send(f"Don't kill me!")

    @commands.bot_has_permissions(embed_links=True)
    @commands.command(pass_context=True)
    async def stats(self, ctx):
        """Returns current statistics of the bot."""

        seconds = round(time.time() - self.bot.uptime)

        sec = timedelta(seconds=seconds)
        d = datetime(1, 1, 1) + sec

        uptime = f"{d.day-1:d}d {d.hour}h {d.minute}m {d.second}s"
        guilds = str(len(self.bot.guilds))
        command_count = self.bot.command_count + 1

        embed = discord.Embed(title="Koneko's Statistics", description="", color=discord.Color.dark_purple())
        embed.add_field(name="Uptime", value=uptime, inline=True)
        embed.add_field(name="Guilds", value=guilds, inline=True)
        embed.add_field(name="Commands executed", value=command_count, inline=True)

        await ctx.channel.send(embed=embed)

    # TODO: add command /remind <message>


def setup(bot):
    bot.add_cog(Utility(bot))

# Builtins
from time import time
from datetime import datetime, timedelta

# Pip
import discord
from discord.ext import commands

# Locals
from src.core.checks import Checks
from src.utils.database.repositories.prefix_repository import PrefixRepository


class Utility(commands.Cog):
    """Utility commands."""

    __slots__ = 'bot'

    def __init__(self, bot):
        self.bot = bot
        self.prefix_repository = PrefixRepository()

    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
    async def stats(self, ctx):
        """Returns current statistics of the bot."""

        seconds = round(time() - self.bot.uptime)

        sec = timedelta(seconds=seconds)
        d = datetime(1, 1, 1) + sec

        uptime = f"{d.day-1:d}d {d.hour}h {d.minute}m {d.second}s"
        guilds = str(len(self.bot.guilds))
        members = str(len(list(self.bot.get_all_members())))
        command_count = self.bot.command_count + 1

        embed = discord.Embed(title="Koneko's Statistics", description="", color=discord.Color.dark_purple())
        embed.add_field(name="Guilds", value=guilds, inline=True)
        embed.add_field(name="Users", value=members, inline=True)
        embed.add_field(name="Uptime", value=uptime, inline=True)
        embed.add_field(name="Commands executed", value=command_count, inline=True)

        await ctx.channel.send(embed=embed)

    @commands.guild_only()
    @commands.group()
    async def prefix(self, ctx):
        if ctx.invoked_subcommand is None:
            prefix = await self.prefix_repository.get(ctx.guild)
            return await ctx.channel.send(f"Prefix for this guild is {prefix}")

    @commands.has_permissions(administrator=True)
    @prefix.command()
    async def set(self, ctx, prefix: str = None):
        if not prefix:
            return await ctx.channel.send(f"Please specify a prefix")
        prefix = await self.prefix_repository.insert(ctx.guild, prefix)
        return await ctx.channel.send(f"Prefix for this guild is now {prefix}")

    @commands.has_permissions(administrator=True)
    @prefix.command()
    async def delete(self, ctx):
        res = await self.prefix_repository.delete(ctx.guild)
        if res:
            return await ctx.channel.send(f"Successfully deleted custom prefix `{ctx.prefix}` will now be the default prefix for this guild")
        else:
            return await ctx.channel.send("No custom prefix found")

    # TODO: add command /remind <message>


def setup(bot):
    bot.add_cog(Utility(bot))

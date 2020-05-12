"""
Module containing utility commands.
"""

# Builtins
import logging
from datetime import datetime, timedelta
from time import time

# Pip
import discord
from discord.ext import commands

# Locals
from src.utils.database.repositories.prefix_repository import PrefixRepository
from src.utils.general import DiscordEmbed

module_logger = logging.getLogger('koneko.Games')


class Utility(commands.Cog):
    """Utility commands."""

    __slots__ = 'bot', 'prefix_repository'

    def __init__(self, bot):
        self.bot = bot
        self.prefix_repository = PrefixRepository()

    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
    async def stats(self, ctx) -> None:
        """Returns current statistics of the bot."""

        seconds = round(time() - self.bot.uptime)

        sec = timedelta(seconds=seconds)
        d = datetime(1, 1, 1) + sec

        parts = []

        for stat, value in {
            'uptime': f"{d.day - 1:d}d {d.hour}h {d.minute}m {d.second}s",
            'guilds': str(len(self.bot.guilds)),
            'members': str(len(list(self.bot.get_all_members()))),
            'command_count': self.bot.command_count + 1
        }:
            parts.append({
                {
                    'name': stat,
                    'value': value,
                    'inline': True
                }
            })

        await DiscordEmbed.message(ctx, parts, title="Koneko's Statistics")

    @commands.guild_only()
    @commands.group()
    async def prefix(self, ctx) -> None:
        """Get Koneko's prefix."""
        if ctx.invoked_subcommand is None:
            prefix = await self.prefix_repository.get(ctx.guild)
            await ctx.channel.send(f"Prefix for this guild is {prefix}")
            return

    @commands.has_permissions(administrator=True)
    @prefix.command()
    async def set(self, ctx, prefix: str = None) -> None:
        """Set a custom prefix for Koneko."""
        if not prefix:
            await ctx.channel.send("Please specify a prefix")
            return
        prefix = await self.prefix_repository.insert(ctx.guild, prefix)
        await ctx.channel.send(f"Prefix for this guild is now {prefix}")
        return

    @commands.has_permissions(administrator=True)
    @prefix.command()
    async def delete(self, ctx) -> None:
        """Delete koneko's custom prefix."""
        res = await self.prefix_repository.delete(ctx.guild)
        if res:
            await ctx.channel.send(f"Successfully deleted custom prefix `{ctx.prefix}` will now be the default prefix for this guild")
        else:
            await ctx.channel.send("No custom prefix found")

    # TODO: add command /remind <message>


def setup(bot) -> None:
    """The setup function to add this cog to Koneko."""
    bot.add_cog(Utility(bot))

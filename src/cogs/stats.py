"""
Module containing stats commands.
"""

# Builtins
import logging
from datetime import datetime, timedelta
from time import time

# Pip
import discord
from discord.ext import commands

# Locals
from src.utils.general import DiscordEmbed, NameTransformer

module_logger = logging.getLogger('koneko.Games')


class Stats(commands.Cog):
    """Stats commands."""

    __slots__ = 'bot',

    def __init__(self, bot):
        self.bot = bot

    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
    async def stats(self, ctx: commands.Context) -> discord.Embed:
        """Returns current statistics of the bot."""

        seconds: int = round(time() - self.bot.uptime)

        sec: timedelta = timedelta(seconds=seconds)
        d: datetime = datetime(1, 1, 1) + sec

        parts: list = []
        data: dict = {
            'Uptime': f"{d.day - 1:d}d {d.hour}h {d.minute}m {d.second}s",
            'Guilds': str(len(self.bot.guilds)),
            'Commands used': self.bot.command_count + 1
        }

        for stat, value in data.items():
            parts.append({
                'name': stat,
                'value': value
            })

        return await DiscordEmbed.message(ctx, parts, title="Koneko's Statistics")

    @commands.guild_only()
    @commands.command(aliases=["followage"])
    async def joined(self, ctx: commands.Context, users: commands.Greedy[discord.Member]):
        """Says when a member joined."""
        if len(users) == 0:
            users: list = [ctx.message.author]
        message: str = ''.join([f'{NameTransformer(user)} joined in {user.joined_at}\n' for user in users])

        await ctx.channel.send(message)

async def setup(bot) -> None:
    """The setup function to add this cog to Koneko."""
    await bot.add_cog(Stats(bot))

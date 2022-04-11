"""
Module containing rpg commands.
"""

# Builtins
import logging

# Pip
import discord
from discord.ext import commands

# Locals
from src.utils.general import DiscordEmbed, NameTransformer

module_logger = logging.getLogger('koneko.General')


class Rpg(commands.Cog):
    """Rpg commands."""

    __slots__ = 'bot',

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def give_item(self, ctx: commands.Context, users: commands.Greedy[discord.Member], *, item) -> discord.Embed:
        """Give one or more users an item."""
        if len(users) == 0:
            users: list = [self.bot.user]
        mentions: str = ' '.join([f'{NameTransformer(user)}' for user in users])
        message: str = f"{ctx.message.author} gives {mentions} {item}"

        return await DiscordEmbed.message(ctx, title=message)


async def setup(bot) -> None:
    """The setup function to add this cog to Koneko."""
    await bot.add_cog(Rpg(bot))

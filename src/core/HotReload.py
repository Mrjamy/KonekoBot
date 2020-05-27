"""
Module to reload cogs on the go.
"""

# Builtins
import logging

# Pip
from discord.ext import commands

module_logger = logging.getLogger('koneko.HotReloading')


class HotReload(commands.Cog):
    """Class for reloading ."""

    __slots__ = ('bot',)

    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx) -> bool:
        """Cog check

        Only returns true for bot owner."""
        return self.bot.is_owner(ctx.author)

    @commands.command(aliases=["load"], hidden=True)
    async def reload(self, ctx, cog: str) -> None:
        """Reloads specified cog."""
        await ctx.channel.send(F"loaded {cog}")

    @commands.command(hidden=True)
    async def unload(self, ctx, cog: str) -> None:
        """Unloads specified cog."""
        await ctx.channel.send(F"unloaded {cog}")


def setup(bot) -> None:
    """The setup function to add this cog to Koneko."""
    bot.add_cog(HotReload(bot))

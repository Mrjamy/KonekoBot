"""
Module to reload cogs on the go.
"""

# Builtins
import logging
from typing import Union

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
        cog = self.__cog_namespace(cog)
        if not cog:
            return await ctx.channel.send(F"Could not find cog: {cog}")

        self.bot.reload_extension(cog)

        await ctx.channel.send(F"loaded {cog}")

    @commands.command(hidden=True)
    async def unload(self, ctx, cog: str) -> None:
        """Unloads specified cog."""
        cog = self.__cog_namespace(cog)
        if not cog:
            return await ctx.channel.send(F"Could not find cog: {cog}")

        self.bot.unload_extension(cog)

        await ctx.channel.send(F"unloaded {cog}")

    def __cog_namespace(self, cog: str)-> Union[str, bool]:
        if cog in self.bot.settings.toggle_extensions:
            return f"src.cogs.{cog}"
        elif cog in self.bot.settings.core_extensions:
            return f"src.core.{cog}"
        else:
            return False


def setup(bot) -> None:
    """The setup function to add this cog to Koneko."""
    bot.add_cog(HotReload(bot))

"""
Module to reload cogs on the go.
"""

# Builtins
import logging
from typing import Union

# Pip
import discord
from discord.ext import commands

module_logger = logging.getLogger('koneko.HotReloading')


class HotReload(commands.Cog):
    """Class for reloading ."""

    __slots__ = 'bot',

    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx: commands.Context) -> bool:
        """Cog check

        Only returns true for bot owner."""
        return self.bot.is_owner(ctx.author)

    @commands.command(aliases=["load"], hidden=True)
    async def reload(self, ctx: commands.Context, cog: str) -> discord.Message:
        """Reloads specified cog."""
        _cog: str = self.__cog_namespace(cog)
        if not _cog:
            return await ctx.channel.send(F"Could not find cog: {cog}")

        extension = _cog or cog
        try:
            await self.bot.load_extension(extension)
            return await ctx.channel.send(F"Loaded {extension}")
        except commands.ExtensionAlreadyLoaded:
            await self.bot.reload_extension(extension)
            return await ctx.channel.send(F"Reloaded {extension}")
        except commands.NoEntryPointError:
            return await ctx.channel.send(F"{extension} does not contain a setup function")
        except commands.ExtensionFailed:
            return await ctx.channel.send(F"{extension} could not be loaded")

    @commands.command(hidden=True)
    async def unload(self, ctx: commands.Context, cog: str) -> None:
        """Unloads specified cog."""
        cog: str = self.__cog_namespace(cog)
        if not cog:
            await ctx.channel.send(F"Could not find cog: {cog}")
            return

        await self.bot.unload_extension(cog)

        await ctx.channel.send(F"unloaded {cog}")

    def __cog_namespace(self, cog: str)-> Union[str, bool]:
        if cog in self.bot.settings.toggle_extensions:
            return f"src.cogs.{cog}"
        elif cog in self.bot.settings.core_extensions:
            return f"src.core.{cog}"
        else:
            return False


async def setup(bot) -> None:
    """The setup function to add this cog to Koneko."""
    await bot.add_cog(HotReload(bot))

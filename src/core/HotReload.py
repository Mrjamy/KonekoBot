# Builtins
import logging

# Pip
from asyncio import coroutine
from discord.ext import commands

module_logger = logging.getLogger('koneko.HotReloading')


class HotReload(commands.Cog):
    """Class for reloading ."""

    __slots__ = 'bot'

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx) -> bool:
        return await self.bot.is_owner(ctx.author)

    @commands.command(aliases=["load"], hidden=True)
    async def reload(self, ctx, cog: str) -> coroutine:
        return await ctx.channel.send(F"loaded {cog}")

    @commands.command(hidden=True)
    async def unload(self, ctx, cog: str) -> coroutine:
        return await ctx.channel.send(F"unloaded {cog}")


def setup(bot) -> None:
    bot.add_cog(HotReload(bot))

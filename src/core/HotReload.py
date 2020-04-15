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
        self.location = "src.cogs."

    async def cog_check(self, ctx) -> bool:
        return await self.bot.is_owner(ctx.author)

    @commands.command(aliases=["load"], hidden=True)
    async def reload(self, ctx, *cogs: str) -> coroutine:
        for cog in cogs:
            self.bot.reload_extension(cog)

        reloaded = " ".join(f"{self.location}{cogs}")
        return await ctx.channel.send(F"loaded {reloaded}")

    @commands.command(hidden=True)
    async def unload(self, ctx, *cogs: str) -> coroutine:
        for cog in cogs:
            self.bot.unload_extension(cog)

        unloaded = " ".join(f"{self.location}{cogs}")
        return await ctx.channel.send(F"unloaded {unloaded}")


def setup(bot) -> None:
    bot.add_cog(HotReload(bot))

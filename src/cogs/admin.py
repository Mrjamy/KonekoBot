from src.core.checks import Checks
from discord.ext import commands


class Admin(commands.Cog):
    """Commands only for the bot owner"""
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)


def setup(bot):
    bot.add_cog(Admin(bot))

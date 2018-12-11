import random
import src.core.checks as checks
from discord.ext import commands


class Gambling:
    """Class description."""

    __slots__ = 'bot'

    def __init__(self, bot):
        self.bot = bot

    @checks.is_dev()
    @commands.command(pass_context=True)
    async def choice(self, ctx, *choices):
        """Choose from the given options split by \",\" """
        result = random.choice(" ".join(choices).split(","))
        if len(result) > 0:
            await ctx.channel.send(result)
        else:
            await ctx.channel.send(f"I am unable to choose, please refer to `{ctx.prefix}help`")


def setup(bot):
    bot.add_cog(Gambling(bot))

from discord.ext import commands
import random


class Gambling:
    """Class description."""

    __slots__ = 'bot'

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def choice(self, ctx, *choices):
        """Choose from the given options split by \",\" """
        result = random.choice(" ".join(choices).split(","))
        await ctx.channel.send(result)


def setup(bot):
    bot.add_cog(Gambling(bot))

import random
import asyncio
from src.core.checks import Checks
from discord.ext import commands


# TODO: add the option to place a bet of :neko: on the following commands


class Gambling:
    """Gambling commands."""

    __slots__ = 'bot'

    def __init__(self, bot):
        self.bot = bot

    @Checks.is_dev()
    @commands.guild_only()
    @commands.command(aliases=[], pass_context=True)
    async def choice(self, ctx, *choices):
        """Choose from the given options split by \",\" """
        result = random.choice(" ".join(choices).split(","))
        if len(result) > 0:
            await ctx.channel.send(result)
        else:
            await ctx.channel.send(f"I am unable to choose, please refer to `{ctx.prefix}help`")

    # TODO: add options to play blackjack.

    # TODO: add options to play roulette.

    # TODO: add options to play russian roulette.


def setup(bot):
    bot.add_cog(Gambling(bot))

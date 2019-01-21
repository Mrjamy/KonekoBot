import random
import asyncio
from src.core.checks import Checks
from discord.ext import commands
from src.modules.economy.currency import Currency
from src.helpers.misc_helper import Name


# TODO: add the option to place a bet of :neko: on the following commands


class Gambling:
    """Class description."""

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

    # TODO: add command /coinflip
    @commands.command(aliases=['flip', 'toss'], pass_context=True)
    async def coinflip(self, ctx, choice: str = None):
        """Tosses a coin."""
        async def result():
            await asyncio.sleep(5)
            if choice in options:
                if choice == flip:
                    await ctx.channel.send(f'Congratulations {Name.nick_parser(ctx.message.author)}! '
                                           f'you guessed right it was {flip}')
                else:
                    await ctx.channel.send(f'The coin landed on {flip}')
            else:
                await ctx.channel.send(f'The coin landed on {flip}')

        if choice is not None:
            choice = choice.lower()
        options = [
            "heads",
            "tails",
        ]
        await ctx.channel.send('Tossing a coin in the air')

        await ctx.trigger_typing()
        flip = random.choice(options)

        await result()

    # TODO: add options to play blackjack.

    # TODO: add options to play roulette.

    # TODO: add options to play russian roulette.


def setup(bot):
    bot.add_cog(Gambling(bot))

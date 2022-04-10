"""
Module containing gambling related commands.
"""

# Builtins
import asyncio
import logging
import random
from enum import Enum

# Pip
from discord.ext import commands

# Locals
from src.utils.general import NameTransformer

module_logger = logging.getLogger('koneko.Gambling')


class RollMode(Enum):
    DEFAULT = "default"
    ADVANTAGE = "advantage"
    A = "a"
    DISADVANTAGE = "disadvantage"
    D = "d"


# TODO: add the option to place a bet of :neko: on the following commands
class Gambling(commands.Cog):
    """Gambling commands."""

    __slots__ = 'bot',

    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(aliases=['flip', 'toss'])
    async def coinflip(self, ctx: commands.Context, choice: str = None) -> None:
        """Tosses a coin."""
        async def result():
            await asyncio.sleep(5)
            if choice in options:
                if choice == flip:
                    await ctx.channel.send(f'Congratulations {NameTransformer(ctx.message.author)}! '
                                           f'you guessed right it was {flip}')
                else:
                    await ctx.channel.send(f'The coin landed on {flip}')
            else:
                await ctx.channel.send(f'The coin landed on {flip}')

        if choice is not None:
            choice: str = choice.lower()
        options: list = [
            "heads",
            "tails",
        ]
        await ctx.channel.send('Tossing a coin in the air')

        await ctx.trigger_typing()
        flip: str = random.choice(options)

        await result()

    @commands.command()
    async def roll(self, ctx: commands.Context, dice: str, mode: RollMode = RollMode.DEFAULT, keep: int = 1) -> None:
        """Rolls a die in NdN format."""
        try:
            amount, limit = map(int, dice.split('d'))
        except ValueError:
            await ctx.channel.send('Format has to be in NdN!')
            return
        rolls: list = [random.randint(1, limit) for _ in range(amount)]
        if keep <= 0: keep = len(rolls)

        rolls.sort()
        if mode in [RollMode.ADVANTAGE, RollMode.A]:
            mode: RollMode = RollMode.ADVANTAGE
            rolls: list = rolls[-keep:]
        if mode in [RollMode.DISADVANTAGE, RollMode.A]:
            mode: RollMode = RollMode.DISADVANTAGE
            rolls: list = rolls[:keep]

        addition: str = f' with {mode.value}' if mode != RollMode.DEFAULT else ''
        result: str = 'rolled ' + ', '.join(str(roll) for roll in rolls) + addition
        await ctx.channel.send(result)



def setup(bot) -> None:
    """The setup function to add this cog to Koneko."""
    bot.add_cog(Gambling(bot))

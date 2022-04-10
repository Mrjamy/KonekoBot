"""
Module containing gambling related commands.
"""

# Builtins
import asyncio
import logging
import random

# Pip
from discord.ext import commands

# Locals
from src.utils.general import NameTransformer

module_logger = logging.getLogger('koneko.Gambling')


# TODO: add the option to place a bet of :neko: on the following commands
class Gambling(commands.Cog):
    """Gambling commands."""

    __slots__ = 'bot',

    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(aliases=['flip', 'toss'])
    async def coinflip(self, ctx, choice: str = None) -> None:
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
            choice = choice.lower()
        options = [
            "heads",
            "tails",
        ]
        await ctx.channel.send('Tossing a coin in the air')

        await ctx.trigger_typing()
        flip = random.choice(options)

        await result()


def setup(bot) -> None:
    """The setup function to add this cog to Koneko."""
    bot.add_cog(Gambling(bot))

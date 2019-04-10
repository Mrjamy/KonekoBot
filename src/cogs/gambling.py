# Builtins
import random
import asyncio

# Pip
import discord
from discord.ext import commands

# Locals
from src.core.checks import Checks
from src.core.exceptions import NotEnoughBalance
from src.utils.database.repositories.currency_repository import CurrencyRepository
from src.utils.games.slotmachine import Slots
from src.utils.user.nick_helper import Name


# TODO: add the option to place a bet of :neko: on the following commands
class Gambling(commands.Cog):
    """Gambling commands."""

    __slots__ = 'bot', 'currency_repository'

    def __init__(self, bot):
        self.bot = bot
        self.currency_repository = CurrencyRepository()

    # TODO: add options to play blackjack.

    # TODO: add options to play roulette.

    # TODO: add options to play russian roulette.

    @commands.guild_only()
    @commands.command(aliases=['flip', 'toss'])
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

    @commands.guild_only()
    @commands.command(aliases=["bet"])
    async def gamble(self, ctx, amount: int = 100):
        """Gambles an amount of :nekko:."""

        balance = await self.currency_repository.get(ctx.author.id, ctx.guild.id)

        if not 0 <= amount <= balance.amount:
            raise NotEnoughBalance

        if random.randint(1, 100) > 51:
            await self.currency_repository.update(ctx.author.id, ctx.guild.id, +amount)
            await ctx.channel.send('Congratulations you doubled your bet!')
        else:
            await self.currency_repository.update(ctx.author.id, ctx.guild.id, -amount)
            await ctx.channel.send('Unfortunately you lost :(')

    @commands.command()
    async def slots(self, ctx, bet: int = 10):
        """Play a game of slots."""
        balance = await self.currency_repository.get(ctx.author.id, ctx.guild.id)

        if not 0 <= bet <= balance.amount:
            raise NotEnoughBalance

        mutation = -bet
        slotmachine = Slots(bet=bet)
        slotmachine._play_round()
        mutation += bet * slotmachine.win

        await self.currency_repository.update(ctx.author.id, ctx.guild.id, mutation)

        # TODO: add emojoi\'s to the embed.
        embed = discord.Embed(title=f"You pulled the slots! \n {slotmachine.slots}",
                              color=discord.Color.dark_purple())
        await ctx.channel.send(embed=embed)

        embed = discord.Embed(title=f"Your bet {bet}, {slotmachine.msg}",
                              color=discord.Color.dark_purple())
        await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Gambling(bot))

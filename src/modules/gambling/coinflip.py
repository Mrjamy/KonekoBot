import random
import asyncio
from discord.ext import commands
from src.helpers.user.nick_helper import Name
from src.helpers.database.models.currency_model import Currency as Model
from src.core.exceptions import NotEnoughBalance


class Gambling(commands.Cog):
    """Command coinflip."""

    __slots__ = 'bot'

    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
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


def setup(bot):
    bot.add_cog(Gambling(bot))

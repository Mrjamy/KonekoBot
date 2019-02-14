import random
from discord.ext import commands
from src.helpers.database.models.currency_model import Currency as Model
from src.core.exceptions import NotEnoughBalance


class Gambling:
    """Command gamble."""

    __slots__ = 'bot'

    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(aliases=[], pass_context=True)
    async def gamble(self, ctx, amount: int = 100):
        """Gambles an amount of :nekko:."""

        balance = Model().get(ctx.author.id, ctx.guild.id)

        if not 0 <= amount <= balance.amount:
            raise NotEnoughBalance

        if random.randint(1, 100) > 51:
            Model().update(ctx.author.id, ctx.guild.id, +amount)
            await ctx.channel.send('Congratulations you doubled your bet!')
        else:
            Model().update(ctx.author.id, ctx.guild.id, -amount)
            await ctx.channel.send('Unfortunately you lost :(')


def setup(bot):
    bot.add_cog(Gambling(bot))

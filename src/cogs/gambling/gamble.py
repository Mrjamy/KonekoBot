import random
from discord.ext import commands
from src.helpers.database.repositories.currency_repository import CurrencyRepository
from src.core.exceptions import NotEnoughBalance


class Gambling(commands.Cog):
    """Command gamble."""

    __slots__ = 'bot', 'currency_repository'

    def __init__(self, bot):
        self.bot = bot
        self.currency_repository = CurrencyRepository()

    @commands.guild_only()
    @commands.command(aliases=["bet"], pass_context=True)
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


def setup(bot):
    bot.add_cog(Gambling(bot))

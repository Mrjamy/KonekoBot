import discord
from discord.ext import commands
from src.helpers.games.slotmachine import SlotMachine
from src.helpers.database.models.currency_model import Currency as Model
from src.core.exceptions import NotEnoughBalance


class Games:
    """Some fun games."""

    __slots__ = 'bot'

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=[], pass_context=True)
    async def slots(self, ctx, bet: int = 10):
        """Play a game of slots."""
        balance = Model().get(ctx.author.id, ctx.guild.id)

        if not 0 <= bet <= balance.amount:
            raise NotEnoughBalance

        slotmachine = SlotMachine()

        mutation = bet * slotmachine._play_round()
        Model().update(ctx.author.id, ctx.guild.id, mutation)

        embed = discord.Embed(title=f"You pulled the slots! \n {slotmachine.slots}",
                              color=discord.Color.dark_purple())
        await ctx.channel.send(embed=embed)

        embed = discord.Embed(title=f"Your bet {bet}, {slotmachine.message}",
                              color=discord.Color.dark_purple())
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Games(bot))

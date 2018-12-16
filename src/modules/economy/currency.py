import discord
from src.core.checks import Checks
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from src.services.database.models import currency_model as model


class NotEnoughBalance(Exception):
    pass


class Currency:
    """Currency module."""

    __slots__ = ['bot', 'engine', 'session']

    def __init__(self, bot):
        db_uri = 'sqlite:///src/core/data/currency.sqlite'

        self.bot = bot
        self.engine = create_engine(db_uri)
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()

    @commands.guild_only()
    @commands.command(aliases=['balance', 'neko'], pass_context=True)
    async def coins(self, ctx, user=None):
        """Get your total balance."""

        if len(ctx.message.mentions) == 1:
            user = ctx.message.mentions[0]
        else:
            user = ctx.author

        balance = self.session.query(model.Currency) \
            .filter(
                model.Currency.snowflake == user.id,
                model.Currency.guild == ctx.guild.id
            ) \
            .first()
        if balance is None:
            balance = await self.add_user(ctx.guild.id, ctx.author.id)

        embed = discord.Embed(title=f'`{user.name}` has {balance.amount} <:neko:521458388513849344>',
                              color=discord.Color.green())
        await ctx.channel.send(embed=embed)

    @commands.cooldown(1, 60 * 60 * 24, BucketType.member)
    @commands.guild_only()
    @commands.command(aliases=['login', 'daily'], pass_context=True)
    async def claim(self, ctx):
        """Claim your daily login reward."""

        currency = self.session.query(model.Currency) \
            .filter(
                model.Currency.snowflake == ctx.author.id,
                model.Currency.guild == ctx.guild.id
            ) \
            .first()
        if currency is None:
            currency = await self.add_user(ctx.guild.id, ctx.author.id)

        await self.add_currency(currency)
        embed = discord.Embed(title=f'`{ctx.author.name}` claimed their daily login reward',
                              color=discord.Color.green())
        await ctx.channel.send(embed=embed)

    @commands.guild_only()
    @commands.command(pass_context=True)
    async def transfer(self, ctx, user, amount: int):
        """Transfers an amount of coins to a user."""

        if len(ctx.message.mentions) == 1:
            user = ctx.message.mentions[0]
        else:
            embed = discord.Embed(title=f'Could not find a user to transfer the <:neko:521458388513849344> to.',
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed)
            return

        await self._take(ctx.author, ctx.guild, amount)
        await self._give(user, ctx.guild, amount)

        embed = discord.Embed(title=f'{ctx.author.name} successfully transferred {amount} '
                                    f'<:neko:521458388513849344> to {user.name}.',
                              color=discord.Color.green())
        await ctx.channel.send(embed=embed)

    @Checks.is_owner()
    @commands.guild_only()
    @commands.command(pass_context=True)
    async def give(self, ctx, user, amount: int):
        """Give a certain amount of currency to a user."""

        if len(ctx.message.mentions) == 1:
            user = ctx.message.mentions[0]
        else:
            embed = discord.Embed(title=f'Could not find a user to transfer the <:neko:521458388513849344> to.',
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed)
            return

        await self._give(user, ctx.guild, amount)

        embed = discord.Embed(title=f'{ctx.author.name} gave {amount} <:neko:521458388513849344> to {user.name}',
                              color=discord.Color.green())
        await ctx.channel.send(embed=embed)

    async def _give(self, user, guild, amount: int):
        currency = self.session.query(model.Currency) \
            .filter(
                model.Currency.snowflake == user.id,
                model.Currency.guild == guild.id
            ) \
            .first()
        if currency is None:
            currency = await self.add_user(guild.id, user.id)

        await self.add_currency(currency, amount)

    @Checks.is_owner()
    @commands.guild_only()
    @commands.command(pass_context=True)
    async def take(self, ctx, user, amount: int):
        """Take a certain amount of currency from a user."""

        if len(ctx.message.mentions) == 1:
            user = ctx.message.mentions[0]
        else:
            embed = discord.Embed(title=f'Could not find a user to remove <:neko:521458388513849344> from.',
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed)
            return

        await self._take(user, ctx.guild, amount)

        embed = discord.Embed(title=f'{ctx.author.name} took {amount} <:neko:521458388513849344> from {user.name}',
                              color=discord.Color.green())
        await ctx.channel.send(embed=embed)

    async def _take(self, user, guild, amount: int):
        currency = self.session.query(model.Currency) \
            .filter(
                model.Currency.snowflake == user.id,
                model.Currency.guild == guild.id
            ) \
            .first()
        if currency is None:
            currency = await self.add_user(guild.id, user.id)

        if currency.amount < amount:
            raise NotEnoughBalance

        await self.add_currency(currency, -amount)

    async def add_user(self, guild, user):

        currency = model.Currency()
        currency.snowflake = user
        currency.guild = guild
        currency.amount = 0

        try:
            self.session.add(currency)
            self.session.commit()
        except SQLAlchemyError as e:
            print(e)
            return
        return currency

    async def add_currency(self, user, amount: int=100):
        user.amount += amount
        try:
            self.session.commit()
        except SQLAlchemyError as e:
            print(e)
            return
        return user


def setup(bot):
    bot.add_cog(Currency(bot))

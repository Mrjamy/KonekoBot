"""
Module containing currency related commands.
"""

# Builtins
import logging

# Pip
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

# Locals
from src.core.exceptions import NotEnoughBalance
from src.utils.database.repositories.currency_repository import \
    CurrencyRepository
from src.utils.emojis.emoji import Emoji
from src.utils.user.nick_helper import Name

module_logger = logging.getLogger('koneko.Currency')


class Currency(commands.Cog):
    """Currency module."""

    __slots__ = 'bot', 'currency_repository', 'emoji'

    def __init__(self, bot):
        self.bot = bot
        self.currency_repository = CurrencyRepository()
        self.emoji = Emoji()

    async def balance_check(self, user_id: int, guild_id: int, amount: int) -> bool:
        """Check if the user has enough balance"""
        balance = await self.currency_repository.get(user_id, guild_id)

        if not bool(balance.amount >= amount):
            raise NotEnoughBalance
        return True

    @commands.guild_only()
    @commands.command(aliases=['balance', 'neko'])
    async def coins(self, ctx, user: discord.User = None) -> None:
        """Get your total balance."""

        if user is None:
            user = ctx.author

        balance = await self.currency_repository.get(user.id, ctx.guild.id)

        embed = discord.Embed(title=f'`{Name.nick_parser(user)}` has {balance.amount} {self.emoji.cash}',
                              color=discord.Color.green())
        await ctx.channel.send(embed=embed)

    @commands.cooldown(1, 60 * 60 * 20, BucketType.member)
    @commands.guild_only()
    @commands.command(aliases=['login', 'daily'])
    async def claim(self, ctx) -> None:
        """Claim your daily login reward."""

        balance = await self.currency_repository.update(ctx.author.id, ctx.guild.id, +100)

        embed = discord.Embed(title=f'`{Name.nick_parser(ctx.message.author)}` claimed their daily login reward your '
                                    f'new balance is {balance.amount} {self.emoji.cash}',
                              color=discord.Color.green())
        await ctx.channel.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def transfer(self, ctx, user: discord.User, amount: int) -> None:
        """Transfers an amount of coins to a user."""

        if amount <= 0:
            return

        author_id = ctx.author.id
        guild_id = ctx.guild.id

        if await self.balance_check(author_id, ctx.guild.id, amount):
            await self.currency_repository.update(author_id, guild_id, -amount)
            await self.currency_repository.update(user.id, guild_id, +amount)

            embed = discord.Embed(title=f'{Name.nick_parser(ctx.message.author)} successfully transferred {amount} '
                                        f'{self.emoji.cash} to {Name.nick_parser(user)}.',
                                  color=discord.Color.green())
            await ctx.channel.send(embed=embed)

    @commands.is_owner()
    @commands.guild_only()
    @commands.command(hidden=True)
    async def give(self, ctx, user: discord.User, amount: int) -> None:
        """Give a certain amount of currency to a user."""

        if amount <= 0:
            return

        await self.currency_repository.update(user.id, ctx.guild.id, amount)

        embed = discord.Embed(title=f'{Name.nick_parser(ctx.message.author)} gave {amount} {self.emoji.cash} '
                                    f'to {Name.nick_parser(user)}',
                              color=discord.Color.green())
        await ctx.channel.send(embed=embed)

    @commands.is_owner()
    @commands.guild_only()
    @commands.command(hidden=True)
    async def take(self, ctx, user: discord.User, amount: int) -> None:
        """Take a certain amount of currency from a user."""

        await self.currency_repository.update(user.id, ctx.guild.id, -amount)

        embed = discord.Embed(title=f'{Name.nick_parser(ctx.message.author)} took {amount} {self.emoji.cash} '
                                    f'from {Name.nick_parser(user)}',
                              color=discord.Color.green())
        await ctx.channel.send(embed=embed)

    @commands.guild_only()
    @commands.command(aliases=['fortune'])
    async def wealth(self, ctx, rank: int = 1) -> None:
        """Shows the server's wealth."""
        rank -= 1
        if rank < 0:
            rank = 0
            count = 1
        else:
            count = rank + 1

        wealth = await self.currency_repository.get_all(ctx.guild.id, rank)

        embed = discord.Embed(title=f'{ctx.guild.name}\'s wealth overview:',
                              color=discord.Color.green())

        if len(wealth) >= 1:
            for user in wealth:
                u = ctx.guild.get_member(int(user.snowflake))
                if user.amount > 0:
                    try:
                        embed.add_field(
                            name=f'#{count} {Name.nick_parser(u)}',
                            value=f'{user.amount} {self.emoji.cash}',
                            inline=False
                        )
                        count += 1
                    except AttributeError:
                        pass
        else:
            embed.add_field(
                name='Error: ',
                value='No users found for this range',
                inline=False
            )

        await ctx.channel.send(embed=embed)


def setup(bot) -> None:
    """The setup function to add this cog to Koneko."""
    bot.add_cog(Currency(bot))

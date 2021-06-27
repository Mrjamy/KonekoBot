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
from src.utils.database.postgress.repositories.currency_repository import \
    CurrencyRepository
from src.utils.general import DiscordEmbed, Emoji, NameTransformer

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

        await DiscordEmbed.confirm(ctx, title=f'`{NameTransformer(user)}` has {balance.amount} {self.emoji.cash}')

    @commands.cooldown(1, 60 * 60 * 20, BucketType.member)
    @commands.guild_only()
    @commands.command(aliases=['login', 'daily'])
    async def claim(self, ctx) -> None:
        """Claim your daily login reward."""

        balance = await self.currency_repository.update(ctx.author.id, ctx.guild.id, +100)

        await DiscordEmbed.confirm(ctx, title=f'`{NameTransformer(ctx.message.author)}` claimed their daily login reward your new balance is {balance.amount} {self.emoji.cash}')

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

            await DiscordEmbed.confirm(ctx, title=f'{NameTransformer(ctx.message.author)} successfully transferred {amount} {self.emoji.cash} to {NameTransformer(user)}.')

    @commands.is_owner()
    @commands.guild_only()
    @commands.command(hidden=True)
    async def give(self, ctx, user: discord.User, amount: int) -> None:
        """Give a certain amount of currency to a user."""

        if amount <= 0:
            return

        await self.currency_repository.update(user.id, ctx.guild.id, amount)

        await DiscordEmbed.confirm(ctx, title=f'{NameTransformer(ctx.message.author)} gave {amount} {self.emoji.cash} to {NameTransformer(user)}')

    @commands.is_owner()
    @commands.guild_only()
    @commands.command(hidden=True)
    async def take(self, ctx, user: discord.User, amount: int) -> None:
        """Take a certain amount of currency from a user."""

        await self.currency_repository.update(user.id, ctx.guild.id, -amount)

        await DiscordEmbed.confirm(ctx, title=f'{NameTransformer(ctx.message.author)} took {amount} {self.emoji.cash} from {NameTransformer(user)}')

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

        parts = []
        if len(wealth) >= 1:
            for user in wealth:
                if user.amount > 0:
                    u = ctx.guild.get_member(int(user.snowflake))

                    parts.append({
                        'name': f'#{count} {NameTransformer(u)}',
                        'value': f'{user.amount} {self.emoji.cash}'
                    })
                    count += 1
        else:
            parts.append({
                'name': 'Error',
                'value': 'No users found for this range',
            })

        await DiscordEmbed.confirm(ctx, parts, title=f'{ctx.guild.name}\'s wealth overview:')


def setup(bot) -> None:
    """The setup function to add this cog to Koneko."""
    bot.add_cog(Currency(bot))

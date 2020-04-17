# Builtins
import logging

# Pip
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

# Locals
from src.utils.database.repositories.currency_repository import CurrencyRepository
from src.utils.emojis.emoji import Emoji
from src.utils.user.nick_helper import Name

module_logger = logging.getLogger('koneko.Currency')


class Currency(commands.Cog):
    """Currency module."""

    __slots__ = 'bot', 'currency_repository', 'emoji'

    def __init__(self, bot):
        self.bot = bot
        self.currency_repository = CurrencyRepository()
        self.emoji = Emoji(bot)

    @commands.guild_only()
    @commands.command(aliases=['balance', 'neko'])
    async def coins(self, ctx, user=None):
        """Get your total balance."""

        # TODO: add user transformer in function argument

        if len(ctx.message.mentions) == 1:
            user = ctx.message.mentions[0]
        else:
            user = ctx.author

        balance = await self.currency_repository.get(user.id, ctx.guild.id)

        embed = discord.Embed(title=f'`{Name.nick_parser(user)}` has {balance.amount} {self.emoji.cash}',
                              color=discord.Color.green())
        await ctx.channel.send(embed=embed)

    @commands.cooldown(1, 60 * 60 * 20, BucketType.member)
    @commands.guild_only()
    @commands.command(aliases=['login', 'daily'])
    async def claim(self, ctx):
        """Claim your daily login reward."""

        balance = await self.currency_repository.update(ctx.author.id, ctx.guild.id, +100)

        embed = discord.Embed(title=f'`{Name.nick_parser(ctx.message.author)}` claimed their daily login reward your '
                                    f'new balance is {balance.amount} {self.emoji.cash}',
                              color=discord.Color.green())
        await ctx.channel.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def transfer(self, ctx, user, amount: int):
        """Transfers an amount of coins to a user."""

        # TODO: add user transformer in function argument

        if amount <= 0:
            return
        if len(ctx.message.mentions) == 1:
            user = ctx.message.mentions[0]
        else:
            embed = discord.Embed(title=f'Could not find a user to transfer the {self.emoji.cash} to.',
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed)
            return

        await self.currency_repository.update(ctx.author.id, ctx.guild.id, -amount)
        await self.currency_repository.update(user.id, ctx.guild.id, +amount)

        embed = discord.Embed(title=f'{Name.nick_parser(ctx.message.author)} successfully transferred {amount} '
                                    f'{self.emoji.cash} to {Name.nick_parser(user)}.',
                              color=discord.Color.green())
        await ctx.channel.send(embed=embed)

    @commands.is_owner()
    @commands.guild_only()
    @commands.command(hidden=True)
    async def give(self, ctx, user, amount: int):
        """Give a certain amount of currency to a user."""

        # TODO: add user transformer in function argument

        if amount <= 0:
            return
        if len(ctx.message.mentions) == 1:
            user = ctx.message.mentions[0]
        else:
            embed = discord.Embed(title=f'Could not find a user to give the {self.emoji.cash} to.',
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed)
            return

        await self.currency_repository.update(user.id, ctx.guild.id, amount)

        embed = discord.Embed(title=f'{Name.nick_parser(ctx.message.author)} gave {amount} {self.emoji.cash} '
                                    f'to {Name.nick_parser(user)}',
                              color=discord.Color.green())
        await ctx.channel.send(embed=embed)

    @commands.is_owner()
    @commands.guild_only()
    @commands.command(hidden=True)
    async def take(self, ctx, user, amount: int):
        """Take a certain amount of currency from a user."""

        # TODO: add user transformer in function argument

        if len(ctx.message.mentions) == 1:
            user = ctx.message.mentions[0]
        else:
            embed = discord.Embed(title=f'Could not find a user to remove {self.emoji.cash} from.',
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed)
            return

        await self.currency_repository.update(user.id, ctx.guild.id, -amount)

        embed = discord.Embed(title=f'{Name.nick_parser(ctx.message.author)} took {amount} {self.emoji.cash} '
                                    f'from {Name.nick_parser(user)}',
                              color=discord.Color.green())
        await ctx.channel.send(embed=embed)

    @commands.guild_only()
    @commands.command(aliases=['fortune'])
    async def wealth(self, ctx, rank: int = 1):
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


def setup(bot):
    bot.add_cog(Currency(bot))

"""
Module containing commands related to the leveling system.
"""

# Builtins
import logging

# Pip
import discord
from discord.ext import commands

# Locals
from src.utils.database.repositories.level_repository import LevelRepository
from src.utils.general import DiscordEmbed, NameTransformer

module_logger = logging.getLogger('koneko.Level')


class Level(commands.Cog):
    """Leveling module."""

    __slots__ = 'bot', 'level_repository'

    def __init__(self, bot):
        self.bot = bot
        self.level_repository = LevelRepository()

    # TODO: send a fancy card then responding.
    @commands.guild_only()
    @commands.command(aliases=['xp', 'exp', 'experience'])
    async def level(self, ctx, user: discord.User = None) -> None:
        """Shows your xp stats."""

        if user is None:
            user = ctx.author
        if user.bot:
            embed = discord.Embed(title='This is a bot.',
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed)
            return

        level = await self.level_repository.get(user.id, ctx.guild.id)

        up = (level.level + 1) ** 4

        await DiscordEmbed.confirm(ctx, title=f'`{NameTransformer(user)}` '
                                              f'is level {level.level}, '
                                              f'{level.experience}/{up} xp')

    @commands.guild_only()
    @commands.command(aliases=['score', 'levels'])
    async def scoreboard(self, ctx, rank: int = 1) -> None:
        """Shows the server's scoreboard."""
        rank -= 1
        if rank <= 0:
            rank = 0
            count = 1
        else:
            count = rank + 1

        levels = await self.level_repository.get_all(ctx.guild.id, rank)

        parts = []
        if len(levels) >= 1:
            for user in levels:
                if user.experience > 0:
                    u = ctx.guild.get_member(int(user.snowflake))

                    parts.append({
                        'name': f'#{count} {NameTransformer(u)}',
                        'value': f'Level {user.level}, '
                                 f'{user.experience}/{(user.level + 1) ** 4} xp'
                    })
                    count += 1
        else:
            parts.append({
                'name': 'Error',
                'value': 'No users found for this range',
            })

        await DiscordEmbed.confirm(ctx, parts, title=f'{ctx.guild.name}\'s '
                                                     f'scoreboard:')

    @commands.Cog.listener()
    async def on_member_join(self, member) -> None:
        """Stores the user in the database whenever a new user joins."""
        await self.level_repository.get(member.id, member.guild.id)

    @commands.Cog.listener()
    async def on_message(self, ctx) -> None:
        """Whenever a user sends a message award them with some exp."""
        if ctx.author.bot:
            return
        if not ctx.guild:
            return

        await self.level_repository.add_xp(ctx.author.id, ctx.guild.id)
        up = await self.level_repository.levelup_check(ctx.author.id,
                                                       ctx.guild.id)
        level = await self.level_repository.get(ctx.author.id, ctx.guild.id)

        if up:
            # Send an embedded message to notify an user upon leveling up.
            try:
                await DiscordEmbed.message(
                    ctx, title=f'`{NameTransformer(ctx.author)}` '
                               f'has leveled up to level {level.level}')
            except discord.errors.Forbidden:
                # Could not send embedded message, try normal message.
                try:
                    await ctx.channel.send(
                        f'`{NameTransformer(ctx.author)}` has leveled up to '
                        f'level {level.level}')
                #  No message could be delivered.
                except discord.errors.Forbidden:
                    pass


def setup(bot) -> None:
    """The setup function to add this cog to Koneko."""
    bot.add_cog(Level(bot))

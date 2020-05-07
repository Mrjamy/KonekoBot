# Builtins
import logging

# Pip
import discord
from discord.ext import commands

# Locals
from src.utils.database.repositories.level_repository import LevelRepository
from src.utils.user.nick_helper import Name

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
            embed = discord.Embed(title=f'This is a bot.',
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed)
            return

        level = await self.level_repository.get(user.id, ctx.guild.id)

        up = (level.level + 1) ** 4
        embed = discord.Embed(title=f'`{Name.nick_parser(user)}` is level {level.level}, {level.experience}/{up} xp',
                              color=discord.Color.green())
        await ctx.channel.send(embed=embed)

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

        levels = await self.level_repository.get_all(ctx.guild.id)

        embed = discord.Embed(title=f'{ctx.guild.name}\'s scoreboard:',
                              color=discord.Color.green())

        if len(levels) >= 1:
            for user in levels:
                u = ctx.guild.get_member(int(user.snowflake))
                up = (user.level + 1) ** 4
                if user.experience > 0:
                    try:
                        embed.add_field(
                            name=f'#{count} {Name.nick_parser(u)}',
                            value=f'Level {user.level}, {user.experience}/{up} xp',
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
            try:
                embed = discord.Embed(
                    title=f'`{Name.nick_parser(ctx.author)}` has leveled up to level '
                          f'{level.level}',
                    color=discord.Color.dark_purple())
                await ctx.channel.send(embed=embed)
            except discord.errors.Forbidden:
                try:
                    await ctx.channel.send(
                        f'`{Name.nick_parser(ctx.author)}` has leveled up to level '
                        f'{level.level}')
                except discord.errors.Forbidden:
                    pass


def setup(bot) -> None:
    bot.add_cog(Level(bot))

import discord
from discord.ext import commands
from src.helpers.database.models.level_model import Level as Model
from src.helpers.user.nick_helper import Name


class Level(commands.Cog):
    """Leveling module."""

    __slots__ = 'bot'

    def __init__(self, bot):
        self.bot = bot

    # TODO: send a fancy card then responding.
    @commands.guild_only()
    @commands.command(aliases=['xp', 'exp', 'experience'], pass_context=True)
    async def level(self, ctx, user=None):
        """Shows your xp stats."""

        if len(ctx.message.mentions) == 1:
            if ctx.author.bot:
                embed = discord.Embed(title=f'This user is a bot.',
                                      color=discord.Color.red())
                await ctx.channel.send(embed=embed)
                return
            user = ctx.message.mentions[0]
        else:
            user = ctx.author

        level = Model().get(user.id, ctx.guild.id)

        up = (level.level + 1) ** 4
        embed = discord.Embed(title=f'`{Name.nick_parser(user)}` is level {level.level}, {level.experience}/{up} xp',
                              color=discord.Color.green())
        await ctx.channel.send(embed=embed)

    @commands.guild_only()
    @commands.command(aliases=['score', 'levels'], pass_context=True)
    async def scoreboard(self, ctx, rank: int = 1):
        """Shows the server's scoreboard."""
        rank -= 1
        if rank <= 0:
            rank = 0
            count = 1
        else:
            count = rank + 1

        levels = Model().get_all(ctx.guild.id)

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
    async def on_member_join(self, member):
        """Stores the user in the database whenever a new user joins."""
        await Model().insert(member.id, member.guild.id)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        """Whenever a user sends a message award them with a small amount of exp."""
        if ctx.author.bot:
            return
        if not ctx.guild:
            return

        level = Model().get(ctx.author.id, ctx.guild.id)
        await self.level_up(level, ctx)

    async def level_up(self, user, ctx):
        up = Model().levelup_check(ctx.author.id, ctx.guild.id)
        level = Model().get(ctx.author.id, ctx.guild.id)

        if up:
            try:
                embed = discord.Embed(title=f'`{Name.nick_parser(ctx.author)}` has leveled up to level '
                                            f'{level.level}',
                                      color=discord.Color.dark_purple())
                await ctx.channel.send(embed=embed)
            except discord.errors.Forbidden:
                try:
                    await ctx.channel.send(f'`{Name.nick_parser(ctx.author)}` has leveled up to level '
                                           f'{level.level}')
                except discord.errors.Forbidden:
                    pass


def setup(bot):
    bot.add_cog(Level(bot))

import random
import discord
from datetime import datetime
from discord.ext import commands
from KonekoBot import KonekoBot
from src.services.database.models import level_model as model
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError


class Level:
    """Leveling module."""

    __slots__ = ['bot', 'engine', 'session']

    def __init__(self, bot):
        db_uri = 'sqlite:///src/core/data/level.sqlite'

        self.bot = bot
        self.engine = create_engine(db_uri)
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()

    # TODO: add param user = None for help mapping
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

        level = self.session.query(model.Level)\
            .filter(
                model.Level.snowflake == user.id,
                model.Level.guild == ctx.guild.id
            )\
            .first()
        if level is None:
            level = await self.add_user(ctx.guild.id, ctx.author.id)

        up = (level.level + 1) ** 4
        embed = discord.Embed(title=f'`{user.name}` is level {level.level}, {level.experience}/{up} xp',
                              color=discord.Color.green())
        await ctx.channel.send(embed=embed)

    @KonekoBot.event
    async def on_member_join(self, member):
        """Stores the user in the database whenever a new user joins."""
        await self.add_user(member.guild.id, member.id)

    @KonekoBot.event
    async def on_message(self, ctx):
        """Whenever a user sends a message award them with a small amount of exp."""
        if ctx.author.bot:
            return
        if not ctx.guild:
            return

        level = self.session.query(model.Level)\
            .filter(
                model.Level.snowflake == ctx.author.id,
                model.Level.guild == ctx.guild.id
            )\
            .first()
        if level is None:
            level = await self.add_user(ctx.guild.id, ctx.author.id)

        level = await self.add_experience(level)

        await self.level_up(level, ctx)

    # TODO: remove the user's entry from the database
    @KonekoBot.event
    async def on_member_leave(self):
        return

    async def add_user(self, guild, user):

        level = model.Level()
        level.snowflake = user
        level.guild = guild

        try:
            self.session.add(level)
            self.session.commit()
        except SQLAlchemyError as e:
            print(e)
            return
        return level

    async def add_experience(self, user):
        if not await self._cooldown(user):
            user.experience += random.randint(5, 10)
            user.last_message = datetime.now()
            try:
                self.session.commit()
            except SQLAlchemyError as e:
                print(e)
                return
            return user
        return user

    async def level_up(self, user, ctx):
        experience = user.experience
        lvl_start = user.level
        lvl_end = int(experience ** (1/4))

        if lvl_start < lvl_end:
            embed = discord.Embed(title=f'`{ctx.author.name}` has leveled up to level {lvl_end}',
                                  color=discord.Color.dark_purple())
            await ctx.channel.send(embed=embed)
            user.level = lvl_end

        try:
            self.session.commit()
        except SQLAlchemyError as e:
            print(e)
            return
        return user

    async def _cooldown(self, user):
        return (datetime.now() - user.last_message).total_seconds() < 30


def setup(bot):
    bot.add_cog(Level(bot))

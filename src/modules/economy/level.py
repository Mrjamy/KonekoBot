import json
import os
import time
import random
from discord.ext import commands
from KonekoBot import KonekoBot


class Level:
    """Leveling module."""

    __slots__ = ['bot', 'data']

    def __init__(self, bot):
        dir = os.path.dirname(__file__)

        self.bot = bot
        # TODO: move users.json to src/core/data/
        self.data = os.path.join(dir, 'users.json')

    # TODO: add option for mentioning a user.
    # TODO: send a fancy card then responding.
    @commands.guild_only()
    @commands.command(aliases=['xp', 'exp', 'experience'], pass_context=True)
    async def level(self, ctx, user=None):
        """Shows your xp stats. Specify the user to show that user's stats instead."""
        if user is not None:
            await ctx.channel.send('The user parameter is not yet supported, hold tight!')

        with open(self.data, 'r') as f:
            users = json.load(f)

        key = f'{ctx.author.id} - {ctx.guild.id}'

        up = (users[key]['level'] + 1) ** 4
        xp = users[key]['experience']

        try:
            if key in users:
                await ctx.channel.send(f'You are level {users[key]["level"]}, {xp}/{up} xp')
        except KeyError:
            await ctx.channel.send('You don\'t have a level yet, try saying something!')

    @KonekoBot.event
    async def on_member_join(self, member):
        """Stores the user in the database whenever a new user joins."""
        with open(self.data, 'r') as f:
            users = json.load(f)

        guild = member.guild.id
        await self.add_user(users, guild, member.id)

        with open(self.data, 'w') as f:
            json.dump(users, f, indent=4, sort_keys=True)

    @KonekoBot.event
    async def on_message(self, ctx):
        """Whenever a user sends a message award them with a small amount of exp."""
        if ctx.author.bot:
            return
        if not ctx.guild:
            return

        with open(self.data, 'r') as f:
            users = json.load(f)

        guild = str(ctx.guild.id)
        user = str(ctx.author.id)
        await self.add_user(users, guild, user)
        await self.add_experience(users, guild, user)
        await self.level_up(users, guild, ctx.author, ctx)

        with open(self.data, 'w') as f:
            json.dump(users, f, indent=4, sort_keys=True)

    # TODO: remove the user's entry from the json file.
    @KonekoBot.event
    async def on_member_leave(self):
        return

    async def add_user(self, users, guild, user):
        key = f'{user} - {guild}'
        if key not in users:
            users[key] = {}
            users[key]['experience'] = 0
            users[key]['last_message'] = time.time()
            users[key]['level'] = 1

    async def add_experience(self, users, guild, user):
        if not await self._cooldown(users, guild, user):
            key = f'{user} - {guild}'
            users[key]['experience'] += random.randint(5, 10)
            users[key]['last_message'] = time.time()

    async def level_up(self, users, guild, user, ctx):
        key = f'{user.id} - {guild}'
        experience = users[key]['experience']
        lvl_start = users[key]['level']
        lvl_end = int(experience ** (1/4))

        if lvl_start < lvl_end:
            await ctx.channel.send(f'{user.mention} has leveled up to level {lvl_end}')
            users[key]['level'] = lvl_end

    async def _cooldown(self, users, guild, user):
        key = f'{user} - {guild}'
        last = users[key]['last_message']

        return (round(time.time() - last)) < 30


def setup(bot):
    bot.add_cog(Level(bot))

#     y = x ^ (1/4)
#     y < 5

625

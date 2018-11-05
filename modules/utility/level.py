# TODO: add cards for display.

# TODO: Command - !xp (get user's card.)

# TODO: Command - !levels (get the server's scoreboard.)

import random
import time
from KonekoBot import bot as koneko
from services.database.cursors.xp import XP
from discord.ext import commands


class Level:
    def __init__(self, bot):
        self.bot = bot

    @koneko.event
    async def on_message(self, ctx):
        """Get the user's level progress."""
        if ctx.author == self.bot.user:
            return
        if ctx.author.bot:
            return

        author = ctx.author.id
        guild = ctx.guild.id
        xp_reward = random.randint(1, 11)
        timestamp = time.time()
        timeout = 30

        u_obj = XP.get_xp(author, guild)
        old_timestamp = timestamp
        current_xp = 0

        if u_obj is not None:
            old_timestamp = u_obj[2]
            current_xp = u_obj[3]

        if old_timestamp + timeout < timestamp:
            XP.add_xp_to_user(author, guild, current_xp + xp_reward, timestamp)

        # TODO: send message on level up.
        # card = "card here"
        # msg = "Inprogress!"
        # await ctx.channel.send(msg)

    @commands.command()
    async def xp(self, ctx):
        # TODO: add description.
        author = ctx.author.id
        guild = ctx.guild.id
        u_obj = XP.get_xp(author, guild)
        # TODO: add card.
        if u_obj is not None:
            msg = "Your xp is {0}!".format(u_obj[3])
        else:
            msg = "You dont have any xp yet, start earning xp by typing."
        await ctx.channel.send(msg)

    @commands.command()
    async def leaderboard(self, ctx):
        # TODO: add description.
        # TODO: implement leaderboard.
        msg = "Inprogress!"
        await ctx.channel.send(msg)


def setup(bot):
    bot.add_cog(Level(bot))

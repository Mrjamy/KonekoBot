# TODO: add table for xp.

# TODO: get user current xp.

# TODO: get last message send by user (time).

# TODO: add xp to retreived.

# TODO: store xp

# TODO: update last timestamp.

# TODO: add cards for display.

# TODO: Command - !xp (get user's card.)

# TODO: Command - !levels (get the server's scoreboard.)

import random
import time
from KonekoBot import bot as koneko
from services.database.cursors.xp import XP


class Level:
    def __init__(self, bot):
        self.bot = bot

    @koneko.event
    async def on_message(self, ctx):
        """Get the user's level progress."""
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


def setup(bot):
    bot.add_cog(Level(bot))

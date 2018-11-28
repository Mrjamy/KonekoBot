from discord.ext import commands
import random

# TODO: add a dungeon/dnd based game.

# TODO: add command /dungeon <arguments>
"""
explore
battle
etc.
"""


class Dungeon:
    """Explore the dungeon"""

    __slots__ = "bot"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def roll(self, ctx, max_roll: int = 6):
        """Rolls a dice."""i
        roll = random.randint(1, max_roll)
        await ctx.channel.send("Rolled " + str(roll))


def setup(bot):
    bot.add_cog(Dungeon(bot))

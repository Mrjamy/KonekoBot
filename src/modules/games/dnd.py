import discord
import random
from discord.ext import commands
import textwrap

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

    # TODO: update the /roll command to /roll <dices>d<max_roll>
    @commands.command(pass_context=True)
    async def roll(self, ctx, max_roll: int = 6, die: int = 1):
        """Rolls a dice."""

        embed = discord.Embed(title=f'{ctx.author} rolled {die} Dice - {max_roll}',
                              color=discord.Color.dark_purple())
        rolls = ''
        total = 0
        for x in range(0, die):
            roll = random.randint(1, max_roll)
            total += roll
            rolls += f'{str(roll)} '

        embed.add_field(name='Rolls', value=rolls, inline=False)
        embed.add_field(name='Total', value=total, inline=False)
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Dungeon(bot))

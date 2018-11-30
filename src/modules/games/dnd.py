import random
import discord
from discord.ext import commands


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
        """Rolls a die."""

        # The amount of dice need to be within 1 - 20
        if die not in range(1, 20 + 1):
            await ctx.channel.send(f'Do you really need that many dice?')
            return

        # Singular die.
        if die == 1:
            dice = "Die"
        # Plural dice.
        else:
            dice = "Dice"

        # max needs to be at least higher then 0
        if max_roll not in range(1, 20 + 1):
            await ctx.channel.send(f'*Sigh* no.')
            return

        embed = discord.Embed(title=f'{ctx.author} rolled {die} {dice} - {max_roll}',
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

import discord
from rolldice import *
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

    # TODO: update the /roll command to /roll <dice>d<sides>
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(pass_context=True)
    async def roll(self, ctx, *, die: str = 'd20'):
        """Rolls a die."""

        dicebag = DiceBag(die)

        result, explanation = dicebag.roll_dice()

        embed = discord.Embed(title=f'{ctx.author} rolled {die}',
                              color=discord.Color.dark_purple())

        embed.add_field(name='**Total**', value=result, inline=False)
        embed.add_field(name='**Rolled**', value=explanation, inline=False)
        await ctx.channel.send(embed=embed)

    @roll.error
    async def on_roll_error(self, ctx, error):
        """Roll error handler"""
        embed = discord.Embed(title=f'I don\'t think this is a valid dice roll :upside_down:',
                              color=discord.Color.red())
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Dungeon(bot))

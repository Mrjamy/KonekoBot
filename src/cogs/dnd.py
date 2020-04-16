# Builtins
import logging

# Pip
import discord
from rolldice import DiceBag
from discord.ext import commands

# Locals
from src.utils.user.nick_helper import Name


# TODO: add a dungeon/dnd based game.
# TODO: add command /dungeon <arguments>
"""
explore
battle
etc.
"""

module_logger = logging.getLogger('koneko.Dungeon')


class Dungeon(commands.Cog):
    """Explore the dungeon"""

    __slots__ = 'bot'

    def __init__(self, bot):
        self.bot = bot

    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
    async def roll(self, ctx, *, die: str = 'd20'):
        """Rolls a die with standard dice notations."""

        dicebag = DiceBag(die)

        result, explanation = dicebag.roll_dice()

        embed = discord.Embed(title=f'{Name.nick_parser(ctx.message.author)} rolled {die}',
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

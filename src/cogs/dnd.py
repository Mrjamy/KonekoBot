"""
Module related to DND

This is a wip and might become a project of it's own.
"""

# Builtins
import logging

# Pip
import discord
from discord.ext import commands
from rolldice import DiceBag

# Locals
from src.utils.general import DiscordEmbed, NameTransformer

# TODO: add a dungeon/dnd based game.
# TODO: add command /dungeon <arguments>

module_logger = logging.getLogger('koneko.Dungeon')


class Dungeon(commands.Cog):
    """Explore the dungeon"""

    __slots__ = 'bot',

    def __init__(self, bot):
        self.bot = bot

    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
    async def roll(self, ctx, *, die: str = 'd20') -> None:
        """Rolls a die with standard dice notations."""

        dice_bag = DiceBag(die)

        result, explanation = dice_bag.roll_dice()

        embed = discord.Embed(title=f'{NameTransformer(ctx.message.author)} rolled {die}',
                              color=discord.Color.dark_purple())

        embed.add_field(name='**Total**', value=result, inline=False)
        embed.add_field(name='**Rolled**', value=explanation, inline=False)
        await ctx.channel.send(embed=embed)

    @roll.error
    async def on_roll_error(self, ctx, _error) -> None:
        """Roll error handler"""
        await DiscordEmbed.error(ctx, title='I don\'t think this is a valid '
                                            'dice roll :upside_down:')


def setup(bot) -> None:
    """The setup function to add this cog to Koneko."""
    bot.add_cog(Dungeon(bot))

"""
Module containing games and related commands.
"""

# Builtins
import asyncio
import logging
import random

# Pip
from discord.ext import commands

# Locals
from src.utils.general import DiscordEmbed

module_logger = logging.getLogger('koneko.Games')


class Games(commands.Cog):
    """Some fun games."""

    __slots__ = ('bot',)

    def __init__(self, bot):
        self.bot = bot

    # pylint: disable=too-many-branches
    @commands.command()
    async def rps(self, ctx, choice: str = "") -> None:
        """Play a game of rock paper scissors."""
        options = {
            "r": 1,
            "p": 2,
            "s": 3
        }

        reverse_options = {
            1: "rock",
            2: "paper",
            3: "scissor"
        }

        # Getting the input inside <choice>
        if choice == "":
            m = await ctx.channel.send("Please choose from: rock, paper, scissors")

            def validate(m_):
                return m_.author == ctx.author and m_.channel == ctx.channel
            try:
                choice = await ctx.bot.wait_for('message', check=validate,
                                                timeout=60)
                choice = choice.content
            except asyncio.TimeoutError:
                await m.delete()
                return
        # only look at the 1st character of choice
        player = choice.lower()[0]
        if player in options:
            player_choice = options.get(player)
        elif player not in options.values():
            await DiscordEmbed.error(ctx, title='Please choose from: rock, '
                                                'paper, scissors')
            return

        # make the bot choose an option
        bot_choice_key = random.choice(list(options))
        bot_choice = options[bot_choice_key]

        # checking who won and sending the appropiate message
        res = ((player_choice - bot_choice) % 3)
        if res == 0:
            message = f"It is a tie! your {reverse_options[player_choice]} went even with my {reverse_options[bot_choice]}!"
            await DiscordEmbed.message(ctx, title=message)
        elif res == 1:
            message = f"You won! your {reverse_options[player_choice]} beat my {reverse_options[bot_choice]}!"
            await DiscordEmbed.confirm(ctx, title=message)
        else:
            message = f"You lost! your {reverse_options[player_choice]} lost to my {reverse_options[bot_choice]}!"
            await DiscordEmbed.error(ctx, title=message)


def setup(bot) -> None:
    """The setup function to add this cog to Koneko."""
    bot.add_cog(Games(bot))

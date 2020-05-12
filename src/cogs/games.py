"""
Module containing games and related commands.
"""

# Builtins
import asyncio
import logging
import random

# Pip
import discord
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
            "r": "rock",
            "p": "paper",
            "s": "scissors"
        }

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

        player = choice.lower()

        if player in options:
            player = options.get(player)
        elif player not in options.values():
            await DiscordEmbed.error(ctx, title='Please choose from: rock, '
                                                'paper, scissors')
            return

        bot = random.choice(list(options.values()))

        if player == bot:
            color = discord.Color.dark_grey()
            message = "Tie!"
        elif player == "rock":
            if bot == "paper":
                color = discord.Color.red()
                message = f"You lose! {bot} covers {player}"
            else:
                color = discord.Color.green()
                message = f"You win! {player} smashes {bot}"
        elif player == "paper":
            if bot == "Scissors":
                color = discord.Color.red()
                message = f"You lose! {bot} cut {player}"
            else:
                color = discord.Color.green()
                message = f"You win! {player} covers {bot}"
        elif player == "scissors":
            if bot == "rock":
                color = discord.Color.red()
                message = f"You lose! {bot} smashes {player}"
            else:
                color = discord.Color.green()
                message = f"You win! {player} cut {bot}"
        else:
            color = discord.Color.red()
            message = "Oops something went wrong"

        await DiscordEmbed.send(ctx, title=message, color=color)


def setup(bot) -> None:
    """The setup function to add this cog to Koneko."""
    bot.add_cog(Games(bot))

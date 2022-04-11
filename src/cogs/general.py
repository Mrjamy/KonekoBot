"""
Module containing general commands.

General in this sense is quite broad.
"""

# Builtins
import json
import logging

# Pip
import discord
from discord.ext import commands

# Locals
from src.utils.general import DiscordEmbed, ImageProvider, NameTransformer

module_logger = logging.getLogger('koneko.General')


class General(commands.Cog):
    """General commands."""

    __slots__ = 'bot',

    def __init__(self, bot):
        self.bot = bot

    # Command ping, listen to /ping
    @commands.command(aliases=["pong"])
    async def ping(self, ctx: commands.Context) -> None:
        """Get the latency of the bot."""
        # Get the latency of the bot
        latency: str = f"{str(round(self.bot.latency * 1000))} ms"
        # Send it to the user
        await ctx.channel.send(latency)

    @commands.command(aliases=["pat", "kiss", "slap", "lewd", "respect"])
    async def hug(self, ctx: commands.Context, users: commands.Greedy[discord.Member]) -> discord.Embed:
        """Interact with other users.

        Possible interactions are: pat, kiss, slap, lewd and respect"""
        url: str = str(ImageProvider(ctx.invoked_with))

        if len(users) == 0:
            users: list = [self.bot.user]
        mentions: str = ' '.join([f'{NameTransformer(user)}' for user in users])

        with open('src/cogs/utils/sentences.json') as f:
            data: dict = json.load(f)
            if any(u.id in [502913609458909194, 533653653362311188] for u in users):
                message: str = data[ctx.invoked_with]['koneko'].format(NameTransformer(ctx.message.author))
            else:
                if ctx.invoked_with == "respect":
                    message: str = data[ctx.invoked_with]['other'].format(mentions)
                else:
                    message: str = data[ctx.invoked_with]['other'].format(NameTransformer(ctx.message.author), mentions)

        return await DiscordEmbed.message(ctx, title=message, image=url)


async def setup(bot) -> None:
    """The setup function to add this cog to Koneko."""
    await bot.add_cog(General(bot))

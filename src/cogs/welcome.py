# Builtins
import logging

# Pip
from discord.ext import commands

# Locals
from KonekoBot import KonekoBot

module_logger = logging.getLogger('koneko.Welcome')


class Welcome(commands.Cog):
    """Class called when an user join."""

    __slots__ = 'bot'

    def __init__(self, bot):
        self.bot = bot

    # Function called after member joins.
    @KonekoBot.event
    async def on_member_join(self, member):
        """Welcome message"""
        guild = member.guild

        # TODO: allow for custom messages.
        if guild.system_channel is not None:
            await guild.system_channel.send(
                f'Welcome to the {member.guild.name} Discord server, {member.mention}, enjoy your stay!'
            )


def setup(bot):
    bot.add_cog(Welcome(bot))

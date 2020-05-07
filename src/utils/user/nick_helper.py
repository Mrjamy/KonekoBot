"""
Util module to display a discord.User's nickname if applicable.
"""

# Pip
import discord


class Name:
    """Class name."""
    @staticmethod
    def nick_parser(user: discord.User) -> str:
        """Shows the display name of a discord.User object."""
        return user.display_name

# Builtins
import logging
import os
import random

# Pip
import discord

module_logger = logging.getLogger('koneko.utils')


class Emoji:
    """Emoji provider class."""

    __slots__ = ('cash', )

    def __init__(self):
        """Assign all used emoji\'s."""
        self.cash = '<:cashmoney:699293408442974238>'


class ImageProvider:
    """Image provider class."""

    __slots__ = ('image', )

    def __init__(self, query):
        """Generate a random image."""
        path = os.path.join(os.path.dirname(__file__), '..')

        local = os.path.join(rf'{path}', 'core', 'images', query)

        remote = rf'https://raw.githubusercontent.com/mrjamy/KonekoBot/master/src/core/images/{query}'

        filename = random.choice([
            file for file in os.listdir(local)
            if os.path.isfile(os.path.join(local, file))
        ])

        self.image = rf'{remote}/{filename}'

    def __str__(self) -> str:
        """Provide an absolute link to an image in str format."""
        return self.image


class NameTransformer:
    """User to display name transformer."""

    __slots__ = ('user', )

    def __init__(self, user: discord.User):
        self.user = user

    def __str__(self) -> str:
        """Shows the display name of a discord.User object."""
        return self.user.display_name


class DiscordEmbed:
    """Class to send discord embedded messages."""

    purple = discord.Color.dark_purple()
    grey = discord.Color.dark_grey()
    red = discord.Color.red()
    green = discord.Color.green()

    @staticmethod
    async def message(ctx, msg: str, color: discord.Color = purple) -> None:
        """Send a message"""
        await DiscordEmbed.send(ctx, msg, color=color)

    @staticmethod
    async def confirm(ctx, msg: str, color: discord.Color = green) -> None:
        """Sends a confirming message"""
        await DiscordEmbed.send(ctx, msg, color=color)

    @staticmethod
    async def error(ctx, msg: str, color: discord.Color = red) -> None:
        """Sends an error message"""
        await DiscordEmbed.send(ctx, msg, color=color)

    @staticmethod
    async def send(ctx, title: str, color: discord.Color = grey) -> None:
        """Send error message in the corresponding channel
         Parameters
        ------------
        ctx: ? [required]
            Error context.
        title: str[required]
            embed title.
        color: discord.Color[required]
            Message color to indicate the type of message.
        description: str[optional]
            Optional embed description/body.
        """
        try:
            await ctx.channel.send(embed=discord.Embed(title=title, color=color))
        # Message could not be delivered.
        except (discord.Forbidden, discord.HTTPException):
            pass
        # Message could not be delivered for possibly fixable reasons.
        except Exception as exception:
            # Log the exception type for proper handling the next occurrence.
            module_logger.error(f"{type(exception)} - error delivering message")

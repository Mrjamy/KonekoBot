"""
Module containing General uncategorized utils.
"""

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
    red = discord.Color.red()
    green = discord.Color.green()

    @staticmethod
    async def message(ctx, parts=None, color: discord.Color = purple, **kwargs) -> None:
        """Send a message"""
        await DiscordEmbed.send(ctx, parts, color=color, **kwargs)

    @staticmethod
    async def confirm(ctx, parts=None, color: discord.Color = green, **kwargs) -> None:
        """Sends a confirming message"""
        await DiscordEmbed.send(ctx, parts, color=color, **kwargs)

    @staticmethod
    async def error(ctx, parts=None, color: discord.Color = red, **kwargs) -> None:
        """Sends an error message"""
        await DiscordEmbed.send(ctx, parts, color=color, **kwargs)

    @staticmethod
    async def send(ctx, parts=None, **kwargs) -> None:
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
        image = kwargs.pop('image', None)

        embed = discord.Embed(**kwargs)

        # Add extra fields to the embed.
        if parts:
            for part in parts:
                embed.add_field(inline=False, **part)
        if image:
            embed.set_image(url=image)

        try:
            await ctx.channel.send(embed=embed)
        # Message could not be delivered.
        except (discord.Forbidden, discord.HTTPException) as error:
            module_logger.error(f'{type(error)} - could not deliver message.')
            module_logger.error(error)

"""
Module containing General uncategorized utils.
"""

# Builtins
import logging
import os
import random

# Pip
import discord
from discord.ext import commands

module_logger = logging.getLogger('koneko.utils')


class Emoji:
    """Emoji provider class."""

    __slots__ = 'cash',

    def __init__(self):
        """Assign all used emoji\'s."""
        self.cash: str = '<:cashmoney:699293408442974238>'


class ImageProvider:
    """Image provider class."""

    __slots__ = 'image',

    def __init__(self, query):
        """Generate a random image."""
        path: str = os.path.join(os.path.dirname(__file__), '..')

        local: str = os.path.join(rf'{path}', 'core', 'images', query)
        remote: str = rf'https://raw.githubusercontent.com/mrjamy/KonekoBot/master/src/core/images/{query}'

        filename: str = random.choice([
            file for file in os.listdir(local)
            if os.path.isfile(os.path.join(local, file))
        ])

        self.image: str = rf'{remote}/{filename}'

    def __str__(self) -> str:
        """Provide an absolute link to an image in str format."""
        return self.image


class NameTransformer:
    """User to display name transformer."""

    __slots__ = 'user',

    def __init__(self, user: discord.User):
        self.user: discord.User = user

    def __str__(self) -> str:
        """Shows the display name of a discord.User object."""
        return self.user.display_name


class DiscordEmbed:
    """Class to send discord embedded messages."""

    purple: discord.Color = discord.Color.dark_purple()
    red: discord.Color = discord.Color.red()
    green: discord.Color = discord.Color.green()

    @staticmethod
    async def message(ctx: commands.Context, parts=None, inline: bool = False, color: discord.Color = purple, **kwargs) -> discord.Embed:
        """Send a message"""
        return await DiscordEmbed.send(ctx, parts, inline=inline, color=color, **kwargs)

    @staticmethod
    async def confirm(ctx: commands.Context, parts=None, inline: bool = False, color: discord.Color = green, **kwargs) -> discord.Embed:
        """Sends a confirming message"""
        return await DiscordEmbed.send(ctx, parts, inline=inline, color=color, **kwargs)

    @staticmethod
    async def error(ctx: commands.Context, parts=None, inline: bool = False, color: discord.Color = red, **kwargs) -> discord.Embed:
        """Sends an error message"""
        return await DiscordEmbed.send(ctx, parts, inline=inline, color=color, **kwargs)

    @staticmethod
    async def send(ctx: commands.Context, parts=None, **kwargs) -> discord.Embed:
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
        image: str = kwargs.pop('image', None)
        inline: bool = kwargs.pop('inline', False)
        embed: discord.Embed = discord.Embed(**kwargs)

        # Add extra fields to the embed.
        if parts:
            for part in parts:
                embed.add_field(inline=inline, **part)
        if image:
            embed.set_image(url=image)

        await ctx.channel.send(embed=embed)

        # return embedded message for test assertion.
        return embed

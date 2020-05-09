# Builtins
import logging

# Pip
import discord

module_logger = logging.getLogger('koneko.Message')


class DiscordEmbed:
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




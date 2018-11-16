import discord
from discord.ext import commands


class General:
    """Music related commands."""

    __slots__ = 'bot'

    def __init__(self, bot):
        self.bot = bot

    # Command hello, listen to /hello
    @commands.command(pass_context=True)
    async def hello(self, ctx):
        """Hello!"""
        message = f'Hello {ctx.author.mention}'
        await ctx.channel.send(message)

    # Command ping, listen to /ping
    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """Get the latency of the bot."""
        # Get the latency of the bot
        latency = str(round(self.bot.latency * 1000)) + " ms"
        # Send it to the user
        await ctx.channel.send(latency)

    # Command hug, listen to /hug
    @commands.command(aliasses=["pong"], pass_context=True)
    async def hug(self, ctx, user: discord.User=None):
        """Hug!"""
        # TODO: Exceptions need to be caught.
        message = f'*Hugs* {ctx.author.mention}'
        if user:
            message = f'*Hugs* {user.mention}'
        await ctx.channel.send(message)


def setup(bot):
    bot.add_cog(General(bot))

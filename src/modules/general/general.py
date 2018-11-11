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
        message = 'Hello {0.author.mention}'.format(ctx)
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
    async def hug(self, ctx):
        """Hug!"""
        # TODO: add support for passing a user as parameter.
        message = 'Hugs {0.author.mention}'.format(ctx)
        await ctx.channel.send(message)


def setup(bot):
    bot.add_cog(General(bot))

# TODO: add implementation of cleverbot

from discord.ext import commands


class CleverBot(commands.Cog):
    """Cleverbot session."""

    __slots__ = 'bot'

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=[])
    async def clever_bot(self, ctx):

        if ctx.invoked_subcommand is None:
            await ctx.channel.send("pass an action!")

    @clever_bot.command(name="start")
    async def start_session(self, ctx):
        """Command description."""

        await ctx.channel.send("initiating cleverbot session")


def setup(bot):
    bot.add_cog(CleverBot(bot))
import src.core.checks as check
from discord.ext import commands


class Utility:
    """Utility commands."""

    __slots__ = 'bot'

    def __init__(self, bot):
        self.bot = bot

    @check.is_owner()
    @commands.command(pass_context=True, hidden=True)
    async def shutdown(self, ctx):
        """Shuts the bot down."""

        await ctx.channel.send(f"Don't kill me!")


def setup(bot):
    bot.add_cog(Utility(bot))

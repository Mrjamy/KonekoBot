import discord
from discord.ext import commands

from src.core.checks import Checks


class Admin(commands.Cog):
    """Commands only for the bot owner"""
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)


    @commands.command(aliases=["watch", "listen"], pass_context=True)
    async def game(self, ctx, *, name: str = None):
        """Change koneko's presence, owner only"""

        activities = {
            'game': discord.Game(name=name),
            'listen': discord.Activity(type=discord.ActivityType.listening, name=name),
            'watch': discord.Activity(type=discord.ActivityType.watching, name=name)
        }

        activity = activities[ctx.invoked_with]

        await self.bot.change_presence(status=discord.Status.online, activity=activity)
        return

def setup(bot):
    bot.add_cog(Admin(bot))

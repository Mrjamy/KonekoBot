# Pip
import discord
from discord.ext import commands


class EventListener(commands.Cog):
    __slots__ = 'bot'

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """KonekoBot on_ready event."""
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{self.bot.settings.prefix}h for help"
            )
        )
        # Bot logged in.
        print(f'Logged in as {self.bot.user}')
        print(f'I am in {len(self.bot.guilds)} guilds.')

    @commands.Cog.listener()
    async def on_command(self, ctx):
        self.bot.command_count += 1


def setup(bot):
    bot.add_cog(EventListener(bot))

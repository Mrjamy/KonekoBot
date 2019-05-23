# Builtins
import json

# Pip
import discord
from discord.ext import commands

# Locals
from src.utils.random.image_provider import ImageProvider
from src.utils.user.nick_helper import Name


class General(commands.Cog):
    """General commands."""

    __slots__ = 'bot'

    def __init__(self, bot):
        self.bot = bot

    # Command ping, listen to /ping
    @commands.command(aliases=["pong"])
    async def ping(self, ctx):
        """Get the latency of the bot."""
        # Get the latency of the bot
        latency = str(round(self.bot.latency * 1000)) + " ms"
        # Send it to the user
        await ctx.channel.send(latency)

    @commands.command(aliases=["pat", "kiss", "slap", "lewd"])
    async def hug(self, ctx, users: commands.Greedy[discord.Member]):
        provider = ImageProvider()

        url = provider.image(query=ctx.invoked_with)
        if len(users) == 0:
            users = [self.bot.user]
        mentions = ' '.join([f'{Name.nick_parser(user)}' for user in users])

        with open('src/cogs/utils/sentences.json') as f:
            data = json.load(f)
            if any(u.id in [502913609458909194, 533653653362311188] for u in users):
                message = data[ctx.invoked_with]['koneko'].format(Name.nick_parser(ctx.message.author),)
            else:
                message = data[ctx.invoked_with]['other'].format(Name.nick_parser(ctx.message.author), mentions)

        embed = discord.Embed(title=message,
                              color=discord.Color.dark_purple())
        embed.set_image(url=url)

        await ctx.channel.send(embed=embed)

    # TODO: v1.1 add command /beer <user>


def setup(bot):
    bot.add_cog(General(bot))

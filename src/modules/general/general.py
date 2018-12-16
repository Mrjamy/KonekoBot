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
        """A simple greeting!"""
        # TODO: add more greet strings.
        message = f'Hello {ctx.author.mention}'
        await ctx.channel.send(message)

    # Command ping, listen to /ping
    @commands.command(aliases=["pong"], pass_context=True)
    async def ping(self, ctx):
        """Get the latency of the bot."""
        # Get the latency of the bot
        latency = str(round(self.bot.latency * 1000)) + " ms"
        # Send it to the user
        await ctx.channel.send(latency)

    # TODO: add param user = None for help mapping
    # Command hug, listen to /hug
    @commands.command(pass_context=True)
    async def hug(self, ctx):
        """Hug!"""
        if len(ctx.message.mentions) >= 1:
            mentions = ' '.join([f'{user.mention}' for user in ctx.message.mentions])
            message = f'*Hugs* {mentions}'
        else:
            message = f'*Hugs {ctx.author.mention}'
        await ctx.channel.send(message)

    @hug.error
    async def hug_error(self, ctx, *args):
        """hug error handler"""

        if ctx.message.channel.permissions_for(ctx.me).embed_links:
            embed = discord.Embed(title=f'I could not perform this task :sob:',
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send(f'I could not perform this task :sob:')

    # TODO: add param user = None for help mapping
    # Command pat, listen to /pat
    @commands.command(aliases=["headpat"], pass_context=True)
    async def pat(self, ctx):
        """Pat!"""

        if len(ctx.message.mentions) >= 1:
            mentions = ' '.join([f'{user.mention}' for user in ctx.message.mentions])
            message = f'*Gives {mentions} a pat on the head*'
        else:
            message = f'*Gives {ctx.author.mention} a pat on the head*'
        await ctx.channel.send(message)

    @pat.error
    async def pat_error(self, ctx, *args):
        """pat error handler"""

        if ctx.message.channel.permissions_for(ctx.me).embed_links:
            embed = discord.Embed(title=f'I could not perform this task :sob:',
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send(f'I could not perform this task :sob:')

    # TODO: add command /lewd
    # TODO: add command /kiss <user>
    # TODO: add command /slap <user>
    # TODO: add command /beer <user>


def setup(bot):
    bot.add_cog(General(bot))

import discord
from discord.ext import commands
from src.services.random.text_generator import TextGenerator
from src.services.random.image_generator import ImageGenerator


class General:
    """Music related commands."""

    __slots__ = 'bot'

    def __init__(self, bot):
        self.bot = bot

    # Command hello, listen to /hello
    @commands.command(pass_context=True)
    async def hello(self, ctx):
        """A simple greeting!"""

        r = TextGenerator().greet()

        message = f'{r} {ctx.author.mention}'
        await ctx.channel.send(message)

    # Command ping, listen to /ping
    @commands.command(aliases=["pong"], pass_context=True)
    async def ping(self, ctx):
        """Get the latency of the bot."""
        # Get the latency of the bot
        latency = str(round(self.bot.latency * 1000)) + " ms"
        # Send it to the user
        await ctx.channel.send(latency)

    # Command hug, listen to /hug
    @commands.command(pass_context=True)
    async def hug(self, ctx, user=None):
        """Hug!"""

        image = ImageGenerator().hug()

        if len(ctx.message.mentions) >= 1:
            mentions = ' '.join([f'{user.name}' for user in ctx.message.mentions])
            message = f'*Hugs {mentions}*'
        else:
            message = f'*Hugs {ctx.author.name}*'

        embed = discord.Embed(title=message,
                              color=discord.Color.dark_purple())
        embed.set_image(url=image)

        await ctx.channel.send(embed=embed)

    @hug.error
    async def hug_error(self, ctx, *args):
        """hug error handler"""

        if ctx.message.channel.permissions_for(ctx.me).embed_links:
            embed = discord.Embed(title=f'I could not perform this task :sob:',
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send(f'I could not perform this task :sob:')

    # Command pat, listen to /pat
    @commands.command(aliases=["headpat"], pass_context=True)
    async def pat(self, ctx, user=None):
        """Pat!"""

        image = ImageGenerator().pat()

        if len(ctx.message.mentions) >= 1:
            mentions = ' '.join([f'{user.name}' for user in ctx.message.mentions])
            message = f'*Gives {mentions} a pat on the head*'
        else:
            message = f'*Gives {ctx.author.name} a pat on the head*'

        embed = discord.Embed(title=message,
                              color=discord.Color.dark_purple())
        embed.set_image(url=image)

        await ctx.channel.send(embed=embed)

    # @pat.error
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

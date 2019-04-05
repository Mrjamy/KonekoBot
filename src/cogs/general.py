import discord
from discord.ext import commands
from src.helpers.random.text_generator import TextGenerator
from src.helpers.random.image_generator import ImageGenerator
from src.helpers.user.nick_helper import Name


class General(commands.Cog):
    """General commands."""

    __slots__ = 'bot'

    def __init__(self, bot):
        self.bot = bot

    # Command hello, listen to /hello
    @commands.command(aliases=[])
    async def hello(self, ctx):
        """A simple greeting!"""
        # Get a random greeting.

        r = TextGenerator('greet_phrases').to_str()

        message = f'{r} {Name.nick_parser(ctx.message.author)}'
        await ctx.channel.send(message)

    # Command ping, listen to /ping
    @commands.command(aliases=["pong"])
    async def ping(self, ctx):
        """Get the latency of the bot."""
        # Get the latency of the bot
        latency = str(round(self.bot.latency * 1000)) + " ms"
        # Send it to the user
        await ctx.channel.send(latency)

    # Command hug, listen to /hug
    @commands.command(aliases=[])
    async def hug(self, ctx):
        """Mention a user to hug them!"""
        # TODO: async
        image = ImageGenerator(tag='hug').to_image()

        # TODO: add catch for self mentions
        if len(ctx.message.mentions) >= 1:
            if any(u.id == 502913609458909194 for u in ctx.message.mentions):
                message = f'*Hugs {Name.nick_parser(ctx.message.author)} back :heart:*'
            else:
                mentions = ' '.join([f'{Name.nick_parser(user)}' for user in ctx.message.mentions])
                message = f'*{Name.nick_parser(ctx.message.author)} Hugs {mentions}*'
        else:
            message = f'*Hugs {Name.nick_parser(ctx.message.author)}*'
            image = r'https://raw.githubusercontent.com/jmuilwijk/KonekoBot/development/' \
                    r'src/core/images/lonely/selfhug.gif'

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
    @commands.command(aliases=["headpat"])
    async def pat(self, ctx):
        """Mention a user to pat them!"""
        # TODO: async
        image = ImageGenerator(tag='pat').to_image()

        # TODO: add catch for self mentions
        if len(ctx.message.mentions) >= 1:
            if any(u.id == 502913609458909194 for u in ctx.message.mentions):
                message = f'*:blush: pats {Name.nick_parser(ctx.message.author)}*'
            else:
                mentions = ' '.join([f'{Name.nick_parser(user)}' for user in ctx.message.mentions])
                message = f'*{Name.nick_parser(ctx.message.author)} Gives {mentions} a pat on the head*'
        else:
            message = f'*Gives {Name.nick_parser(ctx.message.author)} a pat on the head*'
            image = rf'https://raw.githubusercontent.com/jmuilwijk/KonekoBot/development/' \
                    rf'src/core/images/lonely/selfpat.gif'

        embed = discord.Embed(title=message,
                              color=discord.Color.dark_purple())
        embed.set_image(url=image)

        await ctx.channel.send(embed=embed)

    @pat.error
    async def pat_error(self, ctx, *args):
        """pat error handler"""
        # Throw a patception :sad_face:
        if ctx.message.channel.permissions_for(ctx.me).embed_links:
            embed = discord.Embed(title=f'I could not perform this task :sob:',
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send(f'I could not perform this task :sob:')

    # Command kiss, listen to /kiss
    @commands.command(aliases=[])
    async def kiss(self, ctx):
        """Mention a user to kiss them!"""
        # TODO: async
        image = ImageGenerator(tag='kiss').to_image()

        # TODO: add catch for self mentions
        if len(ctx.message.mentions) >= 1:
            if any(u.id == 502913609458909194 for u in ctx.message.mentions):
                message = f'*Kisses {Name.nick_parser(ctx.message.author)} back :heart:*'
            else:
                mentions = ' '.join([f'{Name.nick_parser(user)}' for user in ctx.message.mentions])
                message = f'*{Name.nick_parser(ctx.message.author)} Kisses {mentions}*'
        else:
            message = f'*Kisses {Name.nick_parser(ctx.message.author)}*'

        embed = discord.Embed(title=message,
                              color=discord.Color.dark_purple())
        embed.set_image(url=image)

        await ctx.channel.send(embed=embed)

    @kiss.error
    async def kiss_error(self, ctx, *args):
        """kiss error handler"""
        if ctx.message.channel.permissions_for(ctx.me).embed_links:
            embed = discord.Embed(title=f'I could not perform this task :sob:',
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send(f'I could not perform this task :sob:')

    # Command slap, listen to /slap
    @commands.command(aliases=[])
    async def slap(self, ctx):
        """Mention a user to slap them!"""
        # TODO: async
        image = ImageGenerator(tag='slap').to_image()

        # TODO: add catch for self mentions
        if len(ctx.message.mentions) >= 1:
            if any(u.id == 502913609458909194 for u in ctx.message.mentions):
                message = f'*Get\'s slightly angry.*'
                image = r'https://raw.githubusercontent.com/jmuilwijk/KonekoBot/development/' \
                        r'src/core/images/notwork.png'
            else:
                mentions = ' '.join([f'{Name.nick_parser(user)}' for user in ctx.message.mentions])
                message = f'*{Name.nick_parser(ctx.message.author)} Slaps {mentions}*'
        else:
            message = f'*Slaps {Name.nick_parser(ctx.message.author)}*'

        embed = discord.Embed(title=message,
                              color=discord.Color.dark_purple())
        embed.set_image(url=image)

        await ctx.channel.send(embed=embed)

    @slap.error
    async def slap_error(self, ctx, *args):
        """slap error handler"""
        if ctx.message.channel.permissions_for(ctx.me).embed_links:
            embed = discord.Embed(title=f'I could not perform this task :sob:',
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send(f'I could not perform this task :sob:')

    # TODO: add command /lewd
    # TODO: add command /beer <user>


def setup(bot):
    bot.add_cog(General(bot))

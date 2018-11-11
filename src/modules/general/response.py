from discord.ext import commands
from profanity import profanity
from src.modules.general.words import predefined


class Response:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def say(self, ctx, *message):
        profanity.load_words(predefined)
        message = " ".join(message)
        if profanity.contains_profanity(message.lower()):
            message = "I don't think i should be saying that."
        await ctx.channel.send(message)


def setup(bot):
    bot.add_cog(Response(bot))

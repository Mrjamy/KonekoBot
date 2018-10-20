from discord.ext import commands
from profanity import profanity
from modules.response.words import predefined


class Response:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *message):
        profanity.load_words(predefined)
        msg = " ".join(message)
        if profanity.contains_profanity(msg.lower()):
            msg = "I don't think i should be saying that."
        await ctx.channel.send(msg)


def setup(bot):
    bot.add_cog(Response(bot))

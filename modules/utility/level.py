# TODO: add table for xp.

# TODO: get user current xp.

# TODO: get last message send by user (time).

# TODO: add xp to retreived.

# TODO: store xp

# TODO: update last timestamp.

# TODO: add cards for display.

# TODO: Command - !xp (get user's card.)

# TODO: Command - !levels (get the server's scoreboard.)

from discord.ext import commands
import services.database.cursors.xp as xp


class Level:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def xp(self, ctx):
        """Get the user's level progress."""
        author = ctx.author.id
        guild = ctx.guild.id

        uxp = xp.XP.xp_by_user(author, guild)

        print(uxp)
        # if not user:
        #     user = ctx.author
        # card = "card here"
        msg = "Inprogress!"
        await ctx.channel.send(msg)


def setup(bot):
    bot.add_cog(Level(bot))

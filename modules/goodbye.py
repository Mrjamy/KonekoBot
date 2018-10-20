from core import bot as core


class Goodbye:
    def __init__(self, bot):
        self.bot = bot

    # Function called after member joins.
    @core.event
    async def on_member_remove(self, member):
        server = member.server.default_channel
        fmt = '{0.mention} has left/been kicked from the server.'
        await self.bot.send_message(server, fmt.format(member, member.server))


def setup(bot):
    bot.add_cog(Goodbye(bot))

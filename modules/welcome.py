from core import bot as core


class Welcome:
    def __init__(self, bot):
        self.bot = bot

    # Function called after member joins.
    @core.event
    async def on_member_join(self, member):
        server = member.server.default_channel
        fmt = 'Welcome to the {1.name} Discord server, {0.mention}, enjoy your stay.'
        await self.bot.send_message(server, fmt.format(member, member.server))


def setup(bot):
    bot.add_cog(Welcome(bot))

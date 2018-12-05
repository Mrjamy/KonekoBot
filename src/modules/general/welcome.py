from KonekoBot import KonekoBot


class Welcome:
    def __init__(self, bot):
        self.bot = bot

    # TODO: needs repair.
    # Function called after member joins.
    @KonekoBot.event
    async def on_member_join(self, member):
        guild = member.guild
        message = 'Welcome to the {1.name} Discord server, {0.mention}, enjoy your stay.'
        if guild.system_channel is not None:
            await guild.system_channel.send(message.format(member, member.guild))


def setup(bot):
    bot.add_cog(Welcome(bot))

from KonekoBot import KonekoBot


class Goodbye:
    def __init__(self, bot):
        self.bot = bot

    # TODO: needs repair.
    # Function called after member joins.
    @KonekoBot.event
    async def on_member_remove(self, member):
        guild = member.guild
        message = 'Goodbye {0.mention}'
        if guild.system_channel is not None:
            await guild.system_channel.send(message.format(member))


def setup(bot):
    bot.add_cog(Goodbye(bot))

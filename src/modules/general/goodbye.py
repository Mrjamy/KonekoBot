from KonekoBot import KonekoBot


class Goodbye:
    def __init__(self, bot):
        self.bot = bot

    # Function called after member joins.
    @KonekoBot.event
    async def on_member_remove(self, member):
        """Goodbye message :("""
        guild = member.guild

        # TODO: allow for custom messages.
        message = 'Goodbye {0.mention}'
        if guild.system_channel is not None:
            await guild.system_channel.send(message.format(member))


def setup(bot):
    bot.add_cog(Goodbye(bot))

from KonekoBot import KonekoBot


class Goodbye:
    """Class called when an user leaves."""

    __slots__ = 'bot'

    def __init__(self, bot):
        self.bot = bot

    # Function called after member joins.
    @KonekoBot.event
    async def on_member_remove(self, member):
        """Goodbye message :("""
        guild = member.guild

        # TODO: allow for custom messages.
        if guild.system_channel is not None:
            await guild.system_channel.send(f'Goodbye {member.mention}')


def setup(bot):
    bot.add_cog(Goodbye(bot))

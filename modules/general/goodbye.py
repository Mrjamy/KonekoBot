from KonekoBot import bot as koneko


class Goodbye:
    def __init__(self, bot):
        self.bot = bot

    # Function called after member joins.
    @koneko.event
    async def on_member_remove(self, member):
        guild = member.guild
        msg = 'Goodbye {0.mention}'
        if guild.system_channel is not None:
            await guild.system_channel.send(msg.format(member))


def setup(bot):
    bot.add_cog(Goodbye(bot))

import discord


class Name:
    @staticmethod
    def nick_parser(user: discord.User) -> str:
        return user.display_name

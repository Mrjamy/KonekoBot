# Pip
import discord


class Name(object):
    @staticmethod
    def nick_parser(user: discord.User) -> str:
        return user.display_name

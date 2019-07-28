# Pip
from discord.ext import commands


class NoPermission(commands.CommandError):
    pass


class NotEnoughBalance(Exception):
    pass

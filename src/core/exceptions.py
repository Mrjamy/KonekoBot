# Pip
from discord.ext import commands


class DevOnly(commands.CommandError):
    pass


class DjOnly(commands.CommandError):
    pass


class NoPermission(commands.CommandError):
    pass


class NotInVoiceChannel(commands.CommandError):
    pass


class NotEnoughBalance(Exception):
    pass

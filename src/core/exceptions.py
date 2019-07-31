# Pip
from discord.ext import commands


class NoPermission(commands.CommandError):
    """No permission for the given action."""
    pass


class NotEnoughBalance(Exception):
    """Not enough balance for the command."""
    pass

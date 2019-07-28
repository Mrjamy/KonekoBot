# Pip
from discord.ext import commands

# Locals
from src.core.config import Settings
from src.core.exceptions import NoPermission

settings = Settings()


class Checks:
    @staticmethod
    def has_permissions(**permissions):
        async def predicate(ctx):
            if all(getattr(ctx.channel.permissions_for(ctx.author), name, None) == value for name, value in
                    permissions.items()):
                return True
            else:
                raise NoPermission
        return commands.check(predicate)

# Pip
import discord
from discord.ext import commands

# Locals
from src.core.config import Settings
from src.core.exceptions import (
    DevOnly,
    NoPermission,
    DjOnly,
    NotInVoiceChannel
)

settings = Settings()


class Checks:
    @staticmethod
    def is_dev():
        async def predicate(ctx):
            if ctx.author.id in settings.dev_ids:
                return True
            else:
                raise DevOnly
        return commands.check(predicate)

    @staticmethod
    def has_permissions(**permissions):
        async def predicate(ctx):
            if all(getattr(ctx.channel.permissions_for(ctx.author), name, None) == value for name, value in
                    permissions.items()):
                return True
            else:
                raise NoPermission
        return commands.check(predicate)

    @staticmethod
    def is_dj():
        async def predicate(ctx):
            if "dj" in [role.name.lower() for role in ctx.author.roles]:
                return True
            elif commands.is_owner():
                return True
            else:
                # TODO: v1.1 Add option to set the DJ role to any existing role.
                # TODO: v1.1 Store this setting in a database.
                # ctx.send("This command requires you to have the role DJ")
                raise DjOnly
        return commands.check(predicate)

    @staticmethod
    def is_connected_voice():
        async def predicate(ctx):
            if hasattr(ctx.author.voice, 'channel'):
                return True
            else:
                raise NotInVoiceChannel

        return commands.check(predicate)

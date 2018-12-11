import discord
from discord.ext import commands
from src.core.config import Settings

settings = Settings()


class OwnerOnly(commands.CommandError):
    pass


class DevOnly(commands.CommandError):
    pass


class DjOnly(commands.CommandError):
    pass


class NotNsfwChannel(commands.CommandError):
    pass


class NoPermission(commands.CommandError):
    pass


def is_owner():
    def predicate(ctx):
        if ctx.author.id == settings.owner_id:
            return True
        else:
            raise OwnerOnly
    return commands.check(predicate)


def is_dev():
    def predicate(ctx):
        if ctx.author.id in settings.dev_ids:
            return True
        elif is_owner():
            return True
        else:
            raise DevOnly
    return commands.check(predicate)


def is_nsfw_channel():
    def predicate(ctx):
        if not isinstance(ctx.channel, discord.DMChannel) and ctx.channel.is_nsfw():
            return True
        else:
            raise NotNsfwChannel
    return commands.check(predicate)


def has_permissions(**permissions):
    def predicate(ctx):
        if all(getattr(ctx.channel.permissions_for(ctx.author), name, None) == value for name, value in
                permissions.items()):
            return True
        else:
            raise NoPermission
    return commands.check(predicate)


def is_dj():
    def predicate(ctx):
        if "dj" in [role.name.lower() for role in ctx.author.roles]:
            return True
        elif is_owner():
            return True
        else:
            # TODO: Add option to set the DJ role to any existing role.
            # TODO: Store this setting in a database.
            ctx.send("This command requires you to have the role DJ")
            raise DjOnly(ctx)
    return commands.check(predicate)


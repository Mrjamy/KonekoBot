import discord
from discord.ext import commands
import src.core.config as config


class OwnerOnly(commands.CommandError):
    pass


class DevOnly(commands.CommandError):
    pass


class NotNsfwChannel(commands.CommandError):
    pass


class NoPermission(commands.CommandError):
    pass


def is_owner():
    def predicate(ctx):
        if ctx.author.id == config.owner_id:
            return True
        else:
            raise OwnerOnly
    return commands.check(predicate)


def is_dev():
    def predicate(ctx):
        if ctx.author.id in config.dev_ids or ctx.author.id == config.owner_id:
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
            print("user tried invoking w/o perms")
            raise NoPermission
    return commands.check(predicate)

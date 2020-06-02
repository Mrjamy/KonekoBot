"""
Module containing mocked objects of discord.py
"""

# Builtin
import collections
import itertools
import unittest.mock
from asyncio import AbstractEventLoop
from aiohttp import ClientSession

# pip
import discord
from discord.ext.commands import Context

# Locals
from KonekoBot import Koneko


class CustomMock:
    """Class to assign some commonly used functionality."""

    spec_set = None
    discord_id = itertools.count(0)

    def __init__(self, **kwargs):
        name = kwargs.pop('name', None)
        super().__init__(spec_set=self.spec_set, **kwargs)

        if name:
            self.name = name


# Create a `discord.Guild` instance
guild_data = {
    'id': 1,
    'name': 'guild',
    'region': 'Europe',
    'verification_level': 2,
    'default_notications': 1,
    'afk_timeout': 100,
    'icon': "icon.png",
    'banner': 'banner.png',
    'mfa_level': 1,
    'splash': 'splash.png',
    'system_channel_id': 657571218324586499,
    'description': 'description',
    'max_presences': 10_000,
    'max_members': 100_000,
    'preferred_locale': 'UTC',
    'owner_id': 1,
    'afk_channel_id': 657571218324586499,
}
guild_instance = discord.Guild(data=guild_data, state=unittest.mock.MagicMock())


class MockGuild(unittest.mock.Mock):
    """A mock subclass to mock `discord.Guild` objects."""
    spec_set = guild_instance


# Create a `discord.Role` instance
role_data = {'name': 'role', 'display_name': 'user', 'id': 1}
role_instance = discord.Role(guild=guild_instance, state=unittest.mock.MagicMock(), data=role_data)


class MockRole(CustomMock, unittest.mock.Mock):
    """A mock subclass to mock `discord.Role` objects."""
    spec_set = role_instance

    def __init__(self, **kwargs) -> None:
        default_kwargs = {
            'id': next(self.discord_id),
            'name': 'role',
            'position': 1,
            'colour': discord.Colour(0xdeadbf),
            'permissions': discord.Permissions(),
        }
        super().__init__(**collections.ChainMap(kwargs, default_kwargs))


# Create a `discord.Member` instance
member_data = {'user': 'mrjamy', 'roles': [1]}
member_instance = discord.Member(data=member_data, guild=guild_instance,
                                 state=unittest.mock.MagicMock())


class MockMember(CustomMock, unittest.mock.Mock):
    """A mock subclass to mock `discord.Member` objects."""

    def __init__(self, roles=None, **kwargs) -> None:
        default_kwargs = {'name': 'member', 'display_name': 'user',
                          'id': next(self.discord_id), 'bot': False}
        super().__init__(**collections.ChainMap(kwargs, default_kwargs))

        self.roles = [MockRole(name="@everyone", position=1, id=0)]
        if roles:
            self.roles.extend(roles)

        if 'mention' not in kwargs:
            self.mention = f"@{self.name}"

    def __str__(self) -> str:
        return self.name

    spec_set = member_instance


# Create a User instance to get a realistic Mock of `discord.User`
user_instance = discord.User(data=unittest.mock.MagicMock(), state=unittest.mock.MagicMock())


class MockUser(CustomMock, unittest.mock.Mock):
    """A mock subclass to mock `discord.User` objects."""
    spec_set = user_instance

    def __init__(self, **kwargs) -> None:
        default_kwargs = {'name': 'user', 'display_name': 'user',
                          'id': next(self.discord_id), 'bot': False}
        super().__init__(**collections.ChainMap(kwargs, default_kwargs))

        if 'mention' not in kwargs:
            self.mention = f"@{self.name}"

    def __str__(self) -> str:
        return self.name


def _get_mock_loop() -> unittest.mock.Mock:
    """Return a mocked asyncio.AbstractEventLoop."""
    loop = unittest.mock.create_autospec(spec=AbstractEventLoop, spec_set=True)

    loop.create_task.side_effect = lambda coroutine: coroutine.close()

    return loop


class MockBot(unittest.mock.MagicMock):
    """A mock subclass to mock `discord.ext.commands.AutoShardedBot` objects."""
    spec_set = Koneko(command_prefix=unittest.mock.MagicMock(),
                      loop=_get_mock_loop())

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.loop = _get_mock_loop()
        self.http_session = unittest.mock.create_autospec(spec=ClientSession,
                                                          spec_set=True)


# Create a `discord.TextChannel` instance
channel_data = {
    'id': 1,
    'type': 'TextChannel',
    'name': 'channel',
    'parent_id': 657571218324586497,
    'topic': 'topic',
    'position': 1,
    'nsfw': False,
    'last_message_id': 1,
}
channel_instance = discord.TextChannel(state=unittest.mock.MagicMock(),
                                       guild=unittest.mock.MagicMock(),
                                       data=channel_data)


class MockTextChannel(unittest.mock.AsyncMock):
    """A mock subclass to mock `discord.TextChannel` objects."""
    spec_set = channel_instance


# Create a `discord.ext.commands.Context` instance
context_instance = Context(message=unittest.mock.MagicMock(),
                           prefix=unittest.mock.MagicMock())


class MockContext(unittest.mock.Mock):
    """A mock subclass to mock `discord.ext.commands.Context` objects."""
    spec_set = context_instance

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.bot = kwargs.get('bot', MockBot())
        self.guild = kwargs.get('guild', MockGuild())
        self.author = kwargs.get('author', MockMember())
        self.channel = kwargs.get('channel', MockTextChannel())

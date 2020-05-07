"""
Prefix repository.
"""

# Builtins
from typing import List

# Pip
import configparser
import logging

# Locals
from src.utils.database.models.prefix import Prefix

config = configparser.ConfigParser()
config.read('config.ini')

module_logger = logging.getLogger('koneko.PrefixRepository')


class PrefixRepository:
    """Prefix repository

    Contains methods to work with the Prefix model."""

    @staticmethod
    async def get(guild_id: int) -> List[Prefix]:
        """ Return all prefixes of a guild.
        Parameters
        ------------
        guild_id: int [required]
            The guild to fetch the prefixes for.
        """
        prefix = await Prefix.filter(
            guild=guild_id
        ).first()
        _prefix = []
        if not prefix:
            _prefix.append(config.get('Koneko', 'prefix'))
        else:
            _prefix.append(str(prefix))
        return _prefix

    @staticmethod
    async def insert(guild_id: int, prefix: str) -> List[Prefix]:
        """ Set a guild specific prefix
        Parameters
        ------------
        guild_id: int [required]
            The guild the prefix is related to.
        prefix: str [required]
            one ore more prefixes to add to a guild.
        """
        exist = await Prefix.filter(
            guild=guild_id
        ).first()
        if not exist:
            await Prefix.create(
                guild=guild_id,
                prefix=prefix
            )
        else:
            await Prefix.filter(
                guild=guild_id
            ).first().update(
                prefix=prefix
            )
        return await PrefixRepository.get(guild_id)

    @staticmethod
    async def delete(guild_id: int) -> bool:
        """ Delete a prefix for a guild
        Parameters
        ------------
        guild_id: int [required]
            The guild the prefix is related to.
        """
        prefix = await Prefix.filter(
            guild=guild_id
        ).first()
        if prefix:
            await prefix.delete()
            return True

        return False

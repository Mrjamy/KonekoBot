# Pip
import configparser
import logging

# Locals
from src.utils.database.models.prefix import Prefix

config = configparser.ConfigParser()
config.read('config.ini')

module_logger = logging.getLogger('koneko.PrefixRepository')

class PrefixRepository:
    async def get(self, guild_id: int) -> Prefix:
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

    async def insert(self, guild_id: int, prefix: str) -> Prefix:
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
        return await self.get(guild_id)

    async def delete(self, guild_id: int) -> bool:
        """ Delete a prefix for a guild
        Parameters
        ------------
        guild_id: int [required]
            The guild the prefix is related to.
        prefix: str [required]
            The prefix to delete.
        """
        prefix = await Prefix.filter(
            guild=guild_id
        ).first()
        if prefix:
            await prefix.delete()
            return True
        else:
            return False

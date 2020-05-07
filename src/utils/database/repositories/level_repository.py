# Builtins
import logging
import random
from datetime import datetime
from typing import List

# Locals
from src.utils.database.models.level import Level

module_logger = logging.getLogger('koneko.LevelRepository')


class LevelRepository(object):
    @staticmethod
    async def get(user_id: int, guild_id: int) -> Level:
        """ Searches the database for a specific user, if not found one will be
        created.
        Parameters
        ------------
        user_id: int [Required]
            The user's discord snowflake.
        guild_id: int [required]
            The guild the user is related to.
        """
        level = await Level.filter(
            snowflake=user_id,
            guild=guild_id
        ).first()

        if level is None:
            level = await LevelRepository.insert(user_id, guild_id)
        return level

    @staticmethod
    async def get_all(guild_id: int, offset: int = 0) -> List[Level]:
        """ Searches the database for the top 10 users based on level. the
        parameter offset can be used to pick a custom starting point.
        Parameters
        ------------
        guild_id: int [required]
            The guild that will be filtered.
        offset: int [optional]
            Optional custom starting point for the scoreboard.
        """
        return await Level.filter(guild=guild_id) \
            .order_by('-experience') \
            .limit(10) \
            .offset(offset) \
            .all()

    @staticmethod
    async def add_xp(user_id: int, guild_id: int) -> Level:
        """ Adds a random amount of experience to the user betweem 5 and 10.
        Parameters
        ------------
        user_id: int [Required]
            The user's discord snowflake.
        guild_id: int [required]
            The guild the user is related to.
        """
        def _cooldown():
            return (datetime.now() - level.last_message).total_seconds() < 30

        level = await LevelRepository.get(user_id, guild_id)

        if not _cooldown():
            xp = level.experience + random.randint(5, 10)
            await Level.filter(
                snowflake=user_id,
                guild=guild_id
            ).first().update(
                experience=xp,
                last_message=datetime.now()
            )
            # Method .update() returns a NoneType so we need to aquire a new
            # copy of the level object
            level = await LevelRepository.get(user_id, guild_id)

        return level

    @staticmethod
    async def insert(user_id: int, guild_id: int) -> Level:
        """ Insert a user to the database
        Parameters
        ------------
        user_id: int [Required]
            The user's discord snowflake.
        guild_id: int [required]
            The guild the user is related to.
        """
        return await Level.create(
            snowflake=user_id,
            guild=guild_id,
            experience=0,
            level=0
        )

    @staticmethod
    async def levelup_check(user_id: int, guild_id: int) -> bool:
        """ Check if the target user has passed the required amount to level up.
        Parameters
        ------------
        user_id: int [Required]
            The user's discord snowflake.
        guild_id: int [required]
            The guild the user is related to.
        """
        level = await LevelRepository.get(user_id, guild_id)

        experience = level.experience
        lvl_start = level.level
        lvl_end = int(experience ** (1 / 4))

        up = False
        if lvl_start < lvl_end:
            await Level.filter(
                snowflake=user_id,
                guild=guild_id
            ).first().update(
                level=lvl_end
            )
            up = True

        return up

"""
Level repository.
"""

# Builtins
import json
import logging
import random
from datetime import datetime
from time import time
from typing import List

# Pip
import discord

# Locals
from src.utils.database.postgress.models.level import Level

module_logger = logging.getLogger('koneko.LevelRepository')


class LevelRepository:
    """Level repository

    Contains methods to work with the Level model."""

    async def get(self, user_id: int, guild_id: int) -> Level:
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
            level = await self.insert(user_id, guild_id)
        return level

    async def get_json(self, user: discord.User, guild_id: int):
        with open('src/utils/database/json/levels.json') as f:
            data = json.load(f)

            try:
                user = data[guild_id][user.id]
                module_logger.debug(user)
                return user
            except KeyError:
                pass

            module_logger.debug(data)


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

    async def add_xp(self, user_id: int, guild_id: int) -> Level:
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

        level = await self.get(user_id, guild_id)

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
            level = await self.get(user_id, guild_id)

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

    async def json_insert(self, user: discord.User, guild_id: str):
        with open('src/utils/database/json/levels.json', 'r') as f:
            data = json.load(f)

        try:
            # Check if the guild is already known.
            if guild_id not in data:
                data[guild_id] = {}
            if user.id not in data[guild_id]:
                data[guild_id][user.id] = {
                    "name": "test",
                    "experience": 0,
                    "level": 1,
                    "last_message": int(time())
                }
            else:
                module_logger.debug(user.id not in data[guild_id])
        except KeyError:
            return False

        with open('src/utils/database/json/levels.json', 'w') as f:
            json.dump(data, f, indent=4, sort_keys=True)



    async def levelup_check(self, user_id: int, guild_id: int) -> bool:
        """ Check if the target user has passed the required amount to level up.
        Parameters
        ------------
        user_id: int [Required]
            The user's discord snowflake.
        guild_id: int [required]
            The guild the user is related to.
        """
        level = await self.get(user_id, guild_id)

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

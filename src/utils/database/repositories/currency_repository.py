"""
Currency repository.
"""

# builtins
import logging
from typing import List

# Pip
import json
import jsonpickle

# Locals
from src.core.exceptions import NotEnoughBalance
from src.utils.database.models.currency import Currency

module_logger = logging.getLogger('koneko.CurrencyRepository')


class CurrencyRepository:
    """Currency repository

    Contains methods to work with the Currency model."""

    @staticmethod
    async def get(user_id: int, guild_id: int) -> Currency:
        """ Searches the database for a specific user, if not found one will be
        created.
        Parameters
        ------------
        user_id: int [Required]
            The user's discord snowflake.
        guild_id: int [required]
            The guild the user is related to.
        """
        currency = await Currency.filter(
            snowflake=user_id,
            guild=guild_id
        ).first()

        if currency is None:
            currency = await CurrencyRepository.insert(user_id, guild_id)
        return currency

    @staticmethod
    async def get_all(guild_id: int, offset: int = 0) -> List[Currency]:
        """ Searches the database for the top 10 users based on currency. the
        parameter offset can be used to pick a custom starting point.
        Parameters
        ------------
        guild_id: int [required]
            The guild that will be filtered.
        offset: int [optional]
            Optional custom starting point for the scoreboard.
        """
        return await Currency.filter(guild=guild_id) \
            .order_by('-amount') \
            .limit(10) \
            .offset(offset) \
            .all()

    @staticmethod
    async def update(user_id: int, guild_id: int, amount: int = +100) -> Currency:
        """ updates an user's balance by amount, positve or negative.
        ------------
        user_id: int [Required]
            The user's discord snowflake.
        guild_id: int [required]
            The guild the user is related to.
        """
        async def check():
            balance = await CurrencyRepository.get(user_id, guild_id)
            if not bool(balance.amount >= amount):
                raise NotEnoughBalance

        # Check if a user has the funds to proceed
        if amount < 0:
            await check()

        currency = await CurrencyRepository.get(user_id, guild_id)

        bal = currency.amount + amount
        await Currency.filter(
            snowflake=user_id,
            guild=guild_id
        ).first().update(
            amount=bal,
        )
        # Method .update() returns a NoneType so we need to aquire a new
        # copy of the currency object
        return await CurrencyRepository.get(user_id, guild_id)

    @staticmethod
    async def insert(user_id: int, guild_id: int) -> Currency:
        """ Insert a user to the database
        Parameters
        ------------
        user_id: int [Required]
            The user's discord snowflake.
        guild_id: int [required]
            The guild the user is related to.
        """
        return await Currency.create(
            snowflake=user_id,
            guild=guild_id,
            amount=0
        )

    @staticmethod
    async def export_db(file: str = 'currency_db.json') -> None:
        """ Exports currency table to a json file
        Parameters
        ------------
        file: str [optional]
            output file name.
        """
        data = await Currency.all().order_by('-amount')

        with open(f'backups/{file}', 'w') as f:
            encoded = jsonpickle.encode(data)
            json.dump(encoded, f, indent=4, sort_keys=True)

    @staticmethod
    async def import_db(file: str = 'currency_db.json') -> None:
        """ Imports to the currency table from a json file
        Parameters
        ------------
        file: str [optional]
            input file name.
        """
        with open(f'backups/{file}') as f:
            data = jsonpickle.decode(f)

            await Currency.bulk_create(data)

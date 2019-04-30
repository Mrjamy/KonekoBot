# Locals
from src.core.exceptions import NotEnoughBalance
from src.utils.database.models.currency import Currency


class CurrencyRepository:
    async def get(self, user_id: int, guild_id: int) -> Currency:
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
            currency = await self.insert(user_id, guild_id)
        return currency

    async def get_all(self, guild_id: int, offset: int = 0) -> list:
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

    async def update(self, user_id: int, guild_id: int, amount: int = +100) -> Currency:
        """ updates an user's balance by amount, positve or negative.
        ------------
        user_id: int [Required]
            The user's discord snowflake.
        guild_id: int [required]
            The guild the user is related to.
        """
        async def check():
            balance = await self.get(user_id, guild_id)
            if not bool(balance.amount >= amount):
                raise NotEnoughBalance

        # Check if a user has the funds to proceed
        if amount < 0:
            await check()

        currency = await self.get(user_id, guild_id)

        bal = currency.amount + amount
        await Currency.filter(
            snowflake=user_id,
            guild=guild_id
        ).first().update(
            amount=bal,
        )
        # Method .update() returns a NoneType so we need to aquire a new
        # copy of the currency object
        return await self.get(user_id, guild_id)

    async def insert(self, user_id: int, guild_id: int) -> Currency:
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

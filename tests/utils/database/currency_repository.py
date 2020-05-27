"""
Currency repository tests.
"""

# Builtins
import unittest

# Pip
from tortoise import generate_config, Tortoise

# Locals
from src.utils.database.repositories.currency_repository import \
    CurrencyRepository


# pylint: disable=no-member
class TestCurrencyRepository(unittest.IsolatedAsyncioTestCase):
    """Test Currency repository.

    Tests for the currency repository."""

    __slots__ = ('connections', 'currency_repository')

    def __init__(self):
        super().__init__()

        self._connections = {}
        self.currency_repository = None

    async def asyncSetUp(self) -> None:
        """Set up function for the tests."""
        config = generate_config(db_url="sqlite://:memory:",
                                 app_modules={'models': [
                                     "src.utils.database.models.level",
                                     "src.utils.database.models.currency",
                                     "src.utils.database.models.prefix"
                                 ]})
        await Tortoise.init(config, _create_db=True)
        await Tortoise.generate_schemas(safe=False)

        self._connections = Tortoise._connections.copy()
        self.currency_repository = CurrencyRepository()

    async def asyncTearDown(self) -> None:
        """tear down function for the tests."""
        Tortoise._connections = self._connections.copy()
        await Tortoise._drop_databases()

        Tortoise.apps = {}
        Tortoise._connections = {}
        Tortoise._inited = False

    async def create_user(self) -> None:
        """Tests creating a new user in the database."""
        user = await self.currency_repository.insert(1, 1)

        self.assertIsNotNone(user)

    async def mutate_balance(self) -> None:
        """Tests mutating an user's balance."""
        await self.currency_repository.insert(2, 1)
        user = await self.currency_repository.update(2, 1, 100)

        self.assertEqual(user.amount, 100)


if __name__ == '__main__':
    unittest.main()

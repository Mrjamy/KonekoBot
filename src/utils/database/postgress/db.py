"""
Simple module to init a database connection using Tortoise-orm.
"""

# Pip
from tortoise import Tortoise


async def run() -> None:
    """Setup Tortoise-orm."""
    await Tortoise.init(config_file='src/utils/database/config.json')
    await Tortoise.generate_schemas()

# Builtins
import asyncio

# Pip
from tortoise import Tortoise


async def run():
    await Tortoise.init(config_file='src/utils/database/config.json')
    await Tortoise.generate_schemas()

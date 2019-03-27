import asyncio

from tortoise import Tortoise

async def run():
    await Tortoise.init(config_file='src/helpers/database/config.json')
    await Tortoise.generate_schemas()

# Pip
from tortoise import Tortoise


async def run() -> None:
    await Tortoise.init(config_file='src/utils/database/config.json')
    await Tortoise.generate_schemas()

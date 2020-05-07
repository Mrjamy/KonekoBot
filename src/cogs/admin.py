# Builtins
import json
import logging

# Pip
import discord
from discord.ext import commands
from src.utils.database.repositories.currency_repository import \
    CurrencyRepository

module_logger = logging.getLogger('koneko.Admin')


class Admin(commands.Cog):
    """Commands only for the bot owner"""

    __slots__ = 'bot', 'currency_repository'

    def __init__(self, bot):
        self.bot = bot
        self.currency_repository = CurrencyRepository()

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.command(aliases=["watch", "listen"], hidden=True)
    async def game(self, ctx, *, name: str = None):
        """Change koneko's presence, owner only"""

        activities = {
            'game': discord.Game(name=name),
            'listen': discord.Activity(type=discord.ActivityType.listening, name=name),
            'watch': discord.Activity(type=discord.ActivityType.watching, name=name)
            # TODO: allow for custom a status
        }

        activity = activities[ctx.invoked_with]

        await self.bot.change_presence(status=discord.Status.online, activity=activity)

    # noinspection PyUnusedLocal
    @commands.command(aliases=["export"], hidden=True)
    async def export_db(self, ctx):
        await self.currency_repository.export_db()

    # noinspection PyUnusedLocal
    @commands.command(aliases=["import"], hidden=True)
    async def import_db(self, ctx):
        await self.currency_repository.import_db()

    @commands.group(hidden=True)
    async def sentence(self, ctx):
        if ctx.invoked_subcommand is None:
            with open('src/cogs/utils/sentences.json') as f:
                data = json.load(f)
                return await ctx.channel.send(f'```json\n {json.dumps(data, indent=4, sort_keys=True)}```')

    @sentence.command()
    async def get(self, ctx, command: str, string: str):
        with open('src/cogs/utils/sentences.json') as f:
            data = json.load(f)
            try:
                response = data[command][string]
                await ctx.channel.send(f"{command}.{string} is `{response}`")
            except KeyError:
                return await ctx.channel.send(F"Could not find {command}.{string}")

    @get.error
    async def get_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Some parameters seem missing :thinking:')
        else:
            raise error

    @sentence.command()
    async def update(self, ctx, command: str, string: str, *, new: str):
        # Open file in read mode.
        with open('src/cogs/utils/sentences.json', 'r') as f:
            data = json.load(f)

        # Try updating the key.
        try:
            data[command][string] = new
        except KeyError:
            return await ctx.channel.send(F"Could not find {command}.{string}")

        # Write the modified json object back to the file.
        with open('src/cogs/utils/sentences.json', 'w') as f:
            json.dump(data, f, indent=4, sort_keys=True)

    @update.error
    async def update_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Some parameters seem missing :thinking:')
        else:
            raise error


def setup(bot):
    bot.add_cog(Admin(bot))

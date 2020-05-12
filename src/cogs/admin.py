"""
Module containing admin commands.
"""

# Builtins
import json
import logging

# Pip
import discord
from discord.ext import commands
from src.utils.database.repositories.currency_repository import \
    CurrencyRepository
from src.utils.general import DiscordEmbed

module_logger = logging.getLogger('koneko.Admin')


class Admin(commands.Cog):
    """Commands only for the bot owner"""

    __slots__ = 'bot', 'currency_repository'

    def __init__(self, bot):
        self.bot = bot
        self.currency_repository = CurrencyRepository()

    def cog_check(self, ctx):
        """Cog check

        Only returns true for bot owner."""
        return self.bot.is_owner(ctx.author)

    # TODO: allow for custom a status
    @commands.command(aliases=["watch", "listen"], hidden=True)
    async def game(self, ctx, *, name: str = None) -> None:
        """Change koneko's presence, owner only"""

        activities = {
            'game': discord.Game(name=name),
            'listen': discord.Activity(type=discord.ActivityType.listening,
                                       name=name),
            'watch': discord.Activity(type=discord.ActivityType.watching,
                                      name=name)
        }

        activity = activities[ctx.invoked_with]

        await self.bot.change_presence(status=discord.Status.online,
                                       activity=activity)

    @commands.command(aliases=["export"], hidden=True)
    async def export_db(self, _ctx) -> None:
        """Create an export of the currency table to a json file."""
        await self.currency_repository.export_db()

    @commands.command(aliases=["import"], hidden=True)
    async def import_db(self, _ctx) -> None:
        """Import to the currency table from a json file."""
        await self.currency_repository.import_db()

    @commands.group(hidden=True)
    async def sentence(self, ctx) -> None:
        """Sentence command group

        Used to modify Koneko's responses."""
        if ctx.invoked_subcommand is None:
            with open('src/cogs/utils/sentences.json') as f:
                data = json.load(f)
                json_str = json.dumps(data, indent=4, sort_keys=True)
                await DiscordEmbed.confirm(ctx, description=f'```json\n '
                                                            f'{json_str}```')
                return

    @sentence.command()
    async def get(self, ctx, command: str, string: str) -> None:
        """Sub-command to get a specific response."""
        with open('src/cogs/utils/sentences.json') as f:
            data = json.load(f)
            try:
                response = data[command][string]
                await ctx.channel.send(f"{command}.{string} is `{response}`")
            except KeyError:
                await ctx.channel.send(F"Could not find {command}.{string}")
                return

    @get.error
    async def get_error(self, ctx, error) -> None:
        """Error handler for getting a specific sentence."""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Some parameters seem missing :thinking:')
        else:
            raise error

    @sentence.command()
    async def update(self, ctx, command: str, string: str, *, new: str) -> None:
        """Sub-command to update a specific response."""
        # Open file in read mode.
        with open('src/cogs/utils/sentences.json', 'r') as f:
            data = json.load(f)

        # Try updating the key.
        try:
            data[command][string] = new
        except KeyError:
            await ctx.channel.send(F"Could not find {command}.{string}")
            return

        # Write the modified json object back to the file.
        with open('src/cogs/utils/sentences.json', 'w') as f:
            json.dump(data, f, indent=4, sort_keys=True)

    @update.error
    async def update_error(self, ctx, error) -> None:
        """Error handler for updating a specific response."""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Some parameters seem missing :thinking:')
        else:
            raise error


def setup(bot) -> None:
    """The setup function to add this cog to Koneko."""
    bot.add_cog(Admin(bot))

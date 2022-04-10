"""
Module containing admin commands.
"""

# Builtins
import asyncio
import json
import logging
from typing import Union, Dict

# Pip
import discord
from discord.ext import commands
from src.utils.general import DiscordEmbed

module_logger = logging.getLogger('koneko.Admin')


class Admin(commands.Cog):
    """Commands only for the bot owner"""

    __slots__ = 'bot',

    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        """Cog check

        Only returns true for bot owner."""
        return self.bot.is_owner(ctx.author)

    @commands.group(hidden=True)
    async def guilds(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is None:
            message: str = '\n'.join([f'{guild}' for guild in self.bot.guilds])

            return await ctx.channel.send(message)


    @guilds.command()
    async def leave(self, ctx: commands.Context, *, guild: Union[str, int]) -> None:
        if isinstance(guild, str):
            result: discord.Guild = discord.utils.get(self.bot.guilds, name=guild)
        else:
            result: discord.Guild = self.bot.get_guild(int(guild))

        if not result:
            return await ctx.channel.send(f"Guild \"{guild}\" could not be found")

        module_logger.debug(self.bot.config.get('favorite_guilds'))
        favorite_guilds = self.bot.config.get('favorite_guilds')
        if favorite_guilds and result.id in favorite_guilds:
            return await ctx.channel.send('Favorite guilds cannot be left.')

        m: discord.Message = await ctx.channel.send(f"Are you sure you want to leave \"{result}\"? [y-N]")

        def validate(m_):
            return m_.author == ctx.author and m_.channel == ctx.channel

        try:
            confirm: discord.Message = await ctx.bot.wait_for('message', check=validate,
                                            timeout=60)
            confirm: str = confirm.content
        except asyncio.TimeoutError:
            await m.delete()
            await ctx.channel.send('No response, aborted.')
            return

        if confirm in ['y', 'Y']:
            await result.leave()
            await ctx.channel.send(f"Left \"{result}\".")
        else:
            await ctx.channel.send(f"Action canceled.")

    @guilds.command()
    async def details(self, ctx: commands.Context, *, guild: str) -> None:
        result: Union[discord.Guild, None] = discord.utils.get(self.bot.guilds, name=guild)
        if not result:
            return await ctx.channel.send(f"Guild \"{guild}\" could not be found")

        await ctx.channel.send(f"Found {result.id} {result.name} {result.member_count} members.")

    # TODO: allow for custom a status
    @commands.command(aliases=["watch", "listen"], hidden=True)
    async def game(self, ctx: commands.Context, *, name: str = None) -> None:
        """Change koneko's presence, owner only"""

        activities: Dict[str] = {
            'game': discord.Game(name=name),
            'listen': discord.Activity(type=discord.ActivityType.listening,
                                       name=name),
            'watch': discord.Activity(type=discord.ActivityType.watching,
                                      name=name)
        }

        activity: str = activities[ctx.invoked_with]

        await self.bot.change_presence(status=discord.Status.online,
                                       activity=activity)

    @commands.group(hidden=True)
    async def sentence(self, ctx: commands.Context) -> None:
        """Sentence command group

        Used to modify Koneko's responses."""
        if ctx.invoked_subcommand is None:
            with open('src/cogs/utils/sentences.json') as f:
                data: dict = json.load(f)
                json_str: str = json.dumps(data, indent=4, sort_keys=True)
                await DiscordEmbed.confirm(ctx, description=f'```json\n '
                                                            f'{json_str}```')
                return

    @sentence.command()
    async def get(self, ctx: commands.Context, command: str, string: str) -> None:
        """Sub-command to get a specific response."""
        with open('src/cogs/utils/sentences.json') as f:
            data: dict = json.load(f)
            try:
                response: str = data[command][string]
                await ctx.channel.send(f"{command}.{string} is `{response}`")
            except KeyError:
                await ctx.channel.send(F"Could not find {command}.{string}")
                return

    @get.error
    async def get_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        """Error handler for getting a specific sentence."""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Some parameters seem missing :thinking:')
        else:
            raise error

    @sentence.command()
    async def update(self, ctx: commands.Context, command: str, string: str, *, new: str) -> None:
        """Sub-command to update a specific response."""
        # Open file in read mode.
        with open('src/cogs/utils/sentences.json', 'r') as f:
            data: dict = json.load(f)

        # Try updating the key.
        try:
            data[command][string]: str = new
        except KeyError:
            await ctx.channel.send(F"Could not find {command}.{string}")
            return

        # Write the modified json object back to the file.
        with open('src/cogs/utils/sentences.json', 'w') as f:
            json.dump(data, f, indent=4, sort_keys=True)

    @update.error
    async def update_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        """Error handler for updating a specific response."""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Some parameters seem missing :thinking:')
        else:
            raise error


def setup(bot) -> None:
    """The setup function to add this cog to Koneko."""
    bot.add_cog(Admin(bot))

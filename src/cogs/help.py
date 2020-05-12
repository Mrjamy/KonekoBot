# Credit to https://github.com/OneEyedKnight

# Builtins
import asyncio
from typing import List

# Pip
import discord
from discord.ext import commands


def chunks(parts, size):
    """Yield successive size-sized chunks from parts."""
    for i in range(0, len(parts), size):
        yield parts[i:i + size]


def helper(ctx) -> List[discord.Embed]:
    """Displays all commands"""

    cmds_ = []
    cogs = ctx.bot.cogs
    for i in cogs:
        cmd_ = ctx.bot.get_cog(i).get_commands()
        cmd_ = [x for x in cmd_ if not x.hidden]
        for x in list(chunks(list(cmd_), 6)):
            embed = discord.Embed(color=discord.Color.dark_purple())
            embed.set_author(name=f"{i} Commands ({len(cmd_)})")
            embed.description = ctx.bot.cogs[i].__doc__
            for y in x:
                embed.add_field(name=f"{y.name} {y.signature}", value=y.help, inline=False)
            cmds_.append(embed)

        for n, a in enumerate(cmds_):
            a.set_footer(
                text=f'Page {n+1} of {len(cmds_)} | Type "{ctx.prefix}help <command>" for more information'
            )
    return cmds_


def cog_helper(cog) -> List[discord.Embed]:
    """Displays commands from a cog"""

    name = cog.__class__.__name__
    cmds_ = []
    cmd = [x for x in cog.get_commands() if not x.hidden]
    if not cmd:
        return (discord.Embed(color=discord.Color.red(),
                              description=f"{name} commands are hidden.")
                .set_author(name="ERROR \N{NO ENTRY SIGN}"))

    for i in list(chunks(list(cmd), 6)):
        embed = discord.Embed(color=discord.Color.dark_purple())
        embed.set_author(name=name)
        embed.description = cog.__doc__
        for x in i:
            embed.add_field(name=f"{x.name} {x.signature}", value=x.help, inline=False)
        cmds_.append(embed)

    for n, a in enumerate(cmds_):
        a.set_footer(text=f"Page {n+1} of {len(cmds_)}")

    return cmds_


def command_helper(command: commands.command) -> List[discord.Embed]:
    """Displays a command and it's sub commands"""

    try:
        cmd = [x for x in command.commands if not x.hidden]  # retrieves commands that are not hidden
        cmds_ = []
        for i in list(chunks(list(cmd), 6)):
            embed = discord.Embed(color=discord.Color.dark_purple())
            embed.set_author(name=command.signature)
            embed.description = command.help
            for x in i:
                embed.add_field(name=f"{x.name} {x.signature}", value=x.help, inline=False)
            cmds_.append(embed)

        for n, x in enumerate(cmds_):
            x.set_footer(text=f"Page {n+1} of {len(cmds_)}")
        return cmds_
    except AttributeError:
        embed = discord.Embed(color=discord.Color.dark_purple())
        embed.set_author(name=f"{command.name} {command.signature}")
        embed.description = command.help
        return [embed]


# ?tag lazy paginator is a more refined/easier to read version of this paginator.
async def paginate(ctx, input_: List[discord.Embed]) -> None:
    """Paginator"""

    try:
        pages = await ctx.send(embed=input_[0])
    except (AttributeError, TypeError):
        await ctx.send(embed=input_)
        return

    if len(input_) == 1:
        return

    current = 0

    r = ['\U000023ee', '\U000025c0', '\U000025b6',
         '\U000023ed', '\U0001f522', '\U000023f9']
    for x in r:
        await pages.add_reaction(x)

    paging = True
    while paging:
        reaction = None

        def check(r_, u_) -> bool:
            return u_ == ctx.author and r_.message.id == pages.id and str(r_.emoji) in r

        done, pending = await asyncio.wait([ctx.bot.wait_for('reaction_add', check=check, timeout=120),
                                            ctx.bot.wait_for('reaction_remove', check=check, timeout=120)],
                                           return_when=asyncio.FIRST_COMPLETED)
        try:
            reaction, user = done.pop().result()
        except asyncio.TimeoutError:
            try:
                await pages.clear_reactions()
            except discord.Forbidden:
                await pages.delete()

            paging = False

        for future in pending:
            future.cancel()
        else:
            if str(reaction.emoji) == r[2]:
                current += 1
                if current == len(input_):
                    current = 0
                    try:
                        await pages.remove_reaction(r[2], ctx.author)
                    except discord.Forbidden:
                        pass
                    await pages.edit(embed=input_[current])

                await pages.edit(embed=input_[current])
            elif str(reaction.emoji) == r[1]:
                current -= 1
                if current == 0:
                    try:
                        await pages.remove_reaction(r[1], ctx.author)
                    except discord.Forbidden:
                        pass

                    await pages.edit(embed=input_[len(input_) - 1])

                await pages.edit(embed=input_[current])
            elif str(reaction.emoji) == r[0]:
                current = 0
                try:
                    await pages.remove_reaction(r[0], ctx.author)
                except discord.Forbidden:
                    pass

                await pages.edit(embed=input_[current])

            elif str(reaction.emoji) == r[3]:
                current = len(input_) - 1
                try:
                    await pages.remove_reaction(r[3], ctx.author)
                except discord.Forbidden:
                    pass

                await pages.edit(embed=input_[current])

            elif str(reaction.emoji) == r[4]:
                m = await ctx.send(f"What page you do want to go? 1-{len(input_)}")

                def pager(m_) -> bool:
                    return m_.author == ctx.author and m_.channel == ctx.channel and int(m_.content) > 1 <= len(input_)

                try:
                    msg = int((await ctx.bot.wait_for('message', check=pager, timeout=60)).content)
                except asyncio.TimeoutError:
                    await m.delete()
                    return
                current = msg - 1
                try:
                    await pages.remove_reaction(r[4], ctx.author)
                except discord.Forbidden:
                    pass

                await pages.edit(embed=input_[current])
            else:
                try:
                    await pages.clear_reactions()
                except discord.Forbidden:
                    await pages.delete()

                paging = False


class Help(commands.Cog):
    """Help command"""

    __slots__ = ('bot',)

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["h"], hidden=True)
    async def help(self, ctx, *, command: str = None) -> None:
        # TODO: v1.2 display aliases too
        if not command:
            await paginate(ctx, helper(ctx))

        if command:
            thing = ctx.bot.get_cog(command) or ctx.bot.get_command(command)
            if not thing:
                await ctx.send(f'Looks like "{command}" is not a command or category.')
                return
            if isinstance(thing, commands.Command):
                await paginate(ctx, command_helper(thing))
            else:
                await paginate(ctx, cog_helper(thing))


def setup(bot) -> None:
    """The setup function to add this cog to Koneko."""
    bot.add_cog(Help(bot))

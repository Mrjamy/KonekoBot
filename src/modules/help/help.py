# TODO: add custom help command

# TODO: add /h command (/help alias)\

import re
from KonekoBot import koneko

_mentions_transforms = {
    '@everyone': '@\u200beveryone',
    '@here': '@\u200bhere'
}
_mention_pattern = re.compile('|'.join(_mentions_transforms.keys()))


@koneko.command(name='help', aliases=['h'], pass_context=True, hidden=True)
async def _default_help_command(ctx, *commands: str):
    """Shows this message."""

    def repl(obj):
        print('halp')
        return _mentions_transforms.get(obj.group(0), '')

    # If no commands are supplied help will return a brief summary of all commands.
    if len(commands) == 0:
        pages = await koneko.formatter.format_help_for(ctx, koneko)
    # If one command is supplied attempt to show it description.
    elif len(commands) == 1:
        print(3)
        # try to see if it is a cog name
        name = _mention_pattern.sub(repl, commands[0])
        command = None
        if name in koneko.cogs:
            command = koneko.cogs[name]
        else:
            if name in koneko.all_commands:
                command = name
            if command is None:
                await ctx.channel.send((koneko.command_not_found.format(name)))
                return

        print(ctx)
        print(command)
        pages = await koneko.formatter.format_help_for(ctx, command)
        print(pages)
    else:
        print(4)
        name = _mention_pattern.sub(repl, commands[0])
        command = None
        if name in koneko.all_commands:
            command = name
        if command is None:
            await ctx.channel.send(koneko.command_not_found.format(name))
            return

        for key in commands[1:]:
            try:
                command = None
                key = _mention_pattern.sub(repl, key)
                if key in koneko.all_commands:
                    command = key
                if command is None:
                    await ctx.channel.send(koneko.command_not_found.format(key))
                    return
            except AttributeError:
                await ctx.channel.send(koneko.command_has_no_subcommands.format(command, key))
                return

        pages = await koneko.formatter.format_help_for(ctx, command)

        if koneko.pm_help is None:
            characters = sum(map(lambda l: len(l), pages))
            # modify destination based on length of pages.
            if characters > 1000:
                await ctx.message.author.pm
                return
    for page in pages:
        await ctx.channel.send(page)

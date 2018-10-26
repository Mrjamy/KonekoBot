from discord.ext import commands
from sys import argv

prefix = "!"
startup_extensions = [
    "modules.welcome",
    "modules.goodbye",
    "modules.general",
    "modules.response.response",
    "modules.music.music"
]

bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix))
bot.pm_help = False


# Function called when the bot is ready.
@bot.event
async def on_ready():
    # Bot logged in.
    print('Logged in as {0.user}'.format(bot))

if __name__ == '__main__':
    for extension in startup_extensions:
        bot.load_extension(extension)
    bot.run(argv[1])

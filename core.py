import discord
import config

client = discord.Client()


@client.event
async def on_ready():
    # Bot logged in.
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

client.run(config.token)

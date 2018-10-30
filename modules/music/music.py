import asyncio
import discord
import youtube_dl

from multiprocessing import Process
from discord.ext import commands

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music:
    def __init__(self, bot):
        self.bot = bot
        self.__queue = asyncio.Queue()

    @commands.command(pass_context=True)
    async def join(self, ctx, *, channel: discord.VoiceChannel = None):
        """Make the bot join the voice channel."""
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                print("InvalidVoiceChannel('No channel to join. Please either specify a valid channel or join one.')")

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                print("VoiceConnectionError(f'Moving to channel: <{channel}> timed out.')")
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                print("VoiceConnectionError(f'Connecting to channel: <{channel}> timed out.')")

        await ctx.send(f'Connected to: **{channel}**', delete_after=20)

    @commands.command()
    async def play(self, ctx):
        """Plays from a url, only youtube supported."""
        while self.__queue:
            for task in self.__queue:


    @commands.command()
    async def add(self, ctx, *, url):
        player = await YTDLSource.from_url(url, loop=self.bot.loop)
        await self.__queue.put(ctx.voice_client.play(
            player, after=lambda e: print('Player error: %s' % e) if e else None
        ))

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume."""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice."""

        await ctx.voice_client.disconnect()

    # TODO: add method deque.
    async def next(self):
        return self.__queue.get()

    # TODO: add method empty_que
    async def empty_que(self):
        self.__queue.empty()
        return

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


def setup(bot):
    bot.add_cog(Music(bot))

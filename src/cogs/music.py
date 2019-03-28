import asyncio
import itertools
from async_timeout import timeout
from functools import partial
import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
from .helpers.exceptions import VoiceConnectionError, InvalidVoiceChannel

# TODO: Fully implement checks.
# TODO: Customizable role for is_dj() check.
from src.core.checks import Checks


ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
}

ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')

        # YTDL info dicts (data) have other useful information you might want
        # https://github.com/rg3/youtube-dl/blob/master/README.md

    def __getitem__(self, item: str):
        """Allows us to access attributes similar to a dict.
        This is only useful when you are NOT downloading.
        """
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
            # TODO: add support for full playlists (terminating once max queue size has been reached)

        embed = discord.Embed(title=f'```[Added {data["title"]} to the Queue.]\n```',
                              color=discord.Color.green())
        await ctx.channel.send(embed=embed, delete_after=20)

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        """Used for preparing a stream, instead of downloading.
        Since Youtube Streaming links expire."""
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)


class MusicPlayer:
    """A class which is assigned to each guild using the bot for Music.
    This class implements a queue and loop, which allows for different guilds to listen to different playlists
    simultaneously.
    When the bot disconnects from the Voice it's instance will be destroyed.
    """

    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None  # Now playing message
        self.volume = .5
        self.current = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        """Our main player loop."""
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                # Wait for the next song. If we timeout cancel the player and disconnect...
                async with timeout(300):  # 5 minutes...
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                # Source was probably a stream (not downloaded)
                # So we should regather to prevent stream expiration
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    embed = discord.Embed(title=f'There was an error processing your song.\n ```css\n[{e}]\n```',
                                          color=discord.Color.red())
                    await self._channel.send(embed=embed)
                    continue

            source.volume = self.volume
            self.current = source

            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            embed = discord.Embed(title=f'**Now Playing:** `{source.title}` requested by `{source.requester}`',
                                  color=discord.Color.green())
            self.np = await self._channel.send(embed=embed)
            await self.next.wait()

            # Make sure the FFmpeg process is cleaned up.
            source.cleanup()
            self.current = None

            try:
                # We are no longer playing this song...
                await self.np.delete()
            except discord.HTTPException:
                pass

    def destroy(self, guild):
        """Disconnect and cleanup the player."""
        return self.bot.loop.create_task(self._cog.cleanup(guild))


class Music(commands.Cog):
    """Music related commands."""

    __slots__ = ('bot', 'players')

    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    def get_player(self, ctx):
        """Retrieve the guild player, or generate one."""
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    @Checks.is_connected_voice()
    @commands.guild_only()
    @commands.command(name='connect', aliases=['join'], pass_context=True)
    async def connect_(self, ctx):
        """Connect to voice."""

        channel = ctx.author.voice.channel
        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                embed = discord.Embed(title=f'Moving to channel: <{channel}> timed out.',
                                      color=discord.Color.red())
                await ctx.channel.send(embed=embed)
                return
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                embed = discord.Embed(title=f'Connecting to channel: <{channel}> timed out.',
                                      color=discord.Color.red())
                await ctx.channel.send(embed=embed)
                return

        embed = discord.Embed(title=f'Connected to: **{channel}**',
                              color=discord.Color.green())
        await ctx.channel.send(embed=embed, delete_after=20)

    @Checks.is_connected_voice()
    @commands.guild_only()
    @commands.command(name='play', aliases=['sing'], pass_context=True)
    async def play_(self, ctx, *, search: str):
        """Request a song and add it to the queue.
        This command attempts to join a valid voice channel if the bot is not already in one.
        Uses YTDL to automatically search and retrieve a song.
        Parameters
        ------------
        search: str [Required]
            The song to search and retrieve using YTDL. This could be a simple search, an ID or URL.
        """
        await ctx.trigger_typing()

        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect_)

        player = self.get_player(ctx)

        # If download is False, source will be a dict which will be used later to regather the stream.
        # If download is True, source will be a discord.FFmpegPCMAudio with a VolumeTransformer.
        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)

        await player.queue.put(source)

    # @Checks.is_dj()
    @Checks.is_connected_voice()
    @commands.guild_only()
    @commands.command(name='pause', aliases=[], pass_context=True)
    async def pause_(self, ctx):
        """Pause the currently playing song."""
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            embed = discord.Embed(title='I am not currently playing anything!',
                                  color=discord.Color.red())
            return await ctx.channel.send(embed=embed, delete_after=20)
        elif vc.is_paused():
            return

        vc.pause()
        embed = discord.Embed(title=f'**`{ctx.author}`**: Paused the song!',
                              color=discord.Color.green())
        await ctx.channel.send(embed=embed, delete_after=20)

    # @Checks.is_dj()
    @Checks.is_connected_voice()
    @commands.guild_only()
    @commands.command(name='resume', aliases=[], pass_context=True)
    async def resume_(self, ctx):
        """Resume the currently paused song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title='I am not currently playing anything!',
                                  color=discord.Color.red())
            return await ctx.channel.send(embed=embed, delete_after=20)
        elif not vc.is_paused():
            return

        vc.resume()
        embed = discord.Embed(title=f'**`{ctx.author}`**: Resumed the song!',
                              color=discord.Color.green())
        await ctx.channel.send(embed=embed, delete_after=20)

    # @Checks.is_dj()
    @Checks.is_connected_voice()
    @commands.guild_only()
    @commands.command(name='skip', aliases=[], pass_context=True)
    async def skip_(self, ctx):
        """Skip the song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title='I am not currently playing anything!',
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed, delete_after=20)

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        vc.stop()
        embed = discord.Embed(title=f'**`{ctx.author}`**: Skipped the song!',
                              color=discord.Color.green())
        await ctx.channel.send(embed=embed)

    @commands.guild_only()
    @commands.command(name='queue', aliases=['q', 'playlist'], pass_context=True)
    async def queue_info(self, ctx):
        """Retrieve a basic queue of upcoming songs."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title='I am not currently connected to voice!',
                                  color=discord.Color.red())
            return await ctx.channel.send(embed=embed)

        player = self.get_player(ctx)
        if player.queue.empty():
            embed = discord.Embed(title='There are currently no more queued songs.',
                                  color=discord.Color.darker_grey())
            return await ctx.channel.send(embed=embed)

        # Grab up to 5 entries from the queue...
        upcoming = list(itertools.islice(player.queue._queue, 0, 5))

        # TODO: add indexing for queued songs.
        # TODO: nice formatting.
        fmt = '\n'.join(f'**`{_["title"]}`**' for _ in upcoming)
        embed = discord.Embed(title=f'Upcoming - Next {len(upcoming)}', description=fmt,
                              color=discord.Color.darker_grey())
        return await ctx.channel.send(embed=embed)

    @commands.guild_only()
    @commands.command(name='now_playing', aliases=['np', 'current', 'currentsong', 'playing'], pass_context=True)
    async def now_playing_(self, ctx):
        """Display information about the currently playing song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title='I am not currently connected to voice!',
                                  color=discord.Color.red())
            return await ctx.channel.send(embed=embed, delete_after=20)

        player = self.get_player(ctx)
        if not player.current:
            embed = discord.Embed(title='I am not currently playing anything!',
                                  color=discord.Color.red())
            return await ctx.channel.send(embed=embed, delete_after=20)

        try:
            # Remove our previous now_playing message.
            await player.np.delete()
        except discord.HTTPException:
            pass

        embed = discord.Embed(title=f'**Now Playing:** `{vc.source.title}` '
                              f'requested by `{vc.source.requester}`',
                              color=discord.Color.green())
        player.np = await ctx.channel.send(embed=embed, delete_after=20)

    # @Checks.is_dj()
    @Checks.is_connected_voice()
    @commands.guild_only()
    @commands.command(name='volume', aliases=['vol'], pass_context=True)
    async def change_volume(self, ctx, *, volume: float):
        """Change the player volume.
        Parameters
        ------------
        volume: float or int [Required]
            The volume to set the player to in percentage. This must be between 1 and 100.
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title='I am not currently connected to voice!',
                                  color=discord.Color.red())
            return await ctx.channel.send(embed=embed, delete_after=20)

        if not 0 < volume < 101:
            embed = discord.Embed(title='Please enter a value between 1 and 100.',
                                  color=discord.Color.red())
            return await ctx.channel.send(embed=embed, delete_after=20)

        player = self.get_player(ctx)

        if vc.source:
            vc.source.volume = volume / 100

        player.volume = volume / 100
        embed = discord.Embed(title=f'**`{ctx.author}`**: Set the volume to **{volume}%**',
                              color=discord.Color.green())
        await ctx.channel.send(embed=embed)

    # @Checks.is_dj()
    @Checks.is_connected_voice()
    @commands.guild_only()
    @commands.command(name='stop', aliases=[], pass_context=True)
    async def stop_(self, ctx):
        """Stop the currently playing song.
        !Warning!
            This will destroy the player assigned to your guild, also deleting any queued songs and settings.
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title='I am not currently playing anything!',
                                  color=discord.Color.red())
            return await ctx.channel.send(embed=embed, delete_after=20)

        await self.cleanup(ctx.guild)


def setup(bot):
    bot.add_cog(Music(bot))

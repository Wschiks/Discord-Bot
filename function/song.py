# song.py
from discord.ext import commands
import discord
import random
import yt_dlp
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import asyncio
import discord


if not discord.opus.is_loaded():
    discord.opus.load_opus("/opt/homebrew/opt/opus/lib/libopus.dylib")


# Spotify api
SPOTIFY_CLIENT_ID = "13f09639d9324f26927f659aa96b0ea0"
SPOTIFY_CLIENT_SECRET = "a4e95c7959de4d2d937ae3d961145012"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

ytdl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True
}

ffmpeg_opts = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = yt_dlp.YoutubeDL(ytdl_opts)

# ----------------------------
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="nieknee")
    async def nieknee(self, ctx, playlist_id: str = "5DDZ7UzIZPjAPBoYT5UrG4"):
        # Join user's voice channel
        if not ctx.voice_client:
            await ctx.author.voice.channel.connect()
            await asyncio.sleep(1)

        # Pick a random Spotify track
        track = random.choice(sp.playlist_tracks(playlist_id)['items'])['track']
        track_name = f"{track['artists'][0]['name']} - {track['name']}"

        # Get YouTube audio
        info = ytdl.extract_info(f"ytsearch:{track_name}", download=False)['entries'][0]
        url = info['url']

        # Play in Discord
        source = discord.FFmpegPCMAudio(url, **ffmpeg_opts)
        player = discord.PCMVolumeTransformer(source, volume=0.8)
        ctx.voice_client.play(player)
        await ctx.send(f"Now playing: {track_name}")

    @commands.command(name="leave")
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected from the voice channel!")

    @commands.command(name="skip")
    async def skip(self, ctx, playlist_id: str = "5DDZ7UzIZPjAPBoYT5UrG4"):
        ctx.voice_client.stop()
        # Join user's voice channel
        if not ctx.voice_client:
            await ctx.author.voice.channel.connect()
            await asyncio.sleep(1)

        # Pick a random Spotify track
        track = random.choice(sp.playlist_tracks(playlist_id)['items'])['track']
        track_name = f"{track['artists'][0]['name']} - {track['name']}"

        # Get YouTube audio
        info = ytdl.extract_info(f"ytsearch:{track_name}", download=False)['entries'][0]
        url = info['url']

        # Play in Discord
        source = discord.FFmpegPCMAudio(url, **ffmpeg_opts)
        player = discord.PCMVolumeTransformer(source, volume=0.8)
        ctx.voice_client.play(player)
        await ctx.send(f"Now playing: {track_name}")


# Setup function
async def setup(bot):
    await bot.add_cog(Music(bot))

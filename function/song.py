from discord.ext import commands
import discord
import random
import yt_dlp
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import asyncio

# voor binnen het gesprek
if not discord.opus.is_loaded():
    discord.opus.load_opus("/opt/homebrew/opt/opus/lib/libopus.dylib")

# Spotify dingentjes
SPOTIFY_CLIENT_ID = "13f09639d9324f26927f659aa96b0ea0"
SPOTIFY_CLIENT_SECRET = "a4e95c7959de4d2d937ae3d961145012"
SPOTIFY_DEFAULT_ID = "3XKvUkeeuxTcKAKBrzR4lE"

# link to spotify
sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    )
)


ytdl_opts = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True
}
ffmpeg_opts = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn"
}
ytdl = yt_dlp.YoutubeDL(ytdl_opts)


# Helper: detect playlist vs album
def get_spotify_tracks(spotify_id: str):
    # Remove ?si=... if user pastes full link
    spotify_id = spotify_id.split("?")[0].split("/")[-1]

    try:
        # Try playlist first
        return [item["track"] for item in sp.playlist_tracks(spotify_id)["items"]]
    except spotipy.exceptions.SpotifyException:
        # If not playlist, try album
        try:
            return sp.album_tracks(spotify_id)["items"]
        except spotipy.exceptions.SpotifyException:
            return []


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="nieknee")
    async def nieknee(self, ctx, spotify_id: str = SPOTIFY_DEFAULT_ID):
        if not ctx.author.voice:
            await ctx.send("You must be in a voice channel to play music!")
            return

        if not ctx.voice_client:
            await ctx.author.voice.channel.connect()
            await asyncio.sleep(1)

        tracks = get_spotify_tracks(spotify_id)
        if not tracks:
            await ctx.send("Could not load tracks from Spotify (invalid link or ID).")
            return

        track = random.choice(tracks)
        track_name = f"{track['artists'][0]['name']} - {track['name']}"
        await ctx.send(f"Now playing: {track_name}")

        info = ytdl.extract_info(f"ytsearch:{track_name}", download=False)["entries"][0]
        url = info["url"]

        source = discord.FFmpegPCMAudio(url, **ffmpeg_opts)
        player = discord.PCMVolumeTransformer(source, volume=0.8)
        ctx.voice_client.play(player)

    @commands.command(name="niekvolgende")
    async def skip(self, ctx, spotify_id: str = SPOTIFY_DEFAULT_ID):
        if ctx.voice_client:
            ctx.voice_client.stop()
        await self.nieknee(ctx, spotify_id)

    @commands.command(name="niekstop")
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Disconnected from the voice channel!")
        else:
            await ctx.send("I'm not connected to a voice channel.")


async def setup(bot):
    await bot.add_cog(Music(bot))

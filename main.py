import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

async def main():
    # Load all cogs
    await bot.load_extension("function.feitje")
    await bot.load_extension("function.song")
    await bot.load_extension("function.uitleg")
    await bot.load_extension("function.praat")

    await bot.start(TOKEN)

asyncio.run(main())

import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Load cogs properly in discord.py v2
import asyncio
async def load_cogs():
    await bot.load_extension("function.feitje")

asyncio.run(load_cogs())

bot.run(TOKEN)

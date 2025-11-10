import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Load token from .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Set up intents (required by discord.py v2+)
intents = discord.Intents.default()
intents.message_content = True  # Required to read messages

# Create bot with command prefix and intents
bot = commands.Bot(command_prefix="!", intents=intents)

# Event: bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Command: !niek
@bot.command(name='niek')
async def niek_command(ctx):
    await ctx.send("Hello")

# Run the bot
bot.run(TOKEN)

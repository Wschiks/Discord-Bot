import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import asyncio

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
ARENA_CHANNEL_ID = int(os.getenv("ARENA_CHANNEL_ID") or 0)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# Store config so cogs can access it
bot.config = {"ARENA_CHANNEL_ID": ARENA_CHANNEL_ID}

@bot.event
async def on_ready():
    print(f"Bot online als {bot.user}")

async def main():
    async with bot:
        # Load all your cogs/extensions
        await bot.load_extension("function.feitje")
        await bot.load_extension("function.song")
        await bot.load_extension("function.uitleg")
        await bot.load_extension("function.arena")

        # Start bot
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())

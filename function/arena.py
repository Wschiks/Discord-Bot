# function/arena.py
import os
import discord
from discord.ext import commands
import asyncio
import random
import openai
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Virtual bots
VIRTUAL_BOTS = [
    {"name": "Niek Brot", "persona": "vrolijk en enthousiast", "avatar_url": "https://i.imgur.com/avatar1.png"},
    {"name": "Niek Brot 2", "persona": "sarcastisch en kritisch", "avatar_url": "https://i.imgur.com/avatar2.png"},
    {"name": "Niek Brot 3", "persona": "mopperig en cynisch", "avatar_url": "https://i.imgur.com/avatar3.png"},
    {"name": "Niek Brot 4", "persona": "wijs en kalm", "avatar_url": "https://i.imgur.com/avatar4.png"},
    {"name": "Niek Brot 5", "persona": "hyper en chaotisch", "avatar_url": "https://i.imgur.com/avatar5.png"},
]

class Arena(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def generate_ai_response(self, bot_info, last_message):
        prompt = f"""
        Jij bent een Discord bot genaamd "{bot_info['name']}".
        Persoonlijkheid: {bot_info['persona']}.
        Het laatste bericht van een andere bot was: "{last_message}"
        Reageer kort, grappig of passend bij je persoonlijkheid, max 100 tekens.
        """
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=50,
                temperature=0.8
            )
            return response.choices[0].text.strip()
        except Exception as e:
            print("OpenAI error:", e)
            return random.choice(["Hmm...", "Oké.", "😂", "Interessant!"])

    async def run_arena(self, channel: discord.TextChannel, messages: int):
        print(f"[DEBUG] Starting arena in channel {channel.name} ({channel.id})")

        # Create webhooks
        webhooks = []
        existing = await channel.webhooks()
        for bot_info in VIRTUAL_BOTS:
            wh = discord.utils.get(existing, name=bot_info["name"])
            if not wh:
                wh = await channel.create_webhook(name=bot_info["name"])
                print(f"[DEBUG] Created webhook for {bot_info['name']}")
            webhooks.append((wh, bot_info["avatar_url"]))

        await channel.send(f"🎙️ NiekBrot Arena gestart: {len(webhooks)} bots praten ({messages} berichten)")

        last_message = "Start van de conversatie!"
        for i in range(messages):
            wh, avatar = random.choice(webhooks)
            msg = await self.generate_ai_response(
                {"name": wh.name, "persona": [b['persona'] for b in VIRTUAL_BOTS if b['name'] == wh.name][0]},
                last_message
            )
            print(f"[DEBUG] Sending message {i+1}: '{msg}' from {wh.name}")
            await wh.send(msg, avatar_url=avatar)
            last_message = msg
            await asyncio.sleep(random.uniform(0.8, 1.8))

        await channel.send("🏁 Arena afgelopen!")
        print("[DEBUG] Arena finished")

    @commands.command(name="niekpraat")
    async def niekpraat_command(self, ctx, messages: int = 30):
        ARENA_CHANNEL_ID = self.bot.config.get("ARENA_CHANNEL_ID", 0)
        print(f"[DEBUG] !niekpraat command invoked in channel {ctx.channel.id}, expected {ARENA_CHANNEL_ID}")

        if ctx.channel.id != ARENA_CHANNEL_ID:
            await ctx.send("Gebruik de arena-kanaal!")
            print("[DEBUG] Wrong channel, message sent to user")
            return

        await self.run_arena(ctx.channel, messages)

async def setup(bot: commands.Bot):
    await bot.add_cog(Arena(bot))

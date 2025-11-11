# praat.py
import os
import discord
from discord.ext import commands
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
PRAAT_CHANNEL_ID = int(os.getenv("PRAAT_CHANNEL_ID"))

class Praat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        # Debug: print all messages
        print(f"Message from {msg.author}: {msg.content}")

        # Ignore bots and messages from other channels
        if msg.author.bot or msg.channel.id != PRAAT_CHANNEL_ID:
            return

        try:
            print("Sending request to OpenAI...")
            # Call OpenAI synchronously
            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a funny, friendly Discord bot named Niek."},
                    {"role": "user", "content": msg.content}
                ]
            )

            reply_text = res.choices[0].message.content
            print("Replying with:", reply_text)
            await msg.reply(reply_text)

        except Exception as e:
            print("OpenAI error:", e)
            await msg.reply("Oops! Something went wrong with OpenAI.")

        # Let commands still work if you add any
        await self.bot.process_commands(msg)

async def setup(bot):
    await bot.add_cog(Praat(bot))

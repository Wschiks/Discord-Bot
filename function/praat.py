# praat_ai_min.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer

load_dotenv()
PRAAT_CHANNEL_ID = int(os.getenv("PRAAT_CHANNEL_ID"))

# link naar path
tokenizer = AutoTokenizer.from_pretrained("./models/gpt-neo-125m")
model = AutoModelForCausalLM.from_pretrained("./models/gpt-neo-125m")

# maakt de reactie terug aan
def generate_reply(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_new_tokens=40,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        repetition_penalty=1.3,
        pad_token_id=tokenizer.eos_token_id
    )


    return tokenizer.decode(outputs[0], skip_special_tokens=True)

class Praat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.channel.id != PRAAT_CHANNEL_ID or msg.author == self.bot.user:
            return


        async with msg.channel.typing():
            reply = generate_reply(msg.content)

        await msg.channel.send(reply)


async def setup(bot):
    await bot.add_cog(Praat(bot))

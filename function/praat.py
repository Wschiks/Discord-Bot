import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer

load_dotenv()
PRAAT_CHANNEL_ID = int(os.getenv("PRAAT_CHANNEL_ID"))

# link naar path
tokenizer = AutoTokenizer.from_pretrained("./models/gpt-neo-350m")
model = AutoModelForCausalLM.from_pretrained("./models/gpt-neo-350m")

# maakt de reactie terug aan
def generate_reply(prompt):
    # zet de "hallo hoe gaat ie" om naar "76 28 186 374" en dan in stukken hakken "76" "28" "186" "374"
    inputs = tokenizer(prompt, return_tensors="pt")
    # bedenkt een response op "76" "28" "186" "374"
    outputs = model.generate(
        # geeft "76" "28" "186" "374" af
        **inputs,
        max_new_tokens=100,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        repetition_penalty=1.3,
        pad_token_id=tokenizer.eos_token_id
    )

# zet de nieuwe bedachte zin weer terug om naar leesbare taal
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


# moet gewoon zodat de bot weet wei hij is
class Praat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
#als er een bericht word versruurd bekijk dan of het in de juiste chat is anders neit luisterem.
    async def on_message(self, msg):
        if msg.channel.id != PRAAT_CHANNEL_ID or msg.author == self.bot.user:
            return

#doet alsof hij aan het typen is
        async with msg.channel.typing():
            #replay = functie om replay te maken (bericht die user vertuurd via discoord)
            reply = generate_reply(msg.content)
# stuur de replay in de discoord chat
        await msg.channel.send(reply)


async def setup(bot):
    await bot.add_cog(Praat(bot))

from discord.ext import commands
import random
from function.list_feit import feitjes

class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # hier wordt aangeroept dat als je !niek doet dat die een random feitje pakt van list_feit in de lijst feitjes
    @commands.command(name="niek")
    async def niek(self, ctx):
        feitje = random.choice(feitjes)
        await ctx.send(feitje)

async def setup(bot):
    await bot.add_cog(Hello(bot))

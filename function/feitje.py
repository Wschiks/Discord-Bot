from discord.ext import commands
import random
from function.list_feit import feitjes

class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="niek")
    async def niek(self, ctx):
        feitje = random.choice(feitjes)
        await ctx.send(feitje)

async def setup(bot):
    await bot.add_cog(Hello(bot))


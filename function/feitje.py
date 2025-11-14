from discord.ext import commands
import random
from function.list_feit import feitjes

class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # hier wordt aangeroept dat als je !niek doet dat die een random feitje pakt van list_feit in de lijst feitjes

    # !niek → geeft een random feitje uit de lijst
    @commands.command(name="niek")
    async def niek(self, ctx):
        feitje = random.choice(feitjes)
        await ctx.send(feitje)


    # !niekwist <tekst> → voegt feitje toe, maar antwoord is altijd "Wist ik al"
    @commands.command(name="niekwist")
    async def niekwist(self, ctx, *, tekst: str):
        feitjes.append(tekst)   # voeg het feitje toe
        await ctx.send("Wist ik al")  # reactie is ALTIJD dit


async def setup(bot):
    await bot.add_cog(Hello(bot))

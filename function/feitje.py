from discord.ext import commands

class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="niek")
    async def hello(self, ctx):
        await ctx.send("baskldjfhlkasdjfh")

async def setup(bot):
    await bot.add_cog(Hello(bot))

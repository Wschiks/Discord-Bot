from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info")
    async def info(self, ctx):
        message = (
            "**# Welkom bij Niek Brot!**\n"
            "**De enige echte bot die zorgt voor muziek, feitjes en gezelligheid in de server!**\n\n"
            "**🎵 MUZIEK COMMANDO'S**\n"
            "`!nieknee` — Speelt een willekeurig nummer uit een Spotify playlist of album\n"
            "`!niekvolgende` — Slaat het huidige nummer over en speelt een nieuw nummer\n"
            "`!niekweg` — Laat de bot het voice kanaal verlaten\n\n"
            "**💡 FEITJES**\n"
            "`!niek` — Laat een willekeurig grappig of interessant feitje zien\n\n"
            "\n"
            "Gebruik `!info` om dit bericht opnieuw te zien 🍞"
        )

        await ctx.send(message)

async def setup(bot):
    await bot.add_cog(Info(bot))

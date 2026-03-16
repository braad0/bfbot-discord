import discord
from discord.ext import commands

class myCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.ekillibre = "https://platform.ekillibre.com/fr/qr/ZGFmNWU5Y2EtNTYyNC00OTk3LWExYzYtNTRlNTg1YTkzMjA4.9JXZeGTUhvadtqeWyCoLwGGEY_yUAaov3GAkgXaJRuk"

    @commands.Cog.listener()
    async def on_ready(self):
        print("Scheduler pause On")

    @commands.command(name="sandwich", description="Rechercher un emploi sur Jooble Belgique")
    async def sandwich(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        await ctx.send("Sandwich")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(myCog(bot))
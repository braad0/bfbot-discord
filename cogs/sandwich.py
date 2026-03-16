import discord
from discord import app_commands
from discord.ext import commands

class LinkView(discord.ui.View):
    def __init__(self, label: str, url: str):
        super().__init__()
        self.add_item(discord.ui.Button(label=label, url=url))

class myCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.ekillibre_url = "https://platform.ekillibre.com/fr/qr/ZGFmNWU5Y2EtNTYyNC00OTk3LWExYzYtNTRlNTg1YTkzMjA4.9JXZeGTUhvadtqeWyCoLwGGEY_yUAaov3GAkgXaJRuk"
        self.arbeapain = "https://click-eat.be/fr/magasin/arbre-a-pain"

    @commands.Cog.listener()
    async def on_ready(self):
        print("Sandwich listener on")

    @app_commands.command(name="sandwich", description="Ekillibre")
    async def sandwich(self, interaction: discord.Interaction):
        view = LinkView(label="Commander chez Ekillibre", url=self.ekillibre_url)
        await interaction.response.send_message(f"Sandwich", view=view)

    @app_commands.command(name="menu", description="Afficher la carte des menus")
    async def menu(self, interaction: discord.Interaction):
        file_path = "noko.jpg" 
        
        try:
            file = discord.File(file_path, filename="noko.jpg")
            embed = discord.Embed(title="Carte de Noko", color=discord.Color.green())
            embed.set_image(url="attachment://noko.jpg")
            
            await interaction.response.send_message(file=file, embed=embed)
            print("Menu envoyé avec succès !")
            
        except FileNotFoundError:
            await interaction.response.send_message(f"Erreur : Je ne trouve pas le fichier à l'adresse : `{file_path}`", ephemeral=True)
            print(f"Erreur : Fichier introuvable à {file_path}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(myCog(bot))
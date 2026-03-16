import discord
from discord import app_commands
from discord.ext import commands
import http.client
import json
import os

class JoobleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.jooble_key = os.getenv('JOOBLE_API_KEY')

    @app_commands.command(name="jobs", description="Recherche Jooble Belgique")
    async def jobs(self, interaction: discord.Interaction, keywords: str, location: str):
        await interaction.response.defer(ephemeral=True)

        try:
            host = 'be.jooble.org'
            connection = http.client.HTTPSConnection(host)
            
            headers = {
                "Content-type": "application/json; charset=utf-8",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36"
            }
            
            # Forcer la recherche "ET" avec les guillemets
            exact_keywords = f'"{keywords}"'
            
            body_dict = {
                "keywords": exact_keywords, 
                "location": location,
                "radius": "25",
                "searchMode": "1" 
            }
            body = json.dumps(body_dict, ensure_ascii=False).encode('utf-8')

            connection.request('POST', f'/api/{self.jooble_key}', body, headers)
            response = connection.getresponse()
            
            # --- RÉCUPÉRATION DU QUOTA ---
            # Jooble renvoie 'X-RateLimit-Remaining' dans les headers
            remaining = response.getheader('X-RateLimit-Remaining', 'Inconnu')
            # -----------------------------

            raw_data = response.read().decode('utf-8')

            if response.status == 200:
                data = json.loads(raw_data)
                
                if "jobs" in data and data["jobs"]:
                    total = data.get('totalCount', len(data["jobs"]))
                    embed = discord.Embed(
                        title=f"💼 {total} offres pour '{keywords}'", 
                        description=f"📍 Secteur : {location}",
                        color=discord.Color.green()
                    )
                    
                    # On ajoute le quota en bas de l'Embed (Footer)
                    embed.set_footer(text=f"Requêtes API restantes : {remaining} / 500")
                    
                    for job in data["jobs"][:5]:
                        title = job.get('title', '').replace("<b>", "").replace("</b>", "")
                        company = job.get('company', 'Inconnue')
                        link = job.get('link', '#')
                        embed.add_field(name=title, value=f"🏢 {company}\n🔗 [Voir l'offre]({link})", inline=False)
                    
                    await interaction.followup.send(embed=embed, ephemeral=True)
                else:
                    await interaction.followup.send(f"❌ Aucun résultat (Quota : {remaining}).", ephemeral=True)
            else:
                await interaction.followup.send(f"⚠️ Erreur Jooble : {response.status}", ephemeral=True)

        except Exception as e:
            print(f"ERREUR : {e}")
            await interaction.followup.send(f"⚠️ Une erreur technique est survenue.", ephemeral=True)
        finally:
            connection.close()

async def setup(bot):
    await bot.add_cog(JoobleCog(bot))
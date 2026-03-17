import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
import asyncio

PAUSES = {
    "10:00": 15,
    "12:00": 60,
    "14:30": 15,
}

class Pause(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.pause_active = False
        self.waiting_confirm = False
        self.pause_channel = None
        self.current_duree = None
        self.already_notified = set() 

    @commands.Cog.listener()
    async def on_ready(self):
        asyncio.create_task(self.scheduler())

    async def scheduler(self):
        while True:
            now = datetime.now().strftime("%H:%M")

            if (now in PAUSES
                and not self.pause_active
                and not self.waiting_confirm
                and now not in self.already_notified
            ):
                self.already_notified.add(now)
                self.waiting_confirm = True
                self.current_duree = PAUSES[now]
                await self.notify_pause(now)

            if now == "00:00":
                self.already_notified.clear()  

            await asyncio.sleep(30)

    async def notify_pause(self, heure):
        if self.pause_channel is None:
            return

        await self.pause_channel.send(
            f"Il est {heure} !\n"
            f"Voulez-vous prendre la pause ? ({self.current_duree} minutes)\n"
            f"Tapez /pause pour confirmer"
        )

    @app_commands.command(name="pause", description="Confirme ou lance la prochaine pause")
    async def pause(self, interaction: discord.Interaction):
        if self.pause_active:
            await interaction.response.send_message("Une pause est déjà en cours.")
            return

        
        if self.waiting_confirm:
            self.waiting_confirm = False
            self.pause_active = True
            heure_debut = datetime.now().strftime("%H:%M")
            await interaction.response.send_message(
                f"@everyone\n"
                f"Pause commencée à {heure_debut} par {interaction.user.mention}"
            )
            await self.start_countdown(interaction.channel, self.current_duree)
            return

        
        now = datetime.now().strftime("%H:%M")
        prochaine = None
        prochaine_duree = None

        for heure, duree in sorted(PAUSES.items()):
            if heure >= now:
                prochaine = heure
                prochaine_duree = duree
                break

        if prochaine is None:
            await interaction.response.send_message("Aucune pause programmée pour le reste de la journée.")
            return

        self.already_notified.add(prochaine)
        self.waiting_confirm = False
        self.pause_active = True
        self.current_duree = prochaine_duree

        heure_debut = datetime.now().strftime("%H:%M")
        await interaction.response.send_message(
            f"@everyone\n"
            f"Pause lancée manuellement à {heure_debut} par {interaction.user.mention}\n"
            f"(Pause de {prochaine} avancée)"
        )
        await self.start_countdown(interaction.channel, prochaine_duree)

    async def start_countdown(self, channel, duree_minutes):
        message = await channel.send(
            f"{duree_minutes} minute(s) restante(s)"
        )

        for minutes_restantes in range(duree_minutes - 1, 0, -1):
            await asyncio.sleep(60)
            await message.edit(content=f"{minutes_restantes} minute(s) restante(s)")

        await asyncio.sleep(60)

        heure_fin = datetime.now().strftime("%H:%M")
        self.pause_active = False  

        await message.edit(content="La pause est terminée.")
        await channel.send(
            f"@everyone\n"
            f"La pause est terminée ! ({heure_fin})\n"
            f"Retour au travail."
        )

    @commands.command()
    async def set_channel(self, ctx):
        self.pause_channel = ctx.channel
        await ctx.send(f"Channel de pause défini sur {ctx.channel.mention}")

    @app_commands.command(name="pause_status", description="Affiche le statut actuel des pauses")
    async def pause_status(self, interaction: discord.Interaction):
        if self.pause_active:
            status = "Pause en cours"
        elif self.waiting_confirm:
            status = f"En attente de /pause ({self.current_duree} min)"
        else:
            status = "Pas de pause en cours"

        await interaction.response.send_message(
            f"Statut : {status}\n"
            f"Pauses programmées : {', '.join(sorted(PAUSES.keys()))}"
        )


async def setup(bot):
    await bot.add_cog(Pause(bot))

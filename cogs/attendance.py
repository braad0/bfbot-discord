from __future__ import annotations

import asyncio
import discord
from discord import app_commands
from discord.ext import commands


class Attendance(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.active_attendance_messages: set[int] = set()

    @app_commands.command(name="attendance", description="Open attendance for the course")
    async def attendance(self, interaction: discord.Interaction) -> None:
        content = (
            "**Présence ouverte**\n"
            "Présence ouverte pour le cours.\n"
            "Vous avez **10 minutes** pour réagir.\n\n"
            "✅ présent\n"
            "⏰ retard\n"
            "❌ absent"
        )

        await interaction.response.send_message(content)
        message = await interaction.original_response()

        await message.add_reaction("✅")
        await message.add_reaction("⏰")
        await message.add_reaction("❌")

        self.active_attendance_messages.add(message.id)
        self.bot.loop.create_task(self.close_attendance_after_delay(message, delay=600))

    async def close_attendance_after_delay(self, message: discord.Message, delay: int = 600) -> None:
        await asyncio.sleep(delay)

        if message.id not in self.active_attendance_messages:
            return

        self.active_attendance_messages.remove(message.id)

        guild = message.guild
        if guild is None:
            await message.channel.send("Impossible de clôturer : ce message n'est pas dans un serveur.")
            return

        refreshed_message = await message.channel.fetch_message(message.id)

        # Cherche le rôle "Stagiaire"
        trainee_role = discord.utils.get(guild.roles, name="Stagiaire")
        if trainee_role is None:
            await message.channel.send("Impossible de clôturer : le rôle **Stagiaire** est introuvable.")
            return

        # Tous les membres du rôle Stagiaire
        trainees = {member.id: member for member in trainee_role.members if not member.bot}

        # Statut par utilisateur
        # priorité choisie : ❌ > ⏰ > ✅
        # comme ça si quelqu'un a plusieurs réactions, on garde le statut le plus "fort"
        statuses: dict[int, str] = {}

        priority = {
            "✅": 1,
            "⏰": 2,
            "❌": 3,
        }

        emoji_to_status = {
            "✅": "présent",
            "⏰": "retard",
            "❌": "absent",
        }

        user_priority: dict[int, int] = {}

        for reaction in refreshed_message.reactions:
            emoji = str(reaction.emoji)
            if emoji not in emoji_to_status:
                continue

            async for user in reaction.users():
                if user.bot:
                    continue

                member = guild.get_member(user.id)
                if member is None:
                    continue

                # On ignore tous ceux qui ne sont pas Stagiaire
                if member.id not in trainees:
                    continue

                new_priority = priority[emoji]
                old_priority = user_priority.get(member.id, 0)

                if new_priority >= old_priority:
                    user_priority[member.id] = new_priority
                    statuses[member.id] = emoji_to_status[emoji]

        presents = []
        lates = []
        absents = []
        no_response = []

        for member_id, member in trainees.items():
            status = statuses.get(member_id)

            if status == "présent":
                presents.append(member.mention)
            elif status == "retard":
                lates.append(member.mention)
            elif status == "absent":
                absents.append(member.mention)
            else:
                no_response.append(member.mention)

        result_message = (
            "**Présence clôturée**\n\n"
            f"✅ **Présents** ({len(presents)}): {', '.join(presents) if presents else 'personne'}\n\n"
            f"⏰ **En retard** ({len(lates)}): {', '.join(lates) if lates else 'personne'}\n\n"
            f"❌ **Absents** ({len(absents)}): {', '.join(absents) if absents else 'personne'}\n\n"
            f"❓ **N'a pas répondu** ({len(no_response)}): {', '.join(no_response) if no_response else 'personne'}"
        )

        await message.channel.send(result_message)

        try:
            await refreshed_message.clear_reactions()
        except discord.Forbidden:
            pass


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Attendance(bot))
import discord  # Importe la bibliothèque Discord pour interagir avec l'API Discord.
import os  # Importe le module os pour interagir avec les variables d'environnement.
import asyncio  # Importe asyncio pour gérer les tâches asynchrones.
from discord.ext import commands  # Importe les commandes de la bibliothèque Discord.
from dotenv import load_dotenv  # Importe load_dotenv pour charger les variables d'environnement depuis un fichier .env.

# Charge les variables d'environnement depuis le fichier .env.
load_dotenv()

# Récupère le token du bot depuis les variables d'environnement.
TOKEN = os.getenv("TOKEN")

# Récupère l'ID du serveur (guild) depuis les variables d'environnement et le convertit en entier.
GUILD_ID = int(os.getenv("GUILD_ID"))


# Définition de la classe Bot qui hérite de commands.Bot.
class Bot(commands.Bot):
    def __init__(self):
        # Définit les intentions du bot (ce qu'il peut écouter et interagir).
        intents = discord.Intents.default()
        intents.message_content = True  # Permet au bot de lire le contenu des messages.
        intents.members = True  # Permet au bot d'accéder aux informations des membres.

        # Initialise la classe parente commands.Bot avec un préfixe de commande.
        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),  # Préfixe des commandes (! ou mention du bot).
            intents=intents  # Passe les intentions définies.
        )

    # Méthode appelée pour configurer le bot avant qu'il ne soit prêt.
    async def setup_hook(self):
        # Charge une extension (cog) appelée "cogs.fun".
        await self.load_extension("cogs.fun")

        # Crée un objet représentant le serveur (guild) avec l'ID spécifié.
        guild = discord.Object(id=GUILD_ID)

        # Copie les commandes globales pour les rendre spécifiques à ce serveur.
        self.tree.copy_global_to(guild=guild)

        # Synchronise les commandes avec le serveur.
        await self.tree.sync(guild=guild)

    # Méthode appelée lorsque le bot est prêt et connecté.
    async def on_ready(self):
        # Affiche un message dans la console indiquant que le bot est connecté.
        print(f"connected as {self.user}")


# Fonction principale pour démarrer le bot.
async def main():
    # Crée une instance de la classe Bot.
    bot = Bot()
    # Démarre le bot avec le token récupéré.
    await bot.start(TOKEN)


# Exécute la fonction main() en tant que tâche asyncio.
asyncio.run(main())

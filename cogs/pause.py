"""
Projet : Commande Pause Bot

Description :
Ce projet consiste à développer un bot qui gère les pauses à des heures spécifiques (10h, 12h, et 14h30). 
L'objectif est de notifier les utilisateurs lorsque la pause commence et de s'assurer qu'elle ne débute que 
lorsqu'un utilisateur confirme avec le message "pause ok". Une fois la pause confirmée, le bot démarre un 
compte à rebours pour la durée de la pause. À la fin de la pause, le bot envoie un message pour indiquer 
que la pause est terminée.

Fonctionnalités principales :
1. Notification automatique des heures de pause (10h, 12h, 14h30).
2. Attente de confirmation par un utilisateur avec le message "pause ok" pour démarrer la pause.
3. Gestion du temps de pause avec un compte à rebours.
4. Notification de fin de pause une fois le temps écoulé.

Exemple de fonctionnement :
- À 10h, le bot envoie : "C'est l'heure de la pause ! Veuillez confirmer avec 'pause ok' pour commencer."
- Un utilisateur répond "pause ok".
- Le bot commence la pause et démarre un compte à rebours.
- À la fin de la pause, le bot envoie : "La pause est terminée ! Retour au travail."

Ce projet peut être implémenté en utilisant un langage comme Python avec une bibliothèque pour les bots 
(discord.py, par exemple) et une gestion des tâches planifiées (comme APScheduler).
"""


from .llm import LLM


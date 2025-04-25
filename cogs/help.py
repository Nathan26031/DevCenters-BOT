import discord
from discord.ext import commands
from discord import app_commands
from typing import List 

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def category_autocomplete(
        # type: ignore
        self, interaction: discord.Interaction, current: str
    ) -> List[app_commands.Choice[str]]:
        categories = ["Aide", "Jeux", "Modération", "Bot"]
        return [
            app_commands.Choice(name=cat, value=cat)
            for cat in categories if current.lower() in cat.lower()
        ]

    @app_commands.command(name="aide", description="Affiche la liste des commandes disponibles.")
    @app_commands.autocomplete(category=category_autocomplete)
    async def aide(self, interaction: discord.Interaction, category: str = None):
        embed = discord.Embed(
            title="📜 Liste des Commandes",
            description="Voici la liste des commandes disponibles.",
            color=discord.Color.blue()
        )

        commandes = {
            "Aide": [
                ("aide", "Affiche cette liste d'aide.")
            ],
            "Jeux": [
                ("dé", "Lance un dé à 6 faces."),
                ("pileouface", "Effectue un tirage de pile ou face."),
                ("addition", "Additionne deux nombres donnés."),
                ("multiplication", "Multiplie deux nombres donnés."),
                ("soustraire", "Soustrait deux nombres donnés."),
            ],
            "Modération": [
                ("kick", "Expulse un membre du serveur avec une raison facultative."),
                ("ban", "Bannit un membre définitivement."),
                ("tempban", "Bannit un membre temporairement."),
                ("mute", "Mute un membre pour une durée définie."),
                ("clear", "Supprime un nombre spécifié de messages."),
                ("repete", "Répète un message un certain nombre de fois."),
                ("unban", "Débannit un utilisateur avec son ID."),
                ("unmute", "Unmute un utilisateur."),
            ],
            "Bot": [
                ("ping", "Affiche la latence du bot."),
            ],
        }

        if category:
            category = category.capitalize()
            if category in commandes:
                embed.add_field(
                    name=f"📌 {category}",
                    value="\n".join([f"**{cmd}** → {desc}" for cmd, desc in commandes[category]]),
                    inline=False
                )
            else:
                embed.color = discord.Color.red()
                embed.add_field(
                    name="❌ Erreur",
                    value=f"La catégorie `{category}` n'existe pas.\nEssayez : `Aide`, `Jeux`, `Modération`, `Bot`.",
                    inline=False
                )
        else:
            for cat, cmds in commandes.items():
                embed.add_field(
                    name=f"📌 {cat}",
                    value="\n".join([f"**{cmd}** → {desc}" for cmd, desc in cmds]),
                    inline=False
                )

        embed.set_footer(text="Utilisez ' / ' avant chaque commande pour l'exécuter.")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
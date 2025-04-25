import random
import discord
from discord.ext import commands
from discord import app_commands

class GamesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="dé", description="Lance un dé à 6 faces et affiche le résultat.")
    async def dé(self, interaction: discord.Interaction):
        result = random.randint(1, 6)
        embed = discord.Embed(
            title="Lancer de dé 🎲",
            description=f"**{interaction.user.name} lance un dé et obtient :** {result}",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="pileouface", description="Effectue un tirage de pile ou face et affiche le résultat.")
    async def pileouface(self, interaction: discord.Interaction):
        result = random.choice(["pile", "face"])
        embed = discord.Embed(
            title="Tirage Pile ou Face  🪙",
            description=f"**Résultat obtenu :** {result}",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="addition", description="Effectue l'addition de deux nombres et affiche le résultat.")
    async def addition(self, interaction: discord.Interaction, a: int, b: int):
        result = a + b
        embed = discord.Embed(
            title="Addition ➕",
            description=f"**{a} + {b} =** {result}",
            color=discord.Color.orange()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="soustraire", description="Effectue la soustraction de deux nombres et affiche le résultat.")
    async def soustraire(self, interaction: discord.Interaction, a: int, b: int):
        result = a - b
        embed = discord.Embed(
            title="Soustraction ➖",
            description=f"**{a} - {b} =** {result}",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="multiplication", description="Effectue la multiplication de deux nombres et affiche le résultat.")
    async def multiplication(self, interaction: discord.Interaction, a: int, b: int):
        result = a * b
        embed = discord.Embed(
            title="Multiplication ✖️",
            description=f"**{a} x {b} =** {result}",
            color=discord.Color.yellow()
        )
        await interaction.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if self.bot.user.mentioned_in(message):
            embed = discord.Embed(
                title="Réponse automatique ⚡",
                description="**Quoi 😠 ???!!!??**",
                color=discord.Color.red()
            )
            await message.reply(embed=embed, mention_author=True)
        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(GamesCog(bot))
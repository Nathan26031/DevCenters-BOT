import discord
from discord import app_commands
from discord.ext import commands
from discord import Embed

class Bot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="ping", description="Affiche la latence du bot")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000) 
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latence du bot: `{latency}ms`",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)

    @commands.Cog.listener() 
    async def on_ready(self):
        
        owner = self.bot.get_user(1316068882154393693) 
        if owner:
            embed = Embed(
                title="Redémarrage du bot",
                description="Le bot a été redémarré avec succès et est de retour en ligne !",
                color=0x00FF00 
            )
            await owner.send(embed=embed)
            print("Le bot a été redémarré avec succès et est de retour en ligne !")

async def setup(bot: commands.Bot):
    if not bot.get_cog("Bot"):
      await bot.add_cog(Bot(bot))
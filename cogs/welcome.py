import discord
from discord.ext import commands

class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()  
    async def on_member_join(self, member):
        channel = self.bot.get_channel(1343953435976007730)
        if channel:
            embed = discord.Embed(
                title="Bienvenue !",
                description=f"🎉 Bienvenue {member.mention} sur le serveur ! 🌟 Pose tes valises, prends un cookie et installe-toi bien ! 🍪",
                color=discord.Color.blue()
            )
            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(WelcomeCog(bot))
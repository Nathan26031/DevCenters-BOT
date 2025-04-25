import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from keep_alive import keep_alive

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

class MonBot(commands.Bot):
    async def setup_hook(self):
      for extension in ['games', 'moderation', 'help', 'bot', 'welcome']:
        await self.load_extension(f"cogs.{extension}")

intents = discord.Intents.all()
bot = MonBot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} commande(s) synchronisée(s)")
    except Exception as e:
        print(e)
    activity = discord.Streaming(name="VS Code", url="https://twitch.tv/nathan260300")
    await bot.change_presence(status=discord.Status.dnd, activity=activity)
    print('Statut mis à jour')

keep_alive()
bot.run(token=token)
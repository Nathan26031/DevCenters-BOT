import asyncio
import discord
from discord.ext import commands
from discord import app_commands

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="kick", description="Kick un membre du serveur avec une raison facultative.")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = None):
      if member.top_role >= interaction.user.top_role:
        embed = discord.Embed(
            title="Action impossible 🚫",
            description="Tu ne peux pas kick cette personne, car elle a un rôle supérieur ou égal au tien.",
            color=discord.Color.orange()
        )
        await interaction.response.send_message(embed=embed)
        return

      if any(role.permissions.administrator for role in member.roles):
          embed = discord.Embed(
              title="Action impossible 🚫",
              description=f"Tu ne peux pas kicker {member.name}, car il/elle est un membre du staff.",
              color=discord.Color.orange()
        )
          await interaction.response.send_message(embed=embed)
          return

      embed = discord.Embed(
          title="Action de Kick 🚫",
          description=f"**{member.name}** a été kické du serveur.",
          color=discord.Color.red()
      )
      embed.add_field(name="Raison", value=reason or "Aucune raison spécifiée.", inline=False)
      embed.set_footer(text=f"Action effectuée par {interaction.user.name}")

      await interaction.response.send_message(embed=embed)

      pm_embed = discord.Embed(
          title="Tu as été kické du serveur ⚠️",
          description=f"Salut {member.name},\n\nTu as été kické du serveur {interaction.guild.name}.",
          color=discord.Color.red()
      )
      pm_embed.add_field(name="Raison", value=reason or "Aucune raison spécifiée.", inline=False)

      try:
          await member.send(embed=pm_embed)
      except discord.errors.Forbidden:
          await interaction.followup.send(f"Impossible d'envoyer un message privé à {member.name}. Il/Elle a peut-être désactivé les MP.")

    @kick.error
    async def kick_error(self, interaction: discord.Interaction, error):
      if isinstance(error, commands.MissingPermissions):
          await interaction.response.send_message("Tu n'as pas la permission de kicker des membres.")
      elif isinstance(error, commands.MissingRequiredArgument):
          await interaction.response.send_message("Tu dois spécifier un membre à kicker.")
      else:
          await interaction.response.send_message("Une erreur est survenue.")


    @app_commands.command(name="clear", description="Supprime un nombre de messages spécifié.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, nombre: int):
    
      if nombre <= 0:
          await interaction.response.send_message("**Veuillez entrer un nombre valide de messages à supprimer.**", ephemeral=True)
          return
    
      if nombre > 100:
          await interaction.response.send_message("**Le nombre de messages à supprimer ne peut pas dépasser 100.**", ephemeral=True)
          return
    
      deleted = await interaction.channel.purge(limit=nombre)
    
      if len(deleted) == 0:
          await interaction.response.send_message("**Aucun message à supprimer.**", ephemeral=True)
          return
      
      confirmation_msg = await interaction.channel.send(f"**{len(deleted)} messages supprimés.**")
      await asyncio.sleep(2) 
      await confirmation_msg.delete()
    
      if interaction.message:
          try:
              await interaction.message.delete()
          except discord.errors.NotFound:
              pass 
  
    @app_commands.command(name="repete", description="Répète un message un nombre spécifié de fois.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def repete(self, interaction: discord.Interaction, nombre: int, message: str):
        await interaction.response.send_message(message)
        for _ in range(1, nombre):
            await interaction.channel.send(message)
    
    @repete.error
    async def repete_error(self, interaction: discord.Interaction, error: Exception):
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message("**Vous n'avez pas la permission d'exécuter cette commande.**", delete_after=5)
        
    @app_commands.command(name="ban", description="Bannit un membre définitivement du serveur.")
    @app_commands.checks.has_permissions(ban_members=True)  
    async def ban(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = "Aucune raison spécifiée"):
        """Commande pour bannir un membre avec une raison"""
        if interaction.user == member:
            await interaction.response.send_message("❌ **Vous ne pouvez pas vous bannir vous-même !**", delete_after=5)
            return
        if interaction.guild.owner_id == member.id:
            await interaction.response.send_message("❌ **Vous ne pouvez pas bannir le propriétaire du serveur !**", delete_after=5)
            return
        if interaction.user.top_role <= member.top_role:
            await interaction.response.send_message("❌ **Vous ne pouvez pas bannir un membre ayant un rôle égal ou supérieur au vôtre !**", delete_after=5)
            return
        try:
            await member.ban(reason=reason)
            await interaction.response.send_message(f"✅ **{member.mention} a été banni pour la raison :** {reason}")
        except discord.errors.Forbidden:
            await interaction.response.send_message("❌ **Je n'ai pas la permission de bannir ce membre.**", delete_after=5)

    @ban.error
    async def ban_error(self, interaction: discord.Interaction, error: Exception):
        """Gestion des erreurs pour la commande ban"""
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message("🚫 **Vous n'avez pas la permission de bannir des membres !**", delete_after=5)
        elif isinstance(error, commands.MissingRequiredArgument):
            await interaction.response.send_message("⚠ **Veuillez mentionner un membre à bannir.**\nExemple : `/ban @membre raison`", delete_after=5)
        elif isinstance(error, commands.BadArgument):
            await interaction.response.send_message("⚠ **Membre introuvable. Veuillez mentionner un utilisateur valide.**", delete_after=5)
    
    @app_commands.command(name="tempban", description="Bannit un membre temporairement du serveur et l'informe en DM.")
    @app_commands.checks.has_permissions(ban_members=True)  
    async def tempban(self, interaction: discord.Interaction, member: discord.Member, duration: int, unit: str, *, reason: str = "Aucune raison spécifiée"):
        """
        Commande pour bannir temporairement un membre en lui envoyant un message privé.
        Usage : /tempban @membre 10 m "Raison"
        """
        if interaction.user == member:
            await interaction.response.send_message("❌ **Vous ne pouvez pas vous bannir vous-même !**", delete_after=5)
            return
        if interaction.guild.owner_id == member.id:
            await interaction.response.send_message("❌ **Vous ne pouvez pas bannir le propriétaire du serveur !**", delete_after=5)
            return
        if interaction.user.top_role <= member.top_role:
            await interaction.response.send_message("❌ **Vous ne pouvez pas bannir un membre ayant un rôle égal ou supérieur au vôtre !**", delete_after=5)
            return
        time_multiplier = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        if unit not in time_multiplier:
            await interaction.response.send_message("⚠ **Unité de temps invalide !** Utilisez `s` (secondes), `m` (minutes), `h` (heures), ou `d` (jours).", delete_after=5)
            return
        ban_time = duration * time_multiplier[unit]
        try:
            embed_dm = discord.Embed(
                title="🚨 Bannissement Temporaire",
                description=f"Vous avez été **temporairement banni** du serveur `{interaction.guild.name}`.",
                color=discord.Color.red()
            )
            embed_dm.add_field(name="⏳ Durée", value=f"{duration}{unit}", inline=True)
            embed_dm.add_field(name="📌 Raison", value=reason, inline=True)
            embed_dm.add_field(name="🔓 Déban automatique", value="Oui", inline=True)
            embed_dm.set_footer(text="Respectez les règles du serveur pour éviter d'autres sanctions.")
            await member.send(embed=embed_dm)
            dm_sent = True
        except discord.Forbidden:
            dm_sent = False
        try:
            await member.ban(reason=f"Tempban ({duration}{unit}) - {reason}")
            confirmation_msg = f"✅ **{member.mention} a été banni pour {duration}{unit} !** Raison : {reason}"
            if not dm_sent:
                confirmation_msg += "\n⚠ **Je n'ai pas pu lui envoyer un message privé.**"
            await interaction.response.send_message(confirmation_msg)
            await asyncio.sleep(ban_time)
            await interaction.guild.unban(member)
            await interaction.response.send_message(f"🔓 **{member.mention} a été débanni après {duration}{unit}.**")
        except discord.errors.Forbidden:
            await interaction.response.send_message("❌ **Je n'ai pas la permission de bannir ce membre.**", delete_after=5)

    @tempban.error
    async def tempban_error(self, interaction: discord.Interaction, error: Exception):
        """Gestion des erreurs pour la commande tempban"""
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message("🚫 **Vous n'avez pas la permission de bannir des membres !**", delete_after=5)
        elif isinstance(error, commands.MissingRequiredArgument):
            await interaction.response.send_message("⚠ **Veuillez mentionner un membre et une durée valide.**\nExemple : `/tempban @membre 10 m \"Raison\"`", delete_after=5)
        elif isinstance(error, commands.BadArgument):
            await interaction.response.send_message("⚠ **Membre introuvable. Veuillez mentionner un utilisateur valide.**", delete_after=5)

    @app_commands.command(name="mute", description="Réduit au silence un membre pour une durée définie.")
    @app_commands.checks.has_permissions(manage_roles=True) 
    async def mute(self, interaction: discord.Interaction, member: discord.Member, duration: int, unit: str, *, reason: str = "Aucune raison spécifiée"):
        """
        Commande pour rendre un membre muet temporairement.
        Usage : /mute @membre 10 m "Spam"
        """
        if interaction.user == member:
            await interaction.response.send_message("❌ **Vous ne pouvez pas vous mute vous-même !**", delete_after=5)
            return
        if interaction.guild.owner_id == member.id:
            await interaction.response.send_message("❌ **Vous ne pouvez pas mute le propriétaire du serveur !**", delete_after=5)
            return
        if interaction.user.top_role <= member.top_role:
            await interaction.response.send_message("❌ **Vous ne pouvez pas mute un membre ayant un rôle égal ou supérieur au vôtre !**", delete_after=5)
            return
        time_multiplier = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        if unit not in time_multiplier:
            await interaction.response.send_message("⚠ **Unité de temps invalide !** Utilisez `s` (secondes), `m` (minutes), `h` (heures), ou `d` (jours).", delete_after=5)
            return
        mute_time = duration * time_multiplier[unit]
        muted_role = discord.utils.get(interaction.guild.roles, name="Mute")
        if not muted_role:
            try:
                muted_role = await interaction.guild.create_role(name="Mute", reason="Création du rôle pour la commande mute")
                for channel in interaction.guild.channels:
                    await channel.set_permissions(muted_role, send_messages=False, speak=False)
            except discord.Forbidden:
                await interaction.response.send_message("❌ **Je n'ai pas la permission de créer/modifier des rôles !**", delete_after=5)
                return
        if muted_role in member.roles:
            await interaction.response.send_message(f"⚠ **{member.mention} est déjà mute !**", delete_after=5)
            return
        try:
            embed_dm = discord.Embed(
                title="🔇 Mute Temporaire",
                description=f"Vous avez été **mute temporairement** sur `{interaction.guild.name}`.",
                color=discord.Color.orange()
            )
            embed_dm.add_field(name="⏳ Durée", value=f"{duration}{unit}", inline=True)
            embed_dm.add_field(name="📌 Raison", value=reason, inline=True)
            embed_dm.add_field(name="🔓 Unmute automatique", value="Oui", inline=True)
            embed_dm.set_footer(text="Respectez les règles du serveur pour éviter d'autres sanctions.")
            await member.send(embed=embed_dm)
            dm_sent = True
        except discord.Forbidden:
            dm_sent = False
        await member.add_roles(muted_role, reason=reason)
        await interaction.response.send_message(f"✅ **{member.mention} est mute pour {duration}{unit}. Raison :** {reason}")
        await asyncio.sleep(mute_time)
        await member.remove_roles(muted_role, reason="Fin du mute temporaire")
        await interaction.response.send_message(f"🔓 **{member.mention} n'est plus mute après {duration}{unit}.**")
    
    @mute.error
    async def mute_error(self, interaction: discord.Interaction, error: Exception):
        """Gestion des erreurs pour la commande mute"""
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message("🚫 **Vous n'avez pas la permission de mute des membres !**", delete_after=5)
        elif isinstance(error, commands.MissingRequiredArgument):
            await interaction.response.send_message("⚠ **Veuillez mentionner un membre et une durée valide.**\nExemple : `/mute @membre 10 m \"Raison\"`", delete_after=5)
        elif isinstance(error, commands.BadArgument):
            await interaction.response.send_message("⚠ **Membre introuvable. Veuillez mentionner un utilisateur valide.**", delete_after=5)

    @app_commands.command(name="unban", description="Débannit un utilisateur avec son ID.")
    @app_commands.describe(user_id="ID de l'utilisateur à débannir")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user_id: str):
        """Débannit un utilisateur et lui envoie un MP"""
        try:
            user_id = int(user_id)  
            user = await self.bot.fetch_user(user_id) 
            await interaction.guild.unban(user) 
            embed = discord.Embed(
                title="🔓 Unban réussi",
                description=f"**{user.name}** a été débanni avec succès !",
                color=discord.Color.green()
            )
            embed.set_footer(text=f"Unban effectué par {interaction.user}", icon_url=interaction.user.avatar.url)

            await interaction.response.send_message(embed=embed)

            try:
                mp_embed = discord.Embed(
                    title="🔓 Vous avez été débanni",
                    description=f"Vous avez été débanni du serveur **{interaction.guild.name}**.\nMerci de respecter les règles si vous revenez.",
                    color=discord.Color.green()
                )
                await user.send(embed=mp_embed)
            except discord.Forbidden:
                await interaction.followup.send(f"⚠️ Impossible d'envoyer un MP à {user.name}.")

        except ValueError:
            await interaction.response.send_message(embed=discord.Embed(
                title="❌ Erreur",
                description="L'ID fourni n'est pas valide. Assurez-vous de copier un ID correct.",
                color=discord.Color.red()
            ))
        except discord.NotFound:
            await interaction.response.send_message(embed=discord.Embed(
                title="❌ Erreur",
                description="L'utilisateur avec cet ID n'existe pas ou n'est pas banni.",
                color=discord.Color.red()
            ))
        except discord.Forbidden:
            await interaction.response.send_message(embed=discord.Embed(
                title="❌ Permission insuffisante",
                description="Je n'ai pas la permission de débannir cet utilisateur.",
                color=discord.Color.red()
            ))
        except discord.HTTPException:
            await interaction.response.send_message(embed=discord.Embed(
                title="❌ Erreur de Discord",
                description="Une erreur s'est produite lors du débannissement.",
                color=discord.Color.red()
            ))

    @app_commands.command(name="unmute", description="Unmute un utilisateur.")
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        """Commande pour unmute un utilisateur."""
        if member.guild.get_member(member.id).guild_permissions.administrator:
            await interaction.response.send_message("Je ne peux pas unmute un administrateur.")
            return

        await member.edit(mute=False)

        embed = discord.Embed(
            title="Utilisateur Unmute",
            description=f"{member.mention} a été unmuté avec succès.",
            color=discord.Color.green()
        )
        embed.set_footer(text="Bot créé par [Ton Nom]")

        await interaction.response.send_message(embed=embed)

        try:
            await member.send(
                embed=discord.Embed(
                    title="Tu as été unmuté",
                    description="Tu as été unmuté sur le serveur.",
                    color=discord.Color.green()
                )
            )
        except discord.Forbidden:
            await interaction.response.send_message(f"Impossible d'envoyer un message privé à {member.mention}.")

async def setup(bot):
    await bot.add_cog(ModerationCog(bot))
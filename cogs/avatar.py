import discord
from discord import app_commands
from discord.ext import commands

class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Slash-Command: /avatar
    @app_commands.command(name="avatar", description="Zeigt den Avatar eines Benutzers an.")
    @app_commands.describe(
        user="Der Benutzer, dessen Avatar angezeigt werden soll."
    )
    async def avatar(self, interaction: discord.Interaction, user: discord.User = None):
        # Standardmäßig den Avatar des Befehlsausführenden anzeigen
        if user is None:
            user = interaction.user

        # Avatar-URL holen
        avatar_url = user.avatar.url if user.avatar else user.default_avatar.url

        # Embed erstellen
        embed = discord.Embed(
            title=f"Avatar von {user.name}",
            color=discord.Color.blue()
        )
        embed.set_image(url=avatar_url)
        embed.add_field(name="Download", value=f"[Hier klicken]({avatar_url})", inline=False)

        # Embed senden
        await interaction.response.send_message(embed=embed)

# Cog für den Bot registrieren
async def setup(bot):
    await bot.add_cog(Avatar(bot))
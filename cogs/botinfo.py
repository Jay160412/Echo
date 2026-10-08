import discord
from discord import app_commands
from discord.ext import commands
import datetime

class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Slash-Command: /botinfo
    @app_commands.command(name="botinfo", description="Zeigt Informationen über den Bot an.")
    async def botinfo(self, interaction: discord.Interaction):
        # Bot-Informationen sammeln
        guild_count = len(self.bot.guilds)  # Anzahl der Server
        command_count = len(self.bot.tree.get_commands())  # Anzahl der Befehle
        bot_created_at = self.bot.user.created_at.strftime("%d.%m.%Y %H:%M:%S")  # Erstellungsdatum
        bot_developer = "Jay_160412"  # Entwickler des Bots (ersetze dies mit deinem Namen)

        # Embed erstellen
        embed = discord.Embed(
            title="🤖 Bot-Informationen",
            description="Hier sind einige Informationen über den Bot:",
            color=discord.Color.blue()
        )
        embed.add_field(name="🖥️ Server", value=f"**{guild_count}**", inline=True)
        embed.add_field(name="📜 Befehle", value=f"**{command_count}**", inline=True)
        embed.add_field(name="📅 Erstellt am", value=f"**{bot_created_at}**", inline=False)
        embed.add_field(name="👨‍💻 Entwickler", value=f"**{bot_developer}**", inline=True)
        embed.set_thumbnail(url=self.bot.user.avatar.url)  # Bot-Avatar

        # Embed senden
        await interaction.response.send_message(embed=embed)

# Cog für den Bot registrieren
async def setup(bot):
    await bot.add_cog(BotInfo(bot))
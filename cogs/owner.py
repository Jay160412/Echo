import discord
from discord import app_commands
from discord.ext import commands

class OwnerInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="owner", description="Zeigt Informationen über den Bot-Besitzer an.")
    async def owner(self, interaction: discord.Interaction):
        # Informationen über den Owner
        owner = await self.bot.fetch_user(1254398312312868945)  # Ersetze DEINE_OWNER_ID durch die tatsächliche ID des Owners

        # Embed erstellen
        embed = discord.Embed(
            title="👑 Bot-Besitzer Informationen",
            description="Hier sind einige Informationen über den Besitzer des Bots:",
            color=discord.Color.blue()
        )

        # Name und Profilbild
        embed.set_author(name=owner.name, icon_url=owner.avatar.url)
        embed.set_thumbnail(url=owner.avatar.url)

        # Server-Links
        embed.add_field(
            name="🔗 Server",
            value=(
                "[Server 1](https://discord.com/invite/V4PJbRWRX5)\n"
                "[Server 2](https://discord.com/invite/qEysQUGStr)"
            ),
            inline=False
        )

        # YouTube-Link
        embed.add_field(
            name="🎥 YouTube (gelöscht)",
            value="[@Jay_YT_real](https://youtube.com/@jay_yt_real?si=BaorJE-yLDDT1se9)",
            inline=False
        )

        # TikTok-Link
        embed.add_field(
            name="📱 TikTok",
            value="[@Jay__tiktok](https://www.tiktok.com/@jay__tiktok?_t=ZN-8utLlIMHBbS&_r=1)",
            inline=False
        )

        # Website
        embed.add_field(
            name="🌐 Website",
            value="[Webseite](https://jaywebsite.vercel.app)",
            inline=False
        )

        # Weitere Informationen
        embed.add_field(
            name="ℹ️ Weitere Infos",
            value="Falls du Fragen hast, kontaktiere mich gerne auf einem der oben genannten Server!",
            inline=False
        )

        # Embed senden
        await interaction.response.send_message(embed=embed)

# Cog für den Bot registrieren
async def setup(bot: commands.Bot):
    await bot.add_cog(OwnerInfo(bot))
import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import random

class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Slash-Command: /meme
    @app_commands.command(name="meme", description="Zeigt ein zufälliges Meme an.")
    async def meme(self, interaction: discord.Interaction):
        # Meme von einer API holen (z. B. Reddit)
        async with aiohttp.ClientSession() as session:
            async with session.get("https://meme-api.com/gimme") as response:
                if response.status == 200:
                    data = await response.json()
                    meme_url = data["url"]
                    meme_title = data["title"]
                    meme_author = data["author"]

                    # Embed erstellen
                    embed = discord.Embed(
                        title=meme_title,
                        color=discord.Color.blue()
                    )
                    embed.set_image(url=meme_url)
                    embed.set_footer(text=f"Von u/{meme_author} auf Reddit")

                    # Embed senden
                    await interaction.response.send_message(embed=embed)
                else:
                    await interaction.response.send_message("Konnte kein Meme laden. 😢", ephemeral=True)

# Cog für den Bot registrieren
async def setup(bot):
    await bot.add_cog(Meme(bot))
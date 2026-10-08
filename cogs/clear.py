import discord
from discord import app_commands
from discord.ext import commands

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Slash-Command: /clear
    @app_commands.command(name="clear", description="Löscht eine bestimmte Anzahl von Nachrichten im aktuellen Kanal.")
    @app_commands.describe(
        amount="Die Anzahl der Nachrichten, die gelöscht werden sollen (0-100)."
    )
    async def clear(self, interaction: discord.Interaction, amount: int):
        # Überprüfen, ob der Benutzer die Berechtigung zum Löschen von Nachrichten hat
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("Du hast keine Berechtigung, Nachrichten zu löschen.", ephemeral=True)
            return

        # Überprüfen, ob die Anzahl gültig ist (0-100)
        if amount < 0 or amount > 100:
            await interaction.response.send_message("Die Anzahl muss zwischen 0 und 100 liegen.", ephemeral=True)
            return

        # Nachrichten löschen
        channel = interaction.channel
        try:
            deleted = await channel.purge(limit=amount + 1)  # +1, um den Befehl selbst zu löschen
            await interaction.response.send_message(f"🗑️ {len(deleted) - 1} Nachrichten wurden gelöscht.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("Ich habe keine Berechtigung, Nachrichten in diesem Kanal zu löschen.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"Fehler beim Löschen der Nachrichten: {e}", ephemeral=True)

# Cog für den Bot registrieren
async def setup(bot):
    await bot.add_cog(Clear(bot))
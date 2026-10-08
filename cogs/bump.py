import discord
from discord import app_commands, ui
from discord.ext import commands
import json
import os
from typing import Dict

# Pfad zur Konfigurationsdatei
CONFIG_PATH = "./data/bump_config.json"

# Funktion zum Laden der Konfiguration
def load_config() -> Dict[str, Dict[str, int]]:
    if not os.path.exists(CONFIG_PATH):
        return {}
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

# Funktion zum Speichern der Konfiguration
def save_config(config: Dict[str, Dict[str, int]]):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

class Bump(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = load_config()

    # Slash-Command: /bump
    @app_commands.command(name="bump", description="Legt die Kanäle für das Bump-System fest.")
    @app_commands.describe(
        bump_channel="Der Kanal, in dem der Bump-Button angezeigt wird.",
        ad_channel="Der Kanal, in dem Werbung gepostet wird."
    )
    async def bump(self, interaction: discord.Interaction, bump_channel: discord.TextChannel, ad_channel: discord.TextChannel):
        # Überprüfen, ob der Benutzer Administratorrechte hat
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Du hast keine Berechtigung, dies zu tun.", ephemeral=True)
            return

        guild_id = str(interaction.guild.id)
        self.config[guild_id] = {
            "bump_channel_id": bump_channel.id,
            "ad_channel_id": ad_channel.id
        }
        save_config(self.config)

        # Nachricht mit Bump-Button senden
        view = ui.View()
        view.add_item(ui.Button(style=discord.ButtonStyle.primary, label="Bump", custom_id="bump_button"))

        await bump_channel.send("Klicke auf den Button, um deinen Server zu bewerben!", view=view)
        await interaction.response.send_message(
            f"✅ Bump-System aktiviert!\n"
            f"**Bump-Kanal:** {bump_channel.mention}\n"
            f"**Werbungskanal:** {ad_channel.mention}"
        )

    # Event: Wenn ein Button geklickt wird
    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type == discord.InteractionType.component:
            custom_id = interaction.data.get("custom_id")
            if custom_id == "bump_button":
                await self.handle_bump(interaction)

    # Funktion: Bump verarbeiten
    async def handle_bump(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild.id)
        if guild_id not in self.config:
            await interaction.response.send_message("Das Bump-System ist nicht korrekt konfiguriert.", ephemeral=True)
            return

        # Werbung in allen Servern posten
        for other_guild_id, config in self.config.items():
            if other_guild_id == guild_id:
                continue  # Ignoriere den eigenen Server

            ad_channel = self.bot.get_channel(config["ad_channel_id"])
            if ad_channel:
                try:
                    invite = await interaction.guild.text_channels[0].create_invite(max_age=300)
                    await ad_channel.send(
                        f"🚀 **Neue Werbung von {interaction.guild.name}**\n"
                        f"🔗 {invite.url}"
                    )
                except Exception as e:
                    print(f"Fehler beim Erstellen der Einladung oder Senden der Nachricht: {e}")

        await interaction.response.send_message("✅ Dein Server wurde erfolgreich beworben!", ephemeral=True)

# Cog für den Bot registrieren
async def setup(bot: commands.Bot):
    await bot.add_cog(Bump(bot))
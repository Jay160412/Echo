import discord

from discord.ext import commands

from discord import app_commands

import json

import os
import logging

from typing import Optional

# Pfad zur Konfigurationsdatei

CONFIG_PATH = "./data/autoreaction_config.json"

def load_config():

    if not os.path.exists(CONFIG_PATH):

        return {}

    with open(CONFIG_PATH, "r") as f:

        raw_config = json.load(f)

    if not isinstance(raw_config, dict):
        raise ValueError("AutoReaction-Konfiguration muss ein JSON-Objekt sein")

    normalized = {}
    for guild_id, settings in raw_config.items():
        if not isinstance(settings, dict):
            continue

        enabled = settings.get("enabled", True) is not False
        channels = {}

        # Älteres Format: {channel_id, emoji, enabled} direkt im Serverobjekt.
        legacy_channel = str(settings.get("channel_id", "")).strip()
        legacy_emoji = settings.get("emoji")
        if enabled and legacy_channel.isdigit() and isinstance(legacy_emoji, str) and legacy_emoji.strip():
            channels[legacy_channel] = legacy_emoji.strip()

        # Unterstützt auch bereits verschachtelte und frühere flache Formate.
        nested_channels = settings.get("channels")
        if isinstance(nested_channels, dict):
            for channel_id, emoji in nested_channels.items():
                channel_id = str(channel_id)
                if channel_id.isdigit() and isinstance(emoji, str) and emoji.strip():
                    channels[channel_id] = emoji.strip()

        for channel_id, emoji in settings.items():
            channel_id = str(channel_id)
            if channel_id.isdigit() and isinstance(emoji, str) and emoji.strip():
                channels[channel_id] = emoji.strip()

        normalized[str(guild_id)] = {"enabled": enabled, "channels": channels}

    if normalized != raw_config:
        backup_path = f"{CONFIG_PATH}.legacy-backup"
        if not os.path.exists(backup_path):
            with open(backup_path, "w") as backup:
                json.dump(raw_config, backup, indent=4)
        save_config(normalized)

    return normalized

def save_config(config):

    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)

    with open(CONFIG_PATH, "w") as f:

        json.dump(config, f, indent=4)

class AutoReaction(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.config = load_config()

    @app_commands.command(name="setautoreaction", description="Aktiviert automatische Reaktionen in Kanälen")

    @app_commands.describe(

        channel1="Erster Kanal",

        reaction1="Erste Reaktion (Emoji)",

        channel2="Zweiter Kanal (optional)",

        reaction2="Zweite Reaktion (optional)",

        channel3="Dritter Kanal (optional)",

        reaction3="Dritte Reaktion (optional)"

    )

    @app_commands.checks.has_permissions(administrator=True)

    async def setautoreaction(

        self, 

        interaction: discord.Interaction,

        channel1: discord.TextChannel,

        reaction1: str,

        channel2: Optional[discord.TextChannel] = None,

        reaction2: Optional[str] = None,

        channel3: Optional[discord.TextChannel] = None,

        reaction3: Optional[str] = None

    ):

        guild = interaction.guild
        if guild is None:
            return await interaction.response.send_message(
                "Dieser Befehl funktioniert nur auf einem Server.",
                ephemeral=True,
            )

        bot_member = guild.me
        if bot_member is None:
            return await interaction.response.send_message(
                "Die Bot-Mitgliedsdaten konnten für diesen Server nicht geladen werden.",
                ephemeral=True,
            )

        pairs = [
            (channel1, reaction1),
            (channel2, reaction2),
            (channel3, reaction3),
        ]
        if any((channel is None) != (reaction is None) for channel, reaction in pairs):
            return await interaction.response.send_message(
                "Gib für jeden optionalen Kanal auch eine Reaktion an – oder lasse beide Felder leer.",
                ephemeral=True,
            )

        configured = []
        for channel, reaction in pairs:
            if channel is None:
                continue
            reaction = reaction.strip()
            if not reaction:
                return await interaction.response.send_message(
                    f"Für {channel.mention} fehlt ein Emoji.",
                    ephemeral=True,
                )

            permissions = channel.permissions_for(bot_member)
            missing = [
                label
                for label, allowed in (
                    ("Kanal ansehen", permissions.view_channel),
                    ("Nachrichtenverlauf ansehen", permissions.read_message_history),
                    ("Reaktionen hinzufügen", permissions.add_reactions),
                )
                if not allowed
            ]
            if missing:
                return await interaction.response.send_message(
                    f"Dem Bot fehlen in {channel.mention} diese Berechtigungen: {', '.join(missing)}.",
                    ephemeral=True,
                )
            configured.append((channel, reaction))

        guild_id = str(guild.id)
        settings = self.config.setdefault(guild_id, {"enabled": True, "channels": {}})
        settings["enabled"] = True
        channel_config = settings.setdefault("channels", {})
        for channel, reaction in configured:
            channel_config[str(channel.id)] = reaction

        save_config(self.config)

        

        # Antwort erstellen

        channels_list = [f"{channel.mention} → {reaction}" for channel, reaction in configured]

        

        embed = discord.Embed(

            title="✅ Auto-Reaktion aktiviert",

            description="\n".join(channels_list),

            color=discord.Color.green()

        )

        

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="resetautoreaction", description="Deaktiviert automatische Reaktionen in einem Kanal")

    @app_commands.describe(channel="Der Kanal, in dem die Auto-Reaktion deaktiviert werden soll")

    @app_commands.checks.has_permissions(administrator=True)

    async def resetautoreaction(self, interaction: discord.Interaction, channel: discord.TextChannel):

        guild_id = str(interaction.guild.id)

        

        if interaction.guild is None:
            return await interaction.response.send_message(
                "Dieser Befehl funktioniert nur auf einem Server.",
                ephemeral=True,
            )

        guild_id = str(interaction.guild.id)
        settings = self.config.get(guild_id, {})
        channels = settings.get("channels", {})
        if str(channel.id) in channels:
            del channels[str(channel.id)]
            if not channels:
                self.config.pop(guild_id, None)
            save_config(self.config)
            await interaction.response.send_message(f"✅ Auto-Reaktion in {channel.mention} deaktiviert")

        else:

            await interaction.response.send_message(f"❌ In {channel.mention} ist keine Auto-Reaktion aktiv", ephemeral=True)

    @app_commands.command(name="autoreactionlist", description="Zeigt alle aktiven Auto-Reaktionen an")

    async def autoreactionlist(self, interaction: discord.Interaction):

        if interaction.guild is None:
            return await interaction.response.send_message(
                "Dieser Befehl funktioniert nur auf einem Server.",
                ephemeral=True,
            )

        guild_id = str(interaction.guild.id)

        

        settings = self.config.get(guild_id, {})
        channels = settings.get("channels", {})
        if not channels:

            return await interaction.response.send_message("❌ Keine aktiven Auto-Reaktionen auf diesem Server", ephemeral=True)

        

        embed = discord.Embed(

            title="🤖 Auto-Reaktionen",

            color=discord.Color.blue()

        )

        

        total = 0
        bot_member = interaction.guild.me

        for channel_id, emoji in channels.items():

            if not str(channel_id).isdigit():
                continue

            channel = interaction.guild.get_channel(int(channel_id))

            if channel:

                missing_permissions = []
                if bot_member is not None:
                    permissions = channel.permissions_for(bot_member)
                    if not permissions.view_channel:
                        missing_permissions.append("Kanal ansehen")
                    if not permissions.read_message_history:
                        missing_permissions.append("Nachrichtenverlauf")
                    if not permissions.add_reactions:
                        missing_permissions.append("Reaktionen hinzufügen")
                status = (
                    f"❌ Fehlende Rechte: {', '.join(missing_permissions)}"
                    if missing_permissions
                    else "✅ Bot-Berechtigungen vorhanden"
                )

                embed.add_field(

                    name=f"#{channel.name}",

                    value=f"Reaktion: {emoji}\n{status}",

                    inline=False

                )

                total += 1

        

        active = settings.get("enabled", True)
        if not active:
            embed.description = "Die gespeicherten Reaktionen sind aktuell deaktiviert. Führe `/setautoreaction` aus, um sie wieder zu aktivieren."

        embed.set_footer(text=f"{total} konfigurierte Auto-Reaktionen • {'aktiv' if active else 'deaktiviert'}")

        if total == 0:
            return await interaction.response.send_message(
                "❌ Es sind keine gültigen Auto-Reaktionen auf diesem Server eingerichtet.",
                ephemeral=True,
            )

        await interaction.response.send_message(embed=embed)

    @commands.Cog.listener()

    async def on_message(self, message: discord.Message):

        if message.author.bot:

            return

        if message.guild is None:
            return

        

        guild_id = str(message.guild.id)

        channel_id = str(message.channel.id)

        

        settings = self.config.get(guild_id)
        if not settings or not settings.get("enabled", True):
            return

        emoji = settings.get("channels", {}).get(channel_id)
        if not emoji:
            return

        try:
            await message.add_reaction(emoji)
        except discord.Forbidden:
            logging.warning(
                "AutoReaction fehlgeschlagen: fehlende Berechtigungen in Kanal %s auf Server %s",
                message.channel.id,
                message.guild.id,
            )
        except discord.HTTPException as error:
            logging.warning("AutoReaction für Kanal %s fehlgeschlagen: %s", message.channel.id, error)

    @setautoreaction.error

    @resetautoreaction.error

    async def autoreaction_error(self, interaction: discord.Interaction, error):

        if isinstance(error, app_commands.MissingPermissions):
            message = "❌ Du benötigst Administratorrechte für diesen Befehl!"
        else:
            logging.error("AutoReaction-Befehl fehlgeschlagen: %s", error)
            message = "❌ Der AutoReaction-Befehl ist fehlgeschlagen. Prüfe die Bot-Berechtigungen und versuche es erneut."

        if interaction.response.is_done():
            await interaction.followup.send(message, ephemeral=True)
        else:
            await interaction.response.send_message(message, ephemeral=True)

async def setup(bot):

    await bot.add_cog(AutoReaction(bot))
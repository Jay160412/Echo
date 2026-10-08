import discord

from discord.ext import commands

from discord import app_commands

import json

import os

import re

from typing import Optional, List

# Pfad zur Konfigurationsdatei

CONFIG_PATH = "./data/autoanswer_config.json"

def load_config():

    if not os.path.exists(CONFIG_PATH):

        return {}

    with open(CONFIG_PATH, "r") as f:

        return json.load(f)

def save_config(config):

    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)

    with open(CONFIG_PATH, "w") as f:

        json.dump(config, f, indent=4)

class AutoAnswer(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.config = load_config()

    # Hilfsfunktion: Nächste ID für einen Server ermitteln

    def _next_id(self, guild_id: str) -> int:

        if guild_id not in self.config:

            self.config[guild_id] = {"next_id": 1, "entries": []}

        # falls "entries" noch nicht existiert (alte Struktur)

        if "entries" not in self.config[guild_id]:

            self.config[guild_id]["entries"] = []

        return self.config[guild_id]["next_id"]

    # Hilfsfunktion: Channel-Mentions parsen

    def _parse_channels(self, guild: discord.Guild, channels_str: str) -> List[int]:

        if not channels_str:

            return []

        channel_ids = []

        for mention in re.findall(r'<#(\d+)>', channels_str):

            channel_id = int(mention)

            if guild.get_channel(channel_id):

                channel_ids.append(channel_id)

        return channel_ids

    @app_commands.command(name="autoanswer", description="Erstellt eine automatische Antwort")

    @app_commands.describe(

        trigger="Das Stichwort (exakter Vergleich, Groß-/Kleinschreibung egal)",

        response="Die Antwort (mit Platzhaltern wie {username}, {member}, {guild})",

        channels="Kanäle (optional, z.B. #allgemein #chat). Leer lassen für alle Kanäle."

    )

    @app_commands.checks.has_permissions(administrator=True)

    async def autoanswer(self, interaction: discord.Interaction, trigger: str, response: str, channels: Optional[str] = None):

        guild_id = str(interaction.guild.id)

        next_id = self._next_id(guild_id)

        channel_ids = self._parse_channels(interaction.guild, channels or "")

        entry = {

            "id": next_id,

            "trigger": trigger.strip(),

            "response": response,

            "channels": channel_ids

        }

        self.config[guild_id]["entries"].append(entry)

        self.config[guild_id]["next_id"] = next_id + 1

        save_config(self.config)

        # Formatierte Antwort für Embed

        channel_text = "alle Kanäle" if not channel_ids else f"{len(channel_ids)} Kanäle"

        embed = discord.Embed(

            title="✅ Auto-Antwort erstellt",

            description=f"**ID:** {next_id}\n**Trigger:** `{trigger}`\n**Antwort:** {response}\n**Kanäle:** {channel_text}",

            color=discord.Color.green()

        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="autoanswerlist", description="Listet alle Auto-Antworten auf")

    async def autoanswerlist(self, interaction: discord.Interaction):

        guild_id = str(interaction.guild.id)

        if guild_id not in self.config or not self.config[guild_id].get("entries"):

            return await interaction.response.send_message("❌ Es sind keine Auto-Antworten konfiguriert.", ephemeral=True)

        entries = self.config[guild_id]["entries"]

        embed = discord.Embed(

            title="📋 Auto-Antworten",

            color=discord.Color.blue()

        )

        for e in entries:

            channels_text = "Alle Kanäle" if not e["channels"] else ", ".join(

                f"<#{cid}>" for cid in e["channels"][:3]

            ) + (" …" if len(e["channels"]) > 3 else "")

            embed.add_field(

                name=f"ID {e['id']} – Trigger: `{e['trigger']}`",

                value=f"**Antwort:** {e['response']}\n**Kanäle:** {channels_text}",

                inline=False

            )

        embed.set_footer(text=f"Insgesamt {len(entries)} Auto-Antworten")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="resetautoanswer", description="Löscht eine Auto-Antwort anhand der ID")

    @app_commands.describe(id="Die ID der zu löschenden Auto-Antwort")

    @app_commands.checks.has_permissions(administrator=True)

    async def resetautoanswer(self, interaction: discord.Interaction, id: int):

        guild_id = str(interaction.guild.id)

        if guild_id not in self.config:

            return await interaction.response.send_message("❌ Es sind keine Auto-Antworten vorhanden.", ephemeral=True)

        entries = self.config[guild_id].get("entries", [])

        for i, e in enumerate(entries):

            if e["id"] == id:

                del entries[i]

                save_config(self.config)

                await interaction.response.send_message(f"✅ Auto-Antwort mit ID {id} wurde gelöscht.")

                return

        await interaction.response.send_message(f"❌ Keine Auto-Antwort mit ID {id} gefunden.", ephemeral=True)

    @commands.Cog.listener()

    async def on_message(self, message: discord.Message):

        if message.author.bot:

            return

        guild_id = str(message.guild.id)

        if guild_id not in self.config:

            return

        entries = self.config[guild_id].get("entries", [])

        for e in entries:

            # Trigger prüfen (exakt, case-insensitive)

            if message.content.strip().lower() != e["trigger"].lower():

                continue

            # Kanalprüfung

            if e["channels"] and message.channel.id not in e["channels"]:

                continue

            # Platzhalter ersetzen

            response = e["response"]

            replacements = {

                "{username}": message.author.name,

                "{member}": message.author.mention,

                "{guild}": message.guild.name,

                "{channel}": message.channel.mention,

                "{user}": message.author.display_name,

                "{server}": message.guild.name,

                "{mention}": message.author.mention

            }

            for key, value in replacements.items():

                response = response.replace(key, value)

            try:

                await message.channel.send(response)

            except discord.Forbidden:

                print(f"Keine Berechtigung zum Senden in {message.channel.name}")

            except Exception as e:

                print(f"Fehler beim Senden der Auto-Antwort: {e}")

    # Fehlerbehandlung für fehlende Berechtigungen

    @autoanswer.error

    @resetautoanswer.error

    async def autoanswer_error(self, interaction: discord.Interaction, error):

        if isinstance(error, app_commands.MissingPermissions):

            await interaction.response.send_message("❌ Du benötigst Administratorrechte für diesen Befehl.", ephemeral=True)

async def setup(bot):

    await bot.add_cog(AutoAnswer(bot))
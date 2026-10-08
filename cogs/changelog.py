import discord

from discord.ext import commands

from discord import app_commands

import json

import os

CHANGELOG_PATH = "./data/changelog.json"

async def is_bot_owner(interaction: discord.Interaction) -> bool:
    return await interaction.client.is_owner(interaction.user)

def load_changelog():

    if not os.path.exists(CHANGELOG_PATH):

        return []

    with open(CHANGELOG_PATH, "r") as f:

        return json.load(f)

def save_changelog(data):

    os.makedirs(os.path.dirname(CHANGELOG_PATH), exist_ok=True)

    with open(CHANGELOG_PATH, "w") as f:

        json.dump(data, f, indent=4)

class Changelog(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @app_commands.command(name="changelog", description="Zeigt die letzten Änderungen des Bots")

    async def changelog(self, interaction: discord.Interaction):

        changelog = load_changelog()

        if not changelog:

            return await interaction.response.send_message("Noch kein Changelog vorhanden.", ephemeral=True)

        embed = discord.Embed(

            title="📜 Changelog",

            description="Neueste Änderungen:",

            color=discord.Color.gold()

        )

        for entry in changelog[:5]:

            embed.add_field(

                name=entry.get("version", "Unbekannt"),

                value=entry.get("description", ""),

                inline=False

            )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="addchangelog", description="Fügt einen Changelog-Eintrag hinzu (nur Owner)")

    @app_commands.check(is_bot_owner)

    async def addchangelog(self, interaction: discord.Interaction, version: str, description: str):

        changelog = load_changelog()

        changelog.insert(0, {"version": version, "description": description})

        save_changelog(changelog)

        await interaction.response.send_message("✅ Changelog-Eintrag hinzugefügt.")

async def setup(bot):

    await bot.add_cog(Changelog(bot))
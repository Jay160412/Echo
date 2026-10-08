import discord

from discord import app_commands

from discord.ext import commands

import json

import os
import logging

from typing import Optional

class WelcomeSystem(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.data_file = "data/welcome_data.json"

        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)

        self.load_data()

    def load_data(self):

        try:

            with open(self.data_file, 'r') as f:

                self.data = json.load(f)

        except (FileNotFoundError, json.JSONDecodeError):

            self.data = {"welcome": {}, "goodbye": {}}

        self.data.setdefault("welcome", {})
        self.data.setdefault("goodbye", {})

    def save_data(self):

        with open(self.data_file, 'w') as f:

            json.dump(self.data, f, indent=2)

    def replace_placeholders(self, text: str, member: discord.Member, guild: discord.Guild) -> str:

        replacements = {

            "{member}": member.mention,

            "{guild}": guild.name,

            "{count}": str(guild.member_count),

            "{username}": member.name,

            "{tag}": str(member)

        }

        for key, value in replacements.items():

            text = text.replace(key, value)

        return text

    async def send_welcome_message(self, member: discord.Member):

        config = self.data["welcome"].get(str(member.guild.id))

        if not config:

            return False

        channel = member.guild.get_channel(config["channel_id"])

        if not channel:

            return False

        embed = discord.Embed(

            title=self.replace_placeholders(config["title"], member, member.guild),

            description=self.replace_placeholders(config["description"], member, member.guild),

            color=config["color"]

        )

        if config["show_avatar"]:

            embed.set_thumbnail(url=member.display_avatar.url)

        if config["footer"]:

            embed.set_footer(text=self.replace_placeholders(config["footer"], member, member.guild))

        try:
            await channel.send(embed=embed)
            return True
        except discord.Forbidden:
            logging.warning("Welcome-Nachricht kann in %s nicht gesendet werden: fehlende Berechtigung", channel.id)
        except discord.HTTPException as error:
            logging.warning("Welcome-Nachricht konnte nicht gesendet werden: %s", error)
        return False

    async def send_goodbye_message(self, member: discord.Member):

        config = self.data["goodbye"].get(str(member.guild.id))

        if not config:

            return False

        channel = member.guild.get_channel(config["channel_id"])

        if not channel:

            return False

        embed = discord.Embed(

            title=self.replace_placeholders(config["title"], member, member.guild),

            description=self.replace_placeholders(config["description"], member, member.guild),

            color=config["color"]

        )

        if config["show_avatar"]:

            embed.set_thumbnail(url=member.display_avatar.url)

        if config["footer"]:

            embed.set_footer(text=self.replace_placeholders(config["footer"], member, member.guild))

        try:
            await channel.send(embed=embed)
            return True
        except discord.Forbidden:
            logging.warning("Bye-Nachricht kann in %s nicht gesendet werden: fehlende Berechtigung", channel.id)
        except discord.HTTPException as error:
            logging.warning("Bye-Nachricht konnte nicht gesendet werden: %s", error)
        return False

    # Befehle

    @app_commands.command(name="setwelcome", description="🎉 Aktiviere Willkommensnachrichten")

    @app_commands.describe(

        channel="Zielkanal",

        title="Titel (Nutze {member}, {guild}, {count}, {username})",

        description="Beschreibung (\\n für neue Zeilen)",

        show_avatar="Avatar anzeigen?",

        footer="Footer-Text",

        color="Hex-Farbe (#RRGGBB)"

    )

    async def set_welcome(

        self,

        interaction: discord.Interaction,

        channel: discord.TextChannel,

        title: str,

        description: str,

        show_avatar: Optional[bool] = False,

        footer: Optional[str] = None,

        color: Optional[str] = None

    ):

        self.data["welcome"][str(interaction.guild.id)] = {

            "channel_id": channel.id,

            "title": title,

            "description": description.replace("\\n", "\n"),

            "show_avatar": show_avatar,

            "footer": footer.replace("\\n", "\n") if footer else None,

            "color": int(color[1:], 16) if color else 0x2ecc71

        }

        self.save_data()

        await interaction.response.send_message(f"✅ Willkommensnachrichten in {channel.mention} aktiviert!", ephemeral=True)

    @app_commands.command(name="testwelcome", description="🔧 Teste die Willkommensnachricht")

    async def test_welcome(self, interaction: discord.Interaction):

        if str(interaction.guild.id) not in self.data["welcome"]:

            return await interaction.response.send_message("❌ Keine Willkommensnachricht konfiguriert!", ephemeral=True)

        

        sent = await self.send_welcome_message(interaction.user)
        if not sent:
            return await interaction.response.send_message(
                "❌ Die Nachricht konnte nicht gesendet werden. Prüfe, ob der Kanal noch existiert "
                "und der Bot dort Nachrichten senden und Embeds einbetten darf.",
                ephemeral=True,
            )

        await interaction.response.send_message("✅ Testnachricht gesendet!", ephemeral=True)

    @app_commands.command(name="resetwelcome", description="🗑️ Deaktiviere Willkommensnachrichten")

    async def reset_welcome(self, interaction: discord.Interaction):

        if str(interaction.guild.id) in self.data["welcome"]:

            del self.data["welcome"][str(interaction.guild.id)]

            self.save_data()

            await interaction.response.send_message("✅ Willkommensnachrichten deaktiviert!", ephemeral=True)

        else:

            await interaction.response.send_message("ℹ️ Es waren keine Willkommensnachrichten aktiviert.", ephemeral=True)

    @app_commands.command(name="setbye", description="👋 Aktiviere Abschiedsnachrichten")

    @app_commands.describe(

        channel="Zielkanal",

        title="Titel (Nutze {member}, {guild}, {count}, {username})",

        description="Beschreibung (\\n für neue Zeilen)",

        show_avatar="Avatar anzeigen?",

        footer="Footer-Text",

        color="Hex-Farbe (#RRGGBB)"

    )

    async def set_goodbye(

        self,

        interaction: discord.Interaction,

        channel: discord.TextChannel,

        title: str,

        description: str,

        show_avatar: Optional[bool] = False,

        footer: Optional[str] = None,

        color: Optional[str] = None

    ):

        self.data["goodbye"][str(interaction.guild.id)] = {

            "channel_id": channel.id,

            "title": title,

            "description": description.replace("\\n", "\n"),

            "show_avatar": show_avatar,

            "footer": footer.replace("\\n", "\n") if footer else None,

            "color": int(color[1:], 16) if color else 0xe74c3c

        }

        self.save_data()

        await interaction.response.send_message(f"✅ Abschiedsnachrichten in {channel.mention} aktiviert!", ephemeral=True)

    @app_commands.command(name="testbye", description="🔧 Teste die Abschiedsnachricht")

    async def test_goodbye(self, interaction: discord.Interaction):

        if str(interaction.guild.id) not in self.data["goodbye"]:

            return await interaction.response.send_message("❌ Keine Abschiedsnachricht konfiguriert!", ephemeral=True)

        

        sent = await self.send_goodbye_message(interaction.user)
        if not sent:
            return await interaction.response.send_message(
                "❌ Die Nachricht konnte nicht gesendet werden. Prüfe, ob der Kanal noch existiert "
                "und der Bot dort Nachrichten senden und Embeds einbetten darf.",
                ephemeral=True,
            )

        await interaction.response.send_message("✅ Testnachricht gesendet!", ephemeral=True)

    @app_commands.command(name="resetbye", description="🗑️ Deaktiviere Abschiedsnachrichten")

    async def reset_goodbye(self, interaction: discord.Interaction):

        if str(interaction.guild.id) in self.data["goodbye"]:

            del self.data["goodbye"][str(interaction.guild.id)]

            self.save_data()

            await interaction.response.send_message("✅ Abschiedsnachrichten deaktiviert!", ephemeral=True)

        else:

            await interaction.response.send_message("ℹ️ Es waren keine Abschiedsnachrichten aktiviert.", ephemeral=True)

    # Event-Handler

    @commands.Cog.listener()

    async def on_member_join(self, member: discord.Member):

        await self.send_welcome_message(member)

    @commands.Cog.listener()

    async def on_member_remove(self, member: discord.Member):

        await self.send_goodbye_message(member)

async def setup(bot):

    await bot.add_cog(WelcomeSystem(bot))
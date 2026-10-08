import discord

from discord.ext import commands
from discord import app_commands
from discord import ui

import json

import os

# Pfad zur Konfigurationsdatei

CONFIG_PATH = "./data/ticket_config.json"

# Funktion zum Laden der Konfiguration

def load_config():

    if not os.path.exists(CONFIG_PATH):

        return {}

    with open(CONFIG_PATH, "r") as f:

        return json.load(f)

# Funktion zum Speichern der Konfiguration

def save_config(config):

    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)

    with open(CONFIG_PATH, "w") as f:

        json.dump(config, f, indent=4)

# Cog für das Ticket-System

class TicketSystem(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.config = load_config()

    # Slash-Command: /ticketenable

    @app_commands.command(name="ticketenable", description="Aktiviert das Ticket-System.")

    @app_commands.describe(

        channel="Der Kanal, in dem die Ticket-Nachricht gesendet werden soll.",

        message="Die Nachricht, die im Ticket-Kanal angezeigt wird.",

        button_text="Der Text, der auf dem Ticket-Button angezeigt wird."

    )

    async def ticketenable(

        self,

        interaction: discord.Interaction,

        channel: discord.TextChannel,

        message: str,

        button_text: str

    ):

        # Überprüfen, ob der Benutzer Administratorrechte hat

        if not interaction.user.guild_permissions.administrator:

            await interaction.response.send_message("Du hast keine Berechtigung, dies zu tun.", ephemeral=True)

            return

        guild_id = str(interaction.guild.id)

        self.config[guild_id] = {

            "ticket_channel_id": channel.id,

            "ticket_message": message,

            "button_text": button_text,

            "enabled": True

        }

        save_config(self.config)

        # Ticket-Nachricht mit Button senden

        view = ui.View()

        view.add_item(ui.Button(style=discord.ButtonStyle.primary, label=button_text, custom_id="create_ticket"))

        await channel.send(message, view=view)

        await interaction.response.send_message("Ticket-System aktiviert! 🎉", ephemeral=True)

    # Slash-Command: /ticketdisable

    @app_commands.command(name="ticketdisable", description="Deaktiviert das Ticket-System.")

    async def ticketdisable(self, interaction: discord.Interaction):

        # Überprüfen, ob der Benutzer Administratorrechte hat

        if not interaction.user.guild_permissions.administrator:

            await interaction.response.send_message("Du hast keine Berechtigung, dies zu tun.", ephemeral=True)

            return

        guild_id = str(interaction.guild.id)

        if guild_id in self.config:

            self.config[guild_id]["enabled"] = False

            save_config(self.config)

            await interaction.response.send_message("Ticket-System deaktiviert! 🚫", ephemeral=True)

        else:

            await interaction.response.send_message("Das Ticket-System ist bereits deaktiviert.", ephemeral=True)

    # Event: Wenn ein Button geklickt wird

    @commands.Cog.listener()

    async def on_interaction(self, interaction: discord.Interaction):

        if interaction.type == discord.InteractionType.component:

            custom_id = interaction.data.get("custom_id")

            if custom_id == "create_ticket":

                await self.create_ticket(interaction)

            elif custom_id == "close_ticket":

                await self.close_ticket(interaction)

    # Funktion: Ticket erstellen

    async def create_ticket(self, interaction: discord.Interaction):

        guild_id = str(interaction.guild.id)

        if guild_id not in self.config or not self.config[guild_id]["enabled"]:

            return  # Ticket-System ist deaktiviert

        # Ticket-Kanal erstellen

        guild = interaction.guild

        category = discord.utils.get(guild.categories, name="Tickets")  # Kategorie für Tickets

        if not category:

            category = await guild.create_category("Tickets")

        ticket_channel = await guild.create_text_channel(

            name=f"ticket-{interaction.user.name}",

            category=category

        )

        # Berechtigungen setzen

        await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)

        await ticket_channel.set_permissions(guild.default_role, read_messages=False)

        # Ticket-Nachricht senden

        embed = discord.Embed(

            title="Ticket erstellt",

            description="Ein Team-Mitglied wird sich bald um dich kümmern.",

            color=discord.Color.blue()

        )

        view = ui.View()

        view.add_item(ui.Button(style=discord.ButtonStyle.danger, label="Ticket schließen", custom_id="close_ticket"))

        await ticket_channel.send(interaction.user.mention, embed=embed, view=view)

        await interaction.response.send_message(f"Dein Ticket wurde erstellt: {ticket_channel.mention}", ephemeral=True)

    # Funktion: Ticket schließen

    async def close_ticket(self, interaction: discord.Interaction):

        # Überprüfen, ob der Kanal ein Ticket-Kanal ist

        if not interaction.channel.name.startswith("ticket-"):

            await interaction.response.send_message("Dies ist kein Ticket-Kanal.", ephemeral=True)

            return

        # Kanal löschen

        await interaction.response.send_message("Ticket wird geschlossen...")

        await interaction.channel.delete()

# Setup-Funktion für den Cog

async def setup(bot):

    await bot.add_cog(TicketSystem(bot))
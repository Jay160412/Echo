import discord

from discord.ext import commands

from discord import app_commands

import json

import os

import asyncio

CONFIG_PATH = "./data/bot_events_config.json"

def load_config():

    if not os.path.exists(CONFIG_PATH):

        return {}

    with open(CONFIG_PATH, "r") as f:

        return json.load(f)

def save_config(config):

    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)

    with open(CONFIG_PATH, "w") as f:

        json.dump(config, f, indent=4)

class BotEvents(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.config = load_config()

        self.last_cogs = set()

    @app_commands.command(name="setbotstatus", description="Setzt den Kanal für Bot-Statusmeldungen")

    @app_commands.checks.has_permissions(administrator=True)

    async def setbotstatus(self, interaction: discord.Interaction, channel: discord.TextChannel):

        guild_id = str(interaction.guild.id)

        if "status" not in self.config:

            self.config["status"] = {}

        self.config["status"][guild_id] = channel.id

        save_config(self.config)

        await interaction.response.send_message(f"✅ Bot-Status wird in {channel.mention} gepostet.")

    @app_commands.command(name="setbotnews", description="Setzt den Kanal für Bot-News (neue Cogs)")

    @app_commands.checks.has_permissions(administrator=True)

    async def setbotnews(self, interaction: discord.Interaction, channel: discord.TextChannel):

        guild_id = str(interaction.guild.id)

        if "news" not in self.config:

            self.config["news"] = {}

        self.config["news"][guild_id] = channel.id

        save_config(self.config)

        await interaction.response.send_message(f"✅ Bot-News werden in {channel.mention} gepostet.")

    async def send_status(self, message: str, color: discord.Color):

        if "status" not in self.config:

            return

        for guild_id, channel_id in self.config["status"].items():

            guild = self.bot.get_guild(int(guild_id))

            if guild:

                channel = guild.get_channel(channel_id)

                if channel:

                    embed = discord.Embed(

                        title="🤖 Bot-Status",

                        description=message,

                        color=color,

                        timestamp=discord.utils.utcnow()

                    )

                    await channel.send(embed=embed)

    async def check_new_cogs(self):

        loaded = set([cog.__class__.__name__ for cog in self.bot.cogs.values()])

        if not self.last_cogs:

            self.last_cogs = loaded

            return

        new_cogs = loaded - self.last_cogs

        if new_cogs and "news" in self.config:

            for guild_id, channel_id in self.config["news"].items():

                guild = self.bot.get_guild(int(guild_id))

                if guild:

                    channel = guild.get_channel(channel_id)

                    if channel:

                        embed = discord.Embed(

                            title="📢 Neue Funktion verfügbar!",

                            description=f"Neuer Befehl: `/{', /'.join(new_cogs)}`",

                            color=discord.Color.blue()

                        )

                        await channel.send(embed=embed)

        self.last_cogs = loaded

    @commands.Cog.listener()

    async def on_ready(self):

        await self.send_status("Bot wurde neugestartet 🔌", discord.Color.green())

        await self.check_new_cogs()

    @commands.Cog.listener()

    async def on_disconnect(self):

        await self.send_status("Bot geht offline ❌", discord.Color.red())

async def setup(bot):

    await bot.add_cog(BotEvents(bot))
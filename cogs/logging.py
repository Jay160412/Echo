import discord

from discord.ext import commands

from discord import app_commands

import json

import os

CONFIG_PATH = "./data/logging_config.json"

def load_config():

    if not os.path.exists(CONFIG_PATH):

        return {}

    with open(CONFIG_PATH, "r") as f:

        return json.load(f)

def save_config(config):

    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)

    with open(CONFIG_PATH, "w") as f:

        json.dump(config, f, indent=4)

class Logging(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.config = load_config()

    @app_commands.command(name="setlogchannel", description="Setzt den Log‑Kanal für diesen Server")

    @app_commands.describe(channel="Der Kanal, in dem Logs erscheinen sollen")

    @app_commands.checks.has_permissions(administrator=True)

    async def setlogchannel(self, interaction: discord.Interaction, channel: discord.TextChannel):

        guild_id = str(interaction.guild.id)

        self.config[guild_id] = {"channel_id": channel.id}

        save_config(self.config)

        await interaction.response.send_message(f"✅ Log‑Kanal wurde auf {channel.mention} gesetzt.")

    # Events

    @commands.Cog.listener()

    async def on_message_delete(self, message: discord.Message):

        if message.author.bot:

            return

        guild_id = str(message.guild.id)

        if guild_id not in self.config:

            return

        channel = message.guild.get_channel(self.config[guild_id]["channel_id"])

        if not channel:

            return

        embed = discord.Embed(

            title="Nachricht gelöscht",

            description=f"**Autor:** {message.author.mention}\n**Kanal:** {message.channel.mention}\n**Inhalt:** {message.content}",

            color=discord.Color.red(),

            timestamp=message.created_at

        )

        await channel.send(embed=embed)

    @commands.Cog.listener()

    async def on_message_edit(self, before: discord.Message, after: discord.Message):

        if before.author.bot or before.content == after.content:

            return

        guild_id = str(before.guild.id)

        if guild_id not in self.config:

            return

        channel = before.guild.get_channel(self.config[guild_id]["channel_id"])

        if not channel:

            return

        embed = discord.Embed(

            title="Nachricht bearbeitet",

            description=f"**Autor:** {before.author.mention}\n**Kanal:** {before.channel.mention}",

            color=discord.Color.orange()

        )

        embed.add_field(name="Vorher", value=before.content[:1024], inline=False)

        embed.add_field(name="Nachher", value=after.content[:1024], inline=False)

        await channel.send(embed=embed)

    @commands.Cog.listener()

    async def on_member_join(self, member: discord.Member):

        guild_id = str(member.guild.id)

        if guild_id not in self.config:

            return

        channel = member.guild.get_channel(self.config[guild_id]["channel_id"])

        if not channel:

            return

        embed = discord.Embed(

            title="Mitglied beigetreten",

            description=f"{member.mention} (`{member}`)",

            color=discord.Color.green(),

            timestamp=member.joined_at

        )

        embed.set_thumbnail(url=member.avatar.url)

        embed.add_field(name="Account erstellt", value=member.created_at.strftime("%d.%m.%Y %H:%M"))

        await channel.send(embed=embed)

    @commands.Cog.listener()

    async def on_member_remove(self, member: discord.Member):

        guild_id = str(member.guild.id)

        if guild_id not in self.config:

            return

        channel = member.guild.get_channel(self.config[guild_id]["channel_id"])

        if not channel:

            return

        embed = discord.Embed(

            title="Mitglied verlassen",

            description=f"{member.mention} (`{member}`)",

            color=discord.Color.red(),

            timestamp=discord.utils.utcnow()

        )

        embed.set_thumbnail(url=member.avatar.url)

        await channel.send(embed=embed)

async def setup(bot):

    await bot.add_cog(Logging(bot))
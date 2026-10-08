import discord

from discord.ext import commands

from discord import app_commands

import json

import os

from typing import Optional

import datetime   # <-- Fehlender Import

CONFIG_PATH = "./data/warns.json"

def load_warns():

    if not os.path.exists(CONFIG_PATH):

        return {}

    with open(CONFIG_PATH, "r") as f:

        return json.load(f)

def save_warns(warns):

    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)

    with open(CONFIG_PATH, "w") as f:

        json.dump(warns, f, indent=4)

class Warn(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.warns = load_warns()

    @app_commands.command(name="warn", description="Verwarnt einen Nutzer")

    @app_commands.describe(

        user="Der Nutzer",

        reason="Grund der Verwarnung",

        dm="Soll der Nutzer per DM benachrichtigt werden?",

        timeout="Optionale Strafe (Timeouts in Minuten, z.B. 10)"

    )

    @app_commands.checks.has_permissions(manage_messages=True)

    async def warn(self, interaction: discord.Interaction, user: discord.Member, reason: str, dm: bool = True, timeout: Optional[int] = None):

        guild_id = str(interaction.guild.id)

        user_id = str(user.id)

        if guild_id not in self.warns:

            self.warns[guild_id] = {}

        if user_id not in self.warns[guild_id]:

            self.warns[guild_id][user_id] = []

        warn_id = len(self.warns[guild_id][user_id]) + 1

        warn_entry = {

            "id": warn_id,

            "reason": reason,

            "moderator": interaction.user.id,

            "timestamp": discord.utils.utcnow().isoformat()

        }

        self.warns[guild_id][user_id].append(warn_entry)

        save_warns(self.warns)

        if dm:

            try:

                embed = discord.Embed(

                    title="⚠️ Verwarnung",

                    description=f"Du wurdest auf **{interaction.guild.name}** verwarnt.\n**Grund:** {reason}",

                    color=discord.Color.orange()

                )

                if timeout:

                    embed.add_field(name="Strafe", value=f"Timeout: {timeout} Minuten", inline=False)

                await user.send(embed=embed)

            except:

                pass

        if timeout:

            try:

                timeout_duration = discord.utils.utcnow() + datetime.timedelta(minutes=timeout)

                await user.timeout(timeout_duration, reason=reason)

            except:

                pass

        embed = discord.Embed(

            title="✅ Verwarnung ausgesprochen",

            description=f"{user.mention} wurde verwarnt.\n**Grund:** {reason}",

            color=discord.Color.green()

        )

        if timeout:

            embed.add_field(name="Strafe", value=f"Timeout: {timeout} Minuten", inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="warns", description="Zeigt Verwarnungen eines Nutzers")

    async def warns(self, interaction: discord.Interaction, user: discord.Member):

        guild_id = str(interaction.guild.id)

        user_id = str(user.id)

        if guild_id not in self.warns or user_id not in self.warns[guild_id]:

            return await interaction.response.send_message(f"{user.mention} hat keine Verwarnungen.", ephemeral=True)

        warns = self.warns[guild_id][user_id]

        embed = discord.Embed(title=f"Verwarnungen von {user.display_name}", color=discord.Color.orange())

        for w in warns[-5:]:

            embed.add_field(

                name=f"ID {w['id']}",

                value=f"**Grund:** {w['reason']}\n**Von:** <@{w['moderator']}>",

                inline=False

            )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="clearwarns", description="Löscht alle Verwarnungen eines Nutzers")

    @app_commands.checks.has_permissions(administrator=True)

    async def clearwarns(self, interaction: discord.Interaction, user: discord.Member):

        guild_id = str(interaction.guild.id)

        user_id = str(user.id)

        if guild_id in self.warns and user_id in self.warns[guild_id]:

            del self.warns[guild_id][user_id]

            save_warns(self.warns)

            await interaction.response.send_message(f"✅ Alle Verwarnungen von {user.mention} wurden gelöscht.")

        else:

            await interaction.response.send_message(f"{user.mention} hat keine Verwarnungen.", ephemeral=True)

async def setup(bot):

    await bot.add_cog(Warn(bot))
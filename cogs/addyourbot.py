import discord
from discord.ext import commands
from discord import app_commands, ui
import datetime
import sqlite3
import re
import os
import asyncio
from typing import Optional

class BotReviewView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @ui.button(label="Akzeptieren", style=discord.ButtonStyle.green, custom_id="accept_bot")
    async def accept_bot(self, interaction: discord.Interaction, button: ui.Button):
        try:
            embed = interaction.message.embeds[0]
            bot_id = int(embed.fields[0].value)
            submitter_id = int(embed.footer.text.split("ID: ")[1])
            
            perms = discord.Permissions(
                manage_roles=True,
                manage_channels=True,
                kick_members=True,
                ban_members=False
            )
            
            invite_url = f"https://discord.com/oauth2/authorize?client_id={bot_id}&permissions={perms.value}&scope=bot%20applications.commands"
            
            embed.color = discord.Color.green()
            embed.title = "✅ Bot akzeptiert"
            embed.add_field(name="Einladungslink", value=f"[Klicke hier]({invite_url})", inline=False)
            
            await interaction.message.edit(embed=embed, view=None)
            
            submitter = interaction.guild.get_member(submitter_id)
            if submitter:
                try:
                    await submitter.send(f"🎉 Dein Bot wurde akzeptiert!\n**Einladungslink:** {invite_url}")
                except discord.Forbidden:
                    pass
            
            await interaction.response.send_message(
                f"✅ Bot erfolgreich akzeptiert! [Einladungslink]({invite_url})",
                ephemeral=True
            )
            
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Fehler: {str(e)}",
                ephemeral=True
            )
    
    @ui.button(label="Ablehnen", style=discord.ButtonStyle.red, custom_id="reject_bot")
    async def reject_bot(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(RejectModal(interaction.message))

class RejectModal(ui.Modal, title="Ablehnungsgrund"):
    reason = ui.TextInput(
        label="Begründung (mind. 30 Zeichen)",
        style=discord.TextStyle.long,
        min_length=30,
        required=True
    )
    
    def __init__(self, message):
        super().__init__()
        self.message = message
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            embed = self.message.embeds[0]
            embed.color = discord.Color.red()
            embed.title = "❌ Bot abgelehnt"
            embed.add_field(name="Begründung", value=self.reason.value, inline=False)
            
            submitter_id = int(embed.footer.text.split("ID: ")[1])
            submitter = interaction.guild.get_member(submitter_id)
            
            await self.message.edit(embed=embed, view=None)
            
            if submitter:
                try:
                    await submitter.send(f"😕 Dein Bot wurde abgelehnt.\n**Grund:** {self.reason.value}")
                except discord.Forbidden:
                    pass
            
            await interaction.response.send_message(
                "✅ Ablehnung erfolgreich gespeichert!",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Fehler: {str(e)}",
                ephemeral=True
            )

class SubmitModal(ui.Modal, title="Bot einreichen"):
    bot_id = ui.TextInput(
        label="Bot-ID",
        placeholder="123456789012345678",
        required=True
    )
    
    prefix = ui.TextInput(
        label="Prefix",
        placeholder="! oder /",
        required=True
    )
    
    description = ui.TextInput(
        label="Beschreibung (mind. 100 Zeichen)",
        style=discord.TextStyle.long,
        min_length=100,
        required=True
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            if not self.bot_id.value.isdigit():
                return await interaction.response.send_message(
                    "❌ Die Bot-ID muss eine Zahl sein!",
                    ephemeral=True
                )
            
            if not re.match(r'^[!\/][\w\d]{0,5}$', self.prefix.value):
                return await interaction.response.send_message(
                    "❌ Ungültiges Prefix! Muss mit ! oder / beginnen und max. 6 Zeichen lang sein.",
                    ephemeral=True
                )
            
            embed = discord.Embed(
                title="🆕 Neue Bot-Einreichung",
                color=discord.Color.blue(),
                timestamp=datetime.datetime.now()
            )
            
            embed.add_field(name="🤖 Bot-ID", value=self.bot_id.value, inline=False)
            embed.add_field(name="🔣 Prefix", value=self.prefix.value, inline=False)
            embed.add_field(name="📝 Beschreibung", value=self.description.value, inline=False)
            embed.set_footer(text=f"Eingereicht von {interaction.user} • ID: {interaction.user.id}")
            
            cog = interaction.client.get_cog("BotReviewSystem")
            
            if cog and cog.review_channel:
                view = BotReviewView()
                await cog.review_channel.send(embed=embed, view=view)
                
                await interaction.response.send_message(
                    "✅ Dein Bot wurde zur Überprüfung eingereicht!",
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    "❌ Review-System nicht korrekt konfiguriert!",
                    ephemeral=True
                )
            
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Fehler: {str(e)}",
                ephemeral=True
            )

class BotReviewSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        db_dir = os.path.dirname(__file__)
        self.db_path = os.path.join(db_dir, '..', 'bot_review.db')
        self.db = sqlite3.connect(self.db_path, check_same_thread=False)
        
        self.submit_channel = None
        self.review_channel = None
        self._initialized = False
        
        self._init_db()
    
    def _init_db(self):
        """Datenbank initialisieren"""
        with self.db:
            self.db.execute("""
                CREATE TABLE IF NOT EXISTS bot_review_config (
                    guild_id INTEGER PRIMARY KEY,
                    submit_channel INTEGER,
                    review_channel INTEGER
                )
            """)
    
    async def _load_config(self):
        """Konfiguration laden"""
        try:
            if not self.bot.guilds:
                return
            
            guild_id = self.bot.guilds[0].id
            with self.db:
                config = self.db.execute("""
                    SELECT submit_channel, review_channel
                    FROM bot_review_config
                    WHERE guild_id = ?
                """, (guild_id,)).fetchone()
                
                if config:
                    try:
                        self.submit_channel = await self.bot.fetch_channel(config[0])
                        self.review_channel = await self.bot.fetch_channel(config[1])
                    except discord.errors.DiscordException:
                        self.submit_channel = None
                        self.review_channel = None
        except discord.errors.DiscordException:
            pass
    
    async def _ensure_setup_message(self):
        """Stellt die Einreichungsnachricht bereit"""
        if not self.submit_channel:
            return
        
        async for message in self.submit_channel.history(limit=5):
            if message.author == self.bot.user and message.components:
                return
        
        embed = discord.Embed(
            title="🤖 Bot einreichen",
            description="Klicke unten um deinen Bot zur Überprüfung einzureichen",
            color=discord.Color.blue()
        )
        
        view = ui.View()
        view.add_item(ui.Button(
            label="📨 Bot einreichen",
            style=discord.ButtonStyle.primary,
            custom_id="submit_bot"
        ))
        
        await self.submit_channel.send(embed=embed, view=view)
    
    @commands.Cog.listener()
    async def on_ready(self):
        if self._initialized:
            return
        await self._load_config()
        await self._ensure_setup_message()
        self._initialized = True
    
    async def _ensure_setup_message(self):
        """Stellt die Einreichungsnachricht bereit"""
        if not self.submit_channel:
            return
        
        async for message in self.submit_channel.history(limit=5):
            if message.author == self.bot.user and message.components:
                return
        
        embed = discord.Embed(
            title="🤖 Bot einreichen",
            description="Klicke unten um deinen Bot zur Überprüfung einzureichen",
            color=discord.Color.blue()
        )
        
        view = ui.View()
        view.add_item(ui.Button(
            label="📨 Bot einreichen",
            style=discord.ButtonStyle.primary,
            custom_id="submit_bot"
        ))
        
        await self.submit_channel.send(embed=embed, view=view)
    
    @app_commands.command(name="setbotsubmit", description="Konfiguriert das Bot-Review-System")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(
        submit_channel="Kanal für Bot-Einreichungen",
        review_channel="Kanal für Mod-Reviews"
    )
    async def setup_system(self, interaction: discord.Interaction,
                         submit_channel: discord.TextChannel,
                         review_channel: discord.TextChannel):
        """Konfiguriert die Systemkanäle"""
        try:
            with self.db:
                self.db.execute("""
                    INSERT OR REPLACE INTO bot_review_config
                    (guild_id, submit_channel, review_channel)
                    VALUES (?, ?, ?)
                """, (interaction.guild.id, submit_channel.id, review_channel.id))
            
            self.submit_channel = submit_channel
            self.review_channel = review_channel
            
            await self._ensure_setup_message()
            
            await interaction.response.send_message(
                "✅ Bot-Review-System erfolgreich eingerichtet!",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Fehler: {str(e)}",
                ephemeral=True
            )
    
    @app_commands.command(name="resetbotsubmit", description="Setzt die Konfiguration zurück")
    @app_commands.default_permissions(administrator=True)
    async def reset_system(self, interaction: discord.Interaction):
        """Setzt die Systemkonfiguration zurück"""
        try:
            with self.db:
                self.db.execute("""
                    DELETE FROM bot_review_config
                    WHERE guild_id = ?
                """, (interaction.guild.id,))
            
            self.submit_channel = None
            self.review_channel = None
            
            await interaction.response.send_message(
                "✅ Konfiguration zurückgesetzt!",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Fehler: {str(e)}",
                ephemeral=True
            )
    
    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        """Handles button interactions"""
        if interaction.type == discord.InteractionType.component:
            if interaction.data.get("custom_id") == "submit_bot":
                await interaction.response.send_modal(SubmitModal())

async def setup(bot):
    cog = BotReviewSystem(bot)
    await bot.add_cog(cog)

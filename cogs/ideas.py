import discord

from discord.ext import commands

from discord import app_commands, ui

import datetime

class IdeaButtons(ui.View):

    def __init__(self):

        super().__init__(timeout=None)

    

    @ui.button(label="👍 Akzeptieren", style=discord.ButtonStyle.green, custom_id="accept_idea")

    async def accept_button(self, interaction: discord.Interaction, button: ui.Button):

        await interaction.response.send_modal(AcceptanceModal(interaction.message))

    @ui.button(label="👎 Ablehnen", style=discord.ButtonStyle.red, custom_id="reject_idea")

    async def reject_button(self, interaction: discord.Interaction, button: ui.Button):

        await interaction.response.send_modal(RejectionModal(interaction.message))

class AcceptanceModal(ui.Modal, title='Akzeptanz-Details'):

    details = ui.TextInput(

        label='Zusätzliche Infos (Dauer/Planung)',

        style=discord.TextStyle.long,

        placeholder="Wird in ~2 Wochen umgesetzt! 🚀",

        required=False

    )

    def __init__(self, message):

        super().__init__()

        self.message = message

    async def on_submit(self, interaction: discord.Interaction):

        try:

            embed = self.message.embeds[0]

            embed.color = 0x57F287

            embed.title = "✅ Idee akzeptiert"

            

            if self.details.value:

                embed.add_field(name="📅 Umsetzungsplan", value=self.details.value, inline=False)

            

            submitter_id = int(embed.footer.text.split("ID: ")[1])

            submitter = interaction.guild.get_member(submitter_id)

            

            # An ERGEBNIS-Kanal senden

            result_channel = interaction.client.get_channel(1357408883358044301)

            if result_channel:

                message_content = [

                    f"{submitter.mention if submitter else 'Der Nutzer'} deine Idee wurde akzeptiert! 🎉",

                    f"**Original-Idee:** {embed.description}"

                ]

                

                if self.details.value:

                    message_content.append(f"\n**📌 Zusatzinfo:** {self.details.value}")

                

                await result_channel.send(

                    "\n".join(message_content),

                    embed=embed

                )

            

            await self.message.edit(embed=embed, view=None)

            await interaction.response.send_message("Akzeptiert! ✅", ephemeral=True)

        except Exception as e:

            await interaction.response.send_message(

                f"❌ Fehler: {str(e)}",

                ephemeral=True

            )

class RejectionModal(ui.Modal, title='Ablehnungsgrund'):

    reason = ui.TextInput(

        label='Begründung (sei konstruktiv!)',

        style=discord.TextStyle.long,

        required=True

    )

    def __init__(self, message):

        super().__init__()

        self.message = message

    async def on_submit(self, interaction: discord.Interaction):

        try:

            embed = self.message.embeds[0]

            embed.color = 0xED4245

            embed.title = "❌ Idee abgelehnt"

            embed.add_field(name="Begründung", value=self.reason.value, inline=False)

            

            submitter_id = int(embed.footer.text.split("ID: ")[1])

            submitter = interaction.guild.get_member(submitter_id)

            

            # An ERGEBNIS-Kanal senden

            result_channel = interaction.client.get_channel(1357408883358044301)

            if result_channel:

                await result_channel.send(

                    f"{submitter.mention if submitter else 'Der Nutzer'} deine Idee wurde leider abgelehnt 😢\n"

                    f"**Original-Idee:** {embed.description}\n"

                    f"**Grund:** {self.reason.value}",

                    embed=embed

                )

            

            await self.message.edit(embed=embed, view=None)

            await interaction.response.send_message("Ablehnung gespeichert!", ephemeral=True)

        except Exception as e:

            await interaction.response.send_message(

                f"❌ Fehler: {str(e)}",

                ephemeral=True

            )

class IdeaModal(ui.Modal, title='Deine geniale Idee für Echo!'):

    idea = ui.TextInput(

        label='Was soll Echo können?',

        style=discord.TextStyle.long,

        placeholder="Wie wärs mit einem Befehl der Katzenbilder spamt? 😼",

        required=True

    )

    async def on_submit(self, interaction: discord.Interaction):

        try:

            embed = discord.Embed(

                title="💡 Neue Idee eingereicht!",

                description=self.idea.value,

                color=0xFEE75C,

                timestamp=datetime.datetime.now()

            )

            embed.set_footer(text=f"Eingereicht von {interaction.user} • ID: {interaction.user.id}")

            embed.set_thumbnail(url="https://i.imgur.com/7W7MWoX.png")

            view = IdeaButtons()

            # An MOD-REVIEW-Kanal senden

            review_channel = interaction.client.get_channel(1357409626194182296)

            if review_channel:

                await review_channel.send(

                    "🚨 **Neue Ideen-Alarm!** 🚨",

                    embed=embed,

                    view=view

                )

                await interaction.response.send_message(

                    "✅ Deine Idee wurde weitergeleitet! Unser Team prüft sie mit 🧐 und 🍵",

                    ephemeral=True

                )

            else:

                await interaction.response.send_message(

                    "❌ Review-Kanal nicht gefunden - bitte Admin informieren!",

                    ephemeral=True

                )

        except Exception as e:

            await interaction.response.send_message(

                f"❌ Huch! Fehler: {str(e)}",

                ephemeral=True

            )

class IdeaSystem(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.submit_channel_id = 1357408741430919169  # Einreichungskanal

        self.review_channel_id = 1357409626194182296  # Admin-Review-Kanal

        self.result_channel_id = 1357408883358044301  # Ergebnis-Kanal

    @commands.Cog.listener()

    async def on_ready(self):

        self.bot.add_view(IdeaButtons())

        

        # Start-Button im Einreichungskanal erstellen

        submit_channel = self.bot.get_channel(self.submit_channel_id)

        if submit_channel:

            async for message in submit_channel.history(limit=10):

                if message.author == self.bot.user and message.components:

                    return

                    

            embed = discord.Embed(

                title="💡 Echo-Ideenbox",

                description=(

                    "**Hast du eine geniale Idee?**\n\n"

                    "• Neue Features\n"

                    "• Verbesserungen\n"

                    "• Oder einfach was Lustiges!\n\n"

                    "**Workflow:**\n"

                    "1. Hier Idee einreichen\n"

                    "2. Mod-Team prüft im Review-Kanal\n"

                    "3. Ergebnis wird im Ergebnis-Kanal gepostet"

                ),

                color=0xFEE75C

            )

            

            view = ui.View()

            view.add_item(ui.Button(

                label="💡 Idee einreichen", 

                style=discord.ButtonStyle.blurple,

                custom_id="submit_idea",

                emoji="✨"

            ))

            

            await submit_channel.send(

                "**Echo sucht frische Ideen!**\n"

                "Was soll ich als nächstes lernen?",

                embed=embed,

                view=view

            )

    @commands.Cog.listener()

    async def on_interaction(self, interaction: discord.Interaction):

        if interaction.type == discord.InteractionType.component:

            if interaction.data.get("custom_id") == "submit_idea":

                await interaction.response.send_modal(IdeaModal())

async def setup(bot):

    await bot.add_cog(IdeaSystem(bot))
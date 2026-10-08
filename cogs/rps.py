import discord

from discord import app_commands, ui

from discord.ext import commands

import random

class RPSGegenBot(ui.View):

    def __init__(self):

        super().__init__(timeout=20)

        self.spieler_wahl = None

        self.bot_wahl = None

        self.ergebnis = None

    @ui.button(label="✊ Stein", style=discord.ButtonStyle.blurple, row=0)

    async def stein(self, interaction: discord.Interaction, button: ui.Button):

        await self.spiel_verarbeiten(interaction, "stein")

    @ui.button(label="✋ Papier", style=discord.ButtonStyle.green, row=0)

    async def papier(self, interaction: discord.Interaction, button: ui.Button):

        await self.spiel_verarbeiten(interaction, "papier")

    @ui.button(label="✌️ Schere", style=discord.ButtonStyle.red, row=0)

    async def schere(self, interaction: discord.Interaction, button: ui.Button):

        await self.spiel_verarbeiten(interaction, "schere")

    async def spiel_verarbeiten(self, interaction: discord.Interaction, wahl: str):

        self.spieler_wahl = wahl

        self.bot_wahl = random.choice(["stein", "papier", "schere"])

        

        # KORRIGIERTER BEREICH (Zeile 52-54)

        if self.spieler_wahl == self.bot_wahl:

            self.ergebnis = "unentschieden"

        elif ((self.spieler_wahl == "stein" and self.bot_wahl == "schere") or

              (self.spieler_wahl == "papier" and self.bot_wahl == "stein") or

              (self.spieler_wahl == "schere" and self.bot_wahl == "papier")):

            self.ergebnis = "gewonnen"

        else:

            self.ergebnis = "verloren"

        await self.ergebnis_anzeigen(interaction)

    async def ergebnis_anzeigen(self, interaction: discord.Interaction):

        for button in self.children:

            button.disabled = True

        emoji_map = {"stein": "✊", "papier": "✋", "schere": "✌️"}

        farben = {

            "gewonnen": discord.Color.green(),

            "verloren": discord.Color.red(),

            "unentschieden": discord.Color.gold()

        }

        embed = discord.Embed(

            title="🎮 Schere-Stein-Papier Ergebnis",

            color=farben[self.ergebnis]

        )

        embed.add_field(

            name="Deine Wahl",

            value=f"{emoji_map[self.spieler_wahl]} {self.spieler_wahl.capitalize()}",

            inline=True

        )

        embed.add_field(

            name="Bot's Wahl",

            value=f"{emoji_map[self.bot_wahl]} {self.bot_wahl.capitalize()}",

            inline=True

        )

        embed.add_field(

            name="Ergebnis",

            value="🎉 Du hast gewonnen!" if self.ergebnis == "gewonnen" else 

                 "😢 Du hast verloren!" if self.ergebnis == "verloren" else 

                 "🤝 Unentschieden!",

            inline=False

        )

        

        await interaction.response.edit_message(embed=embed, view=self)

class RPS(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @app_commands.command(name="rps", description="Spiele Schere-Stein-Papier gegen den Bot")

    async def rps(self, interaction: discord.Interaction):

        embed = discord.Embed(

            title="🎮 Schere-Stein-Papier",

            description="Wähle deine Attacke!",

            color=discord.Color.blue()

        )

        await interaction.response.send_message(embed=embed, view=RPSGegenBot())

async def setup(bot):

    await bot.add_cog(RPS(bot))
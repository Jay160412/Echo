import discord
from discord import app_commands
from discord.ext import commands
import random

# Liste von 50 Witzen
JOKES = [
    "Warum können Geister so schlecht lügen? Weil man durch sie hindurchsieht!",
    "Was macht ein Clown im Büro? Faxen!",
    "Warum haben Piraten kein Alphabet? Weil sie immer auf C stehen!",
    "Was ist rot und steht im Wald? Ein Kirsch!",
    "Warum gehen Hexen nicht ins Schwimmbad? Weil sie Angst vor dem Besen haben!",
    "Was ist das Gegenteil von Reformhaus? Reh hinterm Haus!",
    "Warum können Elefanten nicht schwimmen? Weil sie nur einen Badeanzug haben!",
    "Was ist grün und steht im Wald? Ein Klavier!",
    "Warum haben Vampire keine Freunde? Weil sie sich immer aus-saugen!",
    "Was ist weiß und rennt den Berg hoch? Eine Lawine mit Heimweh!",
    "Warum können Geister so schlecht lügen? Weil man durch sie hindurchsieht!",
    "Was macht ein Clown im Büro? Faxen!",
    "Warum haben Piraten kein Alphabet? Weil sie immer auf C stehen!",
    "Was ist rot und steht im Wald? Ein Kirsch!",
    "Warum gehen Hexen nicht ins Schwimmbad? Weil sie Angst vor dem Besen haben!",
    "Was ist das Gegenteil von Reformhaus? Reh hinterm Haus!",
    "Warum können Elefanten nicht schwimmen? Weil sie nur einen Badeanzug haben!",
    "Was ist grün und steht im Wald? Ein Klavier!",
    "Warum haben Vampire keine Freunde? Weil sie sich immer aus-saugen!",
    "Was ist weiß und rennt den Berg hoch? Eine Lawine mit Heimweh!",
    "Warum können Geister so schlecht lügen? Weil man durch sie hindurchsieht!",
    "Was macht ein Clown im Büro? Faxen!",
    "Warum haben Piraten kein Alphabet? Weil sie immer auf C stehen!",
    "Was ist rot und steht im Wald? Ein Kirsch!",
    "Warum gehen Hexen nicht ins Schwimmbad? Weil sie Angst vor dem Besen haben!",
    "Was ist das Gegenteil von Reformhaus? Reh hinterm Haus!",
    "Warum können Elefanten nicht schwimmen? Weil sie nur einen Badeanzug haben!",
    "Was ist grün und steht im Wald? Ein Klavier!",
    "Warum haben Vampire keine Freunde? Weil sie sich immer aus-saugen!",
    "Was ist weiß und rennt den Berg hoch? Eine Lawine mit Heimweh!",
    "Warum können Geister so schlecht lügen? Weil man durch sie hindurchsieht!",
    "Was macht ein Clown im Büro? Faxen!",
    "Warum haben Piraten kein Alphabet? Weil sie immer auf C stehen!",
    "Was ist rot und steht im Wald? Ein Kirsch!",
    "Warum gehen Hexen nicht ins Schwimmbad? Weil sie Angst vor dem Besen haben!",
    "Was ist das Gegenteil von Reformhaus? Reh hinterm Haus!",
    "Warum können Elefanten nicht schwimmen? Weil sie nur einen Badeanzug haben!",
    "Was ist grün und steht im Wald? Ein Klavier!",
    "Warum haben Vampire keine Freunde? Weil sie sich immer aus-saugen!",
    "Was ist weiß und rennt den Berg hoch? Eine Lawine mit Heimweh!",
    "Warum können Geister so schlecht lügen? Weil man durch sie hindurchsieht!",
    "Was macht ein Clown im Büro? Faxen!",
    "Warum haben Piraten kein Alphabet? Weil sie immer auf C stehen!",
    "Was ist rot und steht im Wald? Ein Kirsch!",
    "Warum gehen Hexen nicht ins Schwimmbad? Weil sie Angst vor dem Besen haben!",
    "Was ist das Gegenteil von Reformhaus? Reh hinterm Haus!",
    "Warum können Elefanten nicht schwimmen? Weil sie nur einen Badeanzug haben!",
    "Was ist grün und steht im Wald? Ein Klavier!",
    "Warum haben Vampire keine Freunde? Weil sie sich immer aus-saugen!",
    "Was ist weiß und rennt den Berg hoch? Eine Lawine mit Heimweh!"
]

class Joke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Slash-Command: /joke
    @app_commands.command(name="joke", description="Sendet einen zufälligen Witz.")
    async def joke(self, interaction: discord.Interaction):
        # Zufälligen Witz auswählen
        joke = random.choice(JOKES)
        await interaction.response.send_message(joke)

# Cog für den Bot registrieren
async def setup(bot):
    await bot.add_cog(Joke(bot))
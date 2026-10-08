import discord
from discord import app_commands, ui
from discord.ext import commands
import random

# Liste von 50 Quiz-Fragen und Antworten
QUIZ_QUESTIONS = [
    {"question": "Was ist die Hauptstadt von Frankreich?", "options": ["Berlin", "Paris", "Madrid", "Rom"], "correct_answer": "Paris"},
    {"question": "Wie viele Planeten hat unser Sonnensystem?", "options": ["7", "8", "9", "10"], "correct_answer": "8"},
    {"question": "Wer hat die Relativitätstheorie entwickelt?", "options": ["Isaac Newton", "Albert Einstein", "Stephen Hawking", "Nikola Tesla"], "correct_answer": "Albert Einstein"},
    {"question": "Was ist das größte Säugetier der Welt?", "options": ["Elefant", "Blauwal", "Giraffe", "Hai"], "correct_answer": "Blauwal"},
    {"question": "Welche Programmiersprache ist bekannt für ihre Verwendung in Webentwicklung?", "options": ["Python", "Java", "JavaScript", "C++"], "correct_answer": "JavaScript"},
    {"question": "Wie heißt der größte Ozean der Erde?", "options": ["Atlantik", "Indischer Ozean", "Pazifik", "Arktischer Ozean"], "correct_answer": "Pazifik"},
    {"question": "Welches Land hat die meisten Einwohner?", "options": ["Indien", "USA", "China", "Russland"], "correct_answer": "China"},
    {"question": "Wie viele Kontinente gibt es?", "options": ["5", "6", "7", "8"], "correct_answer": "7"},
    {"question": "Welches Element hat das chemische Symbol 'O'?", "options": ["Gold", "Sauerstoff", "Eisen", "Kohlenstoff"], "correct_answer": "Sauerstoff"},
    {"question": "Wer schrieb 'Romeo und Julia'?", "options": ["William Shakespeare", "Charles Dickens", "Mark Twain", "Jane Austen"], "correct_answer": "William Shakespeare"},
    {"question": "Was ist die Hauptstadt von Japan?", "options": ["Peking", "Seoul", "Tokio", "Bangkok"], "correct_answer": "Tokio"},
    {"question": "Wie viele Tage hat ein Schaltjahr?", "options": ["365", "366", "364", "367"], "correct_answer": "366"},
    {"question": "Welcher Planet ist der Sonne am nächsten?", "options": ["Venus", "Mars", "Merkur", "Erde"], "correct_answer": "Merkur"},
    {"question": "Welches Tier ist das schnellste Landtier?", "options": ["Gepard", "Löwe", "Pferd", "Windhund"], "correct_answer": "Gepard"},
    {"question": "Welches Land ist bekannt für die Pyramiden von Gizeh?", "options": ["Mexiko", "Ägypten", "Griechenland", "Italien"], "correct_answer": "Ägypten"},
    {"question": "Welches ist das kleinste Land der Welt?", "options": ["Monaco", "Vatikanstadt", "San Marino", "Liechtenstein"], "correct_answer": "Vatikanstadt"},
    {"question": "Welcher Fluss ist der längste der Welt?", "options": ["Amazonas", "Nil", "Jangtse", "Mississippi"], "correct_answer": "Nil"},
    {"question": "Welches Land hat die Form eines Stiefels?", "options": ["Frankreich", "Italien", "Spanien", "Griechenland"], "correct_answer": "Italien"},
    {"question": "Welcher Planet wird als 'Roter Planet' bezeichnet?", "options": ["Venus", "Mars", "Jupiter", "Saturn"], "correct_answer": "Mars"},
    {"question": "Welches Tier ist das größte Reptil?", "options": ["Krokodil", "Komodowaran", "Schlange", "Schildkröte"], "correct_answer": "Komodowaran"},
    {"question": "Welches Land ist bekannt für das Taj Mahal?", "options": ["Indien", "Pakistan", "Bangladesch", "Nepal"], "correct_answer": "Indien"},
    {"question": "Welcher Kontinent ist der kleinste?", "options": ["Afrika", "Europa", "Australien", "Antarktis"], "correct_answer": "Australien"},
    {"question": "Welches Land ist bekannt für die Erfindung der Pizza?", "options": ["Frankreich", "Italien", "Spanien", "Griechenland"], "correct_answer": "Italien"},
    {"question": "Welcher Planet hat die meisten Monde?", "options": ["Jupiter", "Saturn", "Uranus", "Neptun"], "correct_answer": "Saturn"},
    {"question": "Welches Tier ist das größte an Land lebende Tier?", "options": ["Elefant", "Nashorn", "Nilpferd", "Giraffe"], "correct_answer": "Elefant"},
    {"question": "Welches Land ist bekannt für die Erfindung des Automobils?", "options": ["USA", "Deutschland", "Frankreich", "Japan"], "correct_answer": "Deutschland"},
    {"question": "Welcher Berg ist der höchste der Welt?", "options": ["K2", "Mount Everest", "Kangchendzönga", "Lhotse"], "correct_answer": "Mount Everest"},
    {"question": "Welches Land ist bekannt für die Erfindung des Kaffees?", "options": ["Brasilien", "Äthiopien", "Kolumbien", "Vietnam"], "correct_answer": "Äthiopien"},
    {"question": "Welcher Fluss fließt durch Paris?", "options": ["Themse", "Seine", "Donau", "Rhein"], "correct_answer": "Seine"},
    {"question": "Welches Land ist bekannt für die Erfindung des Tees?", "options": ["China", "Indien", "Japan", "Sri Lanka"], "correct_answer": "China"},
    {"question": "Welcher Planet ist der Erde am nächsten?", "options": ["Venus", "Mars", "Merkur", "Jupiter"], "correct_answer": "Venus"},
    {"question": "Welches Tier ist das größte im Wasser lebende Tier?", "options": ["Blauwal", "Hai", "Orca", "Riesenkalmar"], "correct_answer": "Blauwal"},
    {"question": "Welches Land ist bekannt für die Erfindung der Demokratie?", "options": ["Italien", "Griechenland", "Frankreich", "USA"], "correct_answer": "Griechenland"},
    {"question": "Welcher Fluss ist der längste in Europa?", "options": ["Donau", "Wolga", "Rhein", "Elbe"], "correct_answer": "Wolga"},
    {"question": "Welches Land ist bekannt für die Erfindung der Glühbirne?", "options": ["USA", "Deutschland", "Großbritannien", "Frankreich"], "correct_answer": "USA"},
    {"question": "Welcher Planet ist der kälteste?", "options": ["Uranus", "Neptun", "Saturn", "Pluto"], "correct_answer": "Uranus"},
    {"question": "Welches Tier ist das schnellste im Wasser?", "options": ["Delfin", "Hai", "Schwertfisch", "Orca"], "correct_answer": "Schwertfisch"},
    {"question": "Welches Land ist bekannt für die Erfindung des Radios?", "options": ["Italien", "USA", "Großbritannien", "Deutschland"], "correct_answer": "Italien"},
    {"question": "Welcher Fluss fließt durch London?", "options": ["Themse", "Seine", "Donau", "Rhein"], "correct_answer": "Themse"},
    {"question": "Welches Land ist bekannt für die Erfindung des Telefons?", "options": ["USA", "Deutschland", "Großbritannien", "Frankreich"], "correct_answer": "USA"},
    {"question": "Welcher Planet ist der größte im Sonnensystem?", "options": ["Jupiter", "Saturn", "Uranus", "Neptun"], "correct_answer": "Jupiter"},
    {"question": "Welches Tier ist das größte Vogel?", "options": ["Strauß", "Adler", "Kondor", "Pelikan"], "correct_answer": "Strauß"},
    {"question": "Welches Land ist bekannt für die Erfindung des Computers?", "options": ["USA", "Deutschland", "Großbritannien", "Frankreich"], "correct_answer": "USA"},
    {"question": "Welcher Fluss fließt durch Rom?", "options": ["Tiber", "Seine", "Donau", "Rhein"], "correct_answer": "Tiber"},
    {"question": "Welches Land ist bekannt für die Erfindung des Internets?", "options": ["USA", "Deutschland", "Großbritannien", "Frankreich"], "correct_answer": "USA"},
    {"question": "Welcher Planet ist der kleinste im Sonnensystem?", "options": ["Merkur", "Venus", "Erde", "Mars"], "correct_answer": "Merkur"},
    {"question": "Welches Tier ist das größte Säugetier an Land?", "options": ["Elefant", "Nashorn", "Nilpferd", "Giraffe"], "correct_answer": "Elefant"},
    {"question": "Welches Land ist bekannt für die Erfindung des Fernsehens?", "options": ["USA", "Deutschland", "Großbritannien", "Frankreich"], "correct_answer": "USA"},
    {"question": "Welcher Fluss fließt durch New York?", "options": ["Hudson", "Mississippi", "Colorado", "Ohio"], "correct_answer": "Hudson"},
    {"question": "Welches Land ist bekannt für die Erfindung des Flugzeugs?", "options": ["USA", "Deutschland", "Großbritannien", "Frankreich"], "correct_answer": "USA"},
    {"question": "Welcher Planet ist der heißeste?", "options": ["Venus", "Merkur", "Mars", "Jupiter"], "correct_answer": "Venus"},
]

class QuizView(ui.View):
    def __init__(self, question_data, timeout=None):
        super().__init__(timeout=timeout)
        self.question_data = question_data
        self.correct_answer = question_data["correct_answer"]

        # Buttons für jede Antwortmöglichkeit erstellen
        for option in question_data["options"]:
            self.add_item(QuizButton(option, self.correct_answer))

class QuizButton(ui.Button):
    def __init__(self, label, correct_answer):
        super().__init__(style=discord.ButtonStyle.primary, label=label)
        self.correct_answer = correct_answer

    async def callback(self, interaction: discord.Interaction):
        if self.label == self.correct_answer:
            await interaction.response.send_message("✅ Richtig! Gut gemacht!", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ Falsch! Die richtige Antwort war: **{self.correct_answer}**", ephemeral=True)

class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Slash-Command: /quiz
    @app_commands.command(name="quiz", description="Starte ein Quiz-Spiel.")
    async def quiz(self, interaction: discord.Interaction):
        # Zufällige Frage auswählen
        question_data = random.choice(QUIZ_QUESTIONS)

        # Quiz-View erstellen und senden
        view = QuizView(question_data)
        await interaction.response.send_message(
            f"❓ **Frage:** {question_data['question']}\n\n"
            "Wähle die richtige Antwort aus:",
            view=view
        )

# Cog für den Bot registrieren
async def setup(bot):
    await bot.add_cog(Quiz(bot))
import discord

from discord.ext import commands

from discord import app_commands

import random

from typing import List, Tuple

# Liste der Fragen (Frage, Option A, Option B)

WYR_QUESTIONS: List[Tuple[str, str, str]] = [

    ("Könntest du lieber fliegen oder unsichtbar sein?", "Fliegen", "Unsichtbar sein"),

    ("Würdest du lieber 10 Millionen Euro gewinnen oder die Fähigkeit haben, jede Sprache fließend zu sprechen?", "10 Millionen Euro", "Alle Sprachen sprechen"),

    ("Lieber nur noch Pizza oder nur noch Burger essen?", "Nur Pizza", "Nur Burger"),

    ("Lieber im Meer oder im Weltall leben?", "Im Meer", "Im Weltall"),

    ("Würdest du lieber 10 Jahre in die Vergangenheit reisen oder 10 Jahre in die Zukunft?", "10 Jahre zurück", "10 Jahre voraus"),

    ("Lieber niemals mehr telefonieren oder niemals mehr E-Mails schreiben?", "Kein Telefon", "Keine E-Mails"),

    ("Würdest du lieber 1 Milliarde Euro haben oder die Welt retten?", "1 Milliarde Euro", "Die Welt retten"),

    ("Lieber einen Tag als dein Haustier leben oder einen Tag als dein Lieblingspromi?", "Als Haustier", "Als Promi"),

    ("Würdest du lieber immer 5 Minuten zu spät kommen oder immer 30 Minuten zu früh?", "5 Minuten zu spät", "30 Minuten zu früh"),

    ("Lieber nur noch Filme aus den 80ern oder nur noch Filme aus den 2000ern sehen?", "80er Filme", "2000er Filme"),

    ("Würdest du lieber deinen schlimmsten Feind glücklich machen oder deinen besten Freund unglücklich?", "Feind glücklich", "Freund unglücklich"),

    ("Lieber in einem Schloss oder auf einer einsamen Insel wohnen?", "Im Schloss", "Auf der Insel"),

    ("Würdest du lieber einen Monat ohne Internet oder einen Monat ohne Strom leben?", "Kein Internet", "Kein Strom"),

    ("Lieber alle Tiere verstehen können oder alle Menschen?", "Tiere verstehen", "Menschen verstehen"),

    ("Würdest du lieber ein Buch schreiben oder einen Film drehen?", "Buch schreiben", "Film drehen"),

    ("Lieber für immer 12 Jahre alt oder für immer 60 Jahre alt sein?", "12 Jahre alt", "60 Jahre alt"),

    ("Würdest du lieber nie wieder lachen oder nie wieder weinen können?", "Nicht lachen", "Nicht weinen"),

    ("Lieber die Fähigkeit, die Zukunft zu sehen, oder die Vergangenheit zu ändern?", "Zukunft sehen", "Vergangenheit ändern"),

    ("Würdest du lieber auf einer Party der Star sein oder im Hintergrund bleiben?", "Star sein", "Im Hintergrund"),

    ("Lieber nur noch kalt duschen oder nur noch lauwarmes Essen?", "Kalt duschen", "Lauwarmes Essen"),

    ("Würdest du lieber alle Sprachen der Welt sprechen oder jedes Musikinstrument spielen können?", "Alle Sprachen", "Jedes Instrument"),

    ("Lieber 10 cm größer oder 10 cm kleiner sein?", "Größer", "Kleiner"),

    ("Würdest du lieber jeden Tag die gleiche Kleidung tragen oder jeden Tag das gleiche Essen?", "Gleiche Kleidung", "Gleiches Essen"),

    ("Lieber eine Woche ohne Smartphone oder eine Woche ohne Freunde?", "Ohne Smartphone", "Ohne Freunde"),

    ("Würdest du lieber die Fähigkeit haben, dich zu teleportieren oder Gedanken zu lesen?", "Teleportieren", "Gedanken lesen"),

    ("Lieber für immer in einem Fantasy-Roman oder in einem Science-Fiction-Film leben?", "Fantasy", "Science-Fiction"),

    ("Würdest du lieber einen Monat lang jeden Tag eine Stunde Werbung sehen oder einen Monat lang jeden Tag eine Stunde bei der Müllabfuhr mithelfen?", "Werbung sehen", "Müllabfuhr"),

    ("Lieber allein auf einer einsamen Insel oder mit einer Person, die du nicht leiden kannst?", "Allein", "Mit nerviger Person"),

    ("Würdest du lieber dein eigenes Haus entwerfen oder deinen eigenen Garten anlegen?", "Haus entwerfen", "Garten anlegen"),

    ("Lieber einen Monat lang nur im Sitzen oder nur im Stehen schlafen?", "Sitzen", "Stehen"),

    ("Würdest du lieber eine Woche ohne Schlaf auskommen oder eine Woche ohne Essen?", "Ohne Schlaf", "Ohne Essen"),

    ("Lieber in der Steinzeit oder in der Zukunft leben?", "Steinzeit", "Zukunft"),

    ("Würdest du lieber einen Oscar gewinnen oder einen Nobelpreis?", "Oscar", "Nobelpreis"),

    ("Lieber einen Tag mit deinem Idol verbringen oder einen Tag mit einem verstorbenen Familienmitglied?", "Mit Idol", "Mit Familienmitglied"),

    ("Würdest du lieber nie wieder krank werden oder nie wieder hungrig sein?", "Nie krank", "Nie hungrig"),

    ("Lieber alle Verkehrsmittel umsonst nutzen oder alle Eintritte umsonst?", "Umsonst Verkehr", "Umsonst Eintritte"),

    ("Würdest du lieber immer die richtige Lottozahl tippen oder immer den richtigen Aktienkurs vorhersagen?", "Lotto", "Aktien"),

    ("Lieber alle Erinnerungen an eine gute Zeit verlieren oder eine schlimme Zeit doppelt so intensiv erinnern?", "Gute Zeit vergessen", "Schlimme Zeit intensiver"),

    ("Würdest du lieber in einer Welt ohne Regeln oder in einer Welt ohne Gesetze leben?", "Ohne Regeln", "Ohne Gesetze"),

    ("Lieber in einer riesigen Villa mit nur einem Raum oder in einer winzigen Wohnung mit vielen Räumen?", "Riesige Villa", "Winzige Wohnung"),

    ("Würdest du lieber jede Minute deines Lebens aufzeichnen lassen oder nie wieder Fotos machen?", "Aufzeichnung", "Nie Fotos"),

    ("Lieber einen neuen besten Freund finden oder eine neue große Liebe?", "Besten Freund", "Große Liebe"),

    ("Würdest du lieber für immer in einem Land mit Schnee oder mit Strand leben?", "Schnee", "Strand"),

    ("Lieber deine Vergangenheit ändern oder deine Zukunft kontrollieren?", "Vergangenheit ändern", "Zukunft kontrollieren"),

    ("Würdest du lieber ein Genie sein, aber kein soziales Leben haben, oder durchschnittlich, aber viele Freunde?", "Genie", "Durchschnitt"),

    ("Lieber jeden Tag eine neue Fähigkeit lernen oder jeden Tag eine neue Sprache?", "Neue Fähigkeit", "Neue Sprache"),

    ("Würdest du lieber die Stimme von Morgan Freeman haben oder die Singstimme von Beyoncé?", "Morgan Freeman", "Beyoncé"),

    ("Lieber einen Tag lang unendlich viel essen können oder einen Tag lang unendlich viel schlafen?", "Essen", "Schlafen"),

    ("Würdest du lieber dein Leben als Film oder als Buch sehen?", "Als Film", "Als Buch"),

    ("Lieber in einem Haus ohne Heizung oder ohne Klimaanlage leben?", "Ohne Heizung", "Ohne Klima"),

    ("Würdest du lieber nie wieder Serien oder nie wieder Filme schauen?", "Keine Serien", "Keine Filme"),

    # Erweitere nach Belieben – hier sind 50 Beispiele; du kannst weitere hinzufügen

]

class WYRView(discord.ui.View):

    def __init__(self, question: str, option_a: str, option_b: str):

        super().__init__(timeout=60)  # Buttons bleiben 60 Sekunden aktiv

        self.question = question

        self.option_a = option_a

        self.option_b = option_b

    @discord.ui.button(label="Option A", style=discord.ButtonStyle.primary, emoji="🅰️")

    async def option_a_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_message(

            f"Du hast **Option A** gewählt: {self.option_a}",

            ephemeral=True

        )

    @discord.ui.button(label="Option B", style=discord.ButtonStyle.secondary, emoji="🅱️")

    async def option_b_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_message(

            f"Du hast **Option B** gewählt: {self.option_b}",

            ephemeral=True

        )

class WYR(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @app_commands.command(name="wyr", description="Stellt eine 'Would You Rather'-Frage")

    async def wyr(self, interaction: discord.Interaction):

        # Zufällige Frage auswählen

        question, opt_a, opt_b = random.choice(WYR_QUESTIONS)

        # Embed erstellen

        embed = discord.Embed(

            title="❓ Would You Rather …",

            description=question,

            color=discord.Color.random()

        )

        embed.add_field(name="🅰️ Option A", value=opt_a, inline=False)

        embed.add_field(name="🅱️ Option B", value=opt_b, inline=False)

        embed.set_footer(text="Klicke auf einen Button, um deine Wahl zu treffen.")

        # View mit Buttons senden

        view = WYRView(question, opt_a, opt_b)

        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):

    await bot.add_cog(WYR(bot))
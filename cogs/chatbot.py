import discord

from discord.ext import commands

from discord import app_commands

import asyncio

import random

import time

from collections import deque

import groq

import os

# ============================================

# DEIN API-KEY

# ============================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ============================================

# GROQ CLIENT (ASYNC)

# ============================================

groq_client = groq.AsyncGroq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

class Chatbot(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.user_history = {}

        self.request_times = deque(maxlen=60)

    async def rate_limit_check(self):

        now = time.time()

        while self.request_times and now - self.request_times[0] > 60:

            self.request_times.popleft()

        if len(self.request_times) >= 25:

            await asyncio.sleep(1)

            return await self.rate_limit_check()

        self.request_times.append(now)

        return True

    def get_command_list(self):

        """Erzeugt eine kurze Auflistung wichtiger Befehle für den Prompt."""

        commands = self.bot.tree.get_commands()

        important = ["/commandlist", "/owner", "/serverinfo", "/autoanswer", "/rolemenu", "/ticket", "/welcomeenable"]

        lines = [f"`{cmd.name}` – {cmd.description}" for cmd in commands if cmd.name in important]

        if not lines:

            lines = ["`/commandlist` – Zeigt alle Befehle an"]

        return "\n".join(lines)

    def build_system_prompt(self):

        """Erzeugt den vollständigen System‑Prompt mit allen Infos und FAQs."""

        command_overview = self.get_command_list()

        return (

            "Du bist ein freundlicher Discord‑Bot namens Echo. "

            "Antworte auf Deutsch, kurz und hilfreich.\n\n"

            "**Über Echo:**\n"

            "Echo ist ein vielseitiger Bot mit vielen Funktionen: Willkommens‑ und Abschiedsnachrichten, "

            "Auto‑Antworten, Auto‑Reaktionen, Ticket‑System, Rollen‑Menüs, Levels, Quiz, Witze, Memes, "

            "Bump‑System, und vieles mehr. Eine vollständige Liste aller Befehle erhältst du mit `/commandlist`.\n\n"

            "**Owner:**\n"

            "Der Besitzer von Echo heißt `jay_160412`. Bei Fragen oder Problemen kannst du ihn auf dem Support‑Server erreichen.\n\n"

            "**Links:**\n"

            "- Support‑Server: https://discord.gg/uNVnWredk2\n"

            "- Owner‑TikTok: https://www.tiktok.com/@jay__tiktok?_r=1&_t=ZG-94sDCErCnqK\n"

            "- Owner‑Webseite: https://jaywebsite.vercel.app\n\n"

            "**Wichtige Befehle:**\n"

            f"{command_overview}\n\n"

            "**Häufige Fragen (FAQs):**\n"

            "- **Wer hat dich erstellt?** → Mich hat `jay_160412` entwickelt! Er ist der Owner von Echo.\n"

            "- **Was kannst du?** → Ich kann viele Dinge: Willkommensnachrichten, Tickets, Rollen‑Menüs, Level, Quiz, Witze, Memes, Serverinfo und mehr. Mit `/commandlist` siehst du alle Befehle!\n"

            "- **Wie füge ich dich zu meinem Server hinzu?** → Lade mich über den Discord Developer Portal oder frage den Owner nach dem Einladungslink. Hilfe gibt es im Support‑Server.\n"

            "- **Kostet dich etwas?** → Nein, ich bin komplett kostenlos!\n"

            "- **Wo finde ich Hilfe?** → Auf unserem Support‑Server: https://discord.gg/uNVnWredk2. Dort gibt es Hilfe, Updates und du kannst Fragen stellen!\n"

            "- **Wie erreiche ich den Owner?** → Der Owner heißt **jay_160412**. Du kannst ihn auf Discord direkt anschreiben oder auf dem Support‑Server erwähnen.\n"

            "- **Kann ich Fehler melden?** → Ja, melde Fehler bitte auf dem Support‑Server im Channel **#support**. Danke für deine Hilfe!\n"

            "- **Wie aktiviere ich das Welcome‑System?** → Mit `/welcomeenable` und den entsprechenden Kanälen. Für Hilfe schau in der Befehlsliste nach.\n"

            "- **Wie erstelle ich ein Rollen‑Menü?** → Nutze `/rolemenu` und gib die gewünschten Rollen an. Das Menü wird dann im ausgewählten Kanal erstellt.\n"

            "- **Wie funktioniert das Ticket‑System?** → Aktiviere es mit `/ticketenable`. Nutzer können dann ein Ticket erstellen, das in einem privaten Kanal bearbeitet wird.\n"

            "- **Kann ich eigene Auto‑Antworten einrichten?** → Ja! Mit `/autoanswer` legst du Trigger und Antwort fest. Optional kannst du auch Kanäle auswählen.\n"

            "- **Warum antwortest du nicht?** → Prüfe bitte: 1) Hast du mich erwähnt (`@Echo`)? 2) Hat der Bot Lese‑/Schreibrechte im Kanal? 3) Funktioniert die API? Wenn nichts hilft, melde dich im Support‑Server.\n"

            "- **Ein Befehl funktioniert nicht. Was tun?** → Stelle sicher, dass der Bot die nötigen Berechtigungen hat. Falls es ein Fehler ist, melde ihn bitte auf dem Support‑Server (#support)!\n"

            "- **Wie aktualisiere ich den Bot?** → Der Bot wird automatisch aktualisiert, wenn der Owner neue Versionen deployt.\n"

            "- **Hast du eine Webseite?** → Ja! Die Webseite des Owners findest du hier: https://jaywebsite.vercel.app\n"

            "- **Gibt es Updates?** → Ja, alle Neuigkeiten posten wir auf dem Support‑Server und manchmal auch auf dem TikTok‑Kanal des Owners.\n"

            "- **Kann ich dich unterstützen?** → Auf jeden Fall! Teile den Bot mit Freunden, melde Bugs oder helfe im Support‑Server mit!\n\n"

            "Wenn ein Nutzer nach deinen Fähigkeiten fragt, kannst du auf `/commandlist` verweisen oder "
            
            "wenn es um deinen Macher/Owner geht, erwähne oft seine Webseite und das er TikTok hat, aber nur wenn auch wirklich nach dem Owner gefragt wird"
            
            "In der Webseite deines Machers sind du der Bot, der Discord Server vom Bot, Social Media Plattformen deines Owners und weitere Sachen verlinkt, die Webseite ist: https://jaywebsite.vercel.app"

            "gezielt einen Befehl erklären. Sei immer freundlich und hilfsbereit."

        )

    async def get_groq_response(self, messages):

        if groq_client is None:
            print("GROQ_API_KEY fehlt; die KI-Chatfunktion ist nicht verfügbar.")
            return None

        try:

            response = await groq_client.chat.completions.create(

                model="openai/gpt-oss-120b",

                messages=messages,

                temperature=0.7,

                max_tokens=500

            )

            return response.choices[0].message.content.strip()

        except Exception as e:

            print(f"Groq Fehler: {e}")

            return None

    async def get_ai_response(self, user_id: int, prompt: str) -> str:

        await self.rate_limit_check()

        if user_id not in self.user_history:

            self.user_history[user_id] = []

        system_prompt = self.build_system_prompt()

        system_msg = {"role": "system", "content": system_prompt}

        context = self.user_history[user_id][-5:]  # letzte 5 Nachrichten

        messages = [system_msg] + context + [{"role": "user", "content": prompt}]

        response = await self.get_groq_response(messages)

        if response:

            self.user_history[user_id].append({"role": "user", "content": prompt})

            self.user_history[user_id].append({"role": "assistant", "content": response})

            return response

        else:

            return "Entschuldigung, ich habe gerade technische Probleme 😅"

    @commands.Cog.listener()

    async def on_message(self, message: discord.Message):

        if message.author == self.bot.user:

            return

        if self.bot.user in message.mentions:

            prompt = message.clean_content.replace(f"@{self.bot.user.name}", "").strip()

            prompt = prompt.replace(f"@{self.bot.user.display_name}", "").strip()

            if not prompt:

                await message.channel.send(

                    f"Hallo {message.author.mention}! 👋\n"

                    "Schreib deine Frage einfach nach @Echo, z.B. `@Echo Wie geht es dir?`"

                )

                return

            async with message.channel.typing():

                antwort = await self.get_ai_response(message.author.id, prompt)

            await message.channel.send(f"{message.author.mention} {antwort}")

    @app_commands.command(name="reset-chat", description="Löscht deinen Gesprächsverlauf mit dem Bot")

    async def reset_chat(self, interaction: discord.Interaction):

        user_id = interaction.user.id

        if user_id in self.user_history:

            del self.user_history[user_id]

        await interaction.response.send_message(

            "✅ Dein Gesprächsverlauf wurde gelöscht!",

            ephemeral=True

        )

async def setup(bot):

    await bot.add_cog(Chatbot(bot))
import random
import discord
from discord.ext import commands
from discord import ui, app_commands
from typing import Optional

class RoastMenu(ui.View):

    def __init__(self, target: discord.Member, roasts: dict):

        super().__init__(timeout=30)

        self.target = target

        self.roasts = roasts

        self.response: Optional[discord.Interaction] = None

    @ui.select(

        placeholder="Wähle dein Roast-Level...",

        options=[

            discord.SelectOption(label="😊 Harmlos", value="1", emoji="😊"),

            discord.SelectOption(label="🔥 Mittel", value="2", emoji="🔥"),

            discord.SelectOption(label="💀 Nuklear", value="3", emoji="💀"),

            discord.SelectOption(label="🎭 Persönlich", value="4", emoji="🎭"),

        ]

    )

    async def select_roast(self, interaction: discord.Interaction, select: ui.Select):

        if interaction.user != self.target:

            await interaction.response.send_message("❌ Nur das Ziel darf auswählen!", ephemeral=True)

            return

        level = int(select.values[0]) if select.values[0] != "4" else "personalized"

        roast = self.get_roast(level)

        

        await interaction.response.edit_message(

            content=f"**{interaction.user.mention} hat gewählt:**\n{roast}",

            view=None

        )

        self.response = interaction

        self.stop()

    def get_roast(self, level: int | str) -> str:

        if isinstance(level, int):

            pool = self.roasts[f"tier{level}"]

        else:

            traits = ["geek", "gamer", "weeb"]

            pool = random.choice([self.roasts["personalized"][t] for t in traits])

        

        return random.choice(pool).format(user=self.target.mention)

class RoastSystem(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.roast_db = {

            "tier1": [

                "{user} ist so langsam, Windows Updates sind schneller fertig!",

                "{user}'s Coding Skills sind wie ein Quantum Computer - niemand versteht's!",

                "{user} denkt 'sudo' heißt 'Superuser Dumb Operator'!",

                "{user} hat so viele Bugs im Code, selbst Pest Control kapituliert!",

                "{user}'s beste Programmiersprache ist PowerPoint!",

                "{user} nutzt Stack Overflow als IDE!",

                "{user} kompiliert mit 'magic.exe'!",

                "{user}'s Docker-Container enthalten nur Buffet-Reste!",

                "{user} debuggt mit print('Hilfe!')!",

                "{user} denkt JSON ist eine Energy Drink Marke!",

                "{user}'s GitHub besteht nur aus 'git clone' Befehlen!",

                "{user} hat 'Hello World' als Lebensziel!",

                "{user} nutzt Internet Explorer als Standard-Browser!",

                "{user}'s Python-Skills sind snake oil!",

                "{user} denkt '404' ist eine Wohnungsnummer!"

            ],

            

            "tier2": [

                "{user} ist so lost, selbst Google Maps kann ihn nicht finden!",

                "{user}'s Lebenslauf hat mehr Lücken als Swiss Cheese!",

                "{user} hat mehr Memory Leaks als Internet Explorer!",

                "{user} ist so unlucky, selbst 'rm -rf /' würde bei ihm fehlschlagen!",

                "{user}'s Code ist so messy, selbst Black Formatter gibt auf!",

                "{user} denkt TypeScript ist ein Schreibfehler!",

                "{user}'s API-Endpoints return 418 (I'm a teapot)!",

                "{user} hat mehr deprecated Funktionen als Windows XP!",

                "{user}'s Code-Reviews dauern länger als die Bauzeit der Pyramiden!",

                "{user} nutzt 'Leerzeichen statt Tabs' - wie ein Psychopath!",

                "{user}'s Algorithmen haben O(∞) Komplexität!",

                "{user} pushed direkt auf main - ohne Fragen!",

                "{user}'s IDE zeigt nur 'Syntax Error' an!",

                "{user} hat mehr Stack Traces als tatsächlichen Code!",

                "{user} denkt 'Machine Learning' bedeutet, dass die Maschine von selbst lernt!",

                "{user}'s Code hat mehr Backdoors als ein Ikea-Regal!",

                "{user} committet Passwörter im Klartext - als Feature!",

                "{user} denkt 'Blockchain' ist ein neues Lego-Set!",

                "{user}'s Code Coverage liegt bei -5%!",

                "{user} hat mehr segfaults als ein NASA-Computer!"

            ],

            

            "tier3": [

                "{user} ist so nutzlos wie 'sudo apt-get install common-sense'!",

                "{user}'s Existenz ist ein Race Condition!",

                "{user} hat mehr Memory Leaks als Chernobyl!",

                "{user} ist der Grund warum StackOverflow ein 'Rate Limit' hat!",

                "{user}'s Code ist so toxisch, selbst Rust's Borrow Checker weint!",

                "{user} ist der menschliche Äquivalent zu 'NaN'!",

                "{user} hat mehr Bugs als ein Bethesda-Spiel!",

                "{user}'s Lebenslauf ist wie ein 404-CV!",

                "{user} ist so ineffizient, selbst Bubble Sort ist schneller!",

                "{user} denkt 'GPU' heißt 'Gaming Pizza Unit'!",

                "{user}'s Code ist so schlecht, selbst GPT-4 kann ihn nicht erklären!",

                "{user} hat mehr Technical Debt als die Deutsche Bahn!",

                "{user} ist der Grund warum 'YAGNI' erfunden wurde!",

                "{user}'s UX-Design ist wie ein VCR im Jahr 2050!",

                "{user} ist so irrelevant, selbst 'Hello World' ignoriert ihn!"

            ],

            

            "personalized": {

                "geek": [

                    "{user}'s IDE zeigt nur 'Hello World' Beispiele an!",

                    "{user} denkt 'Python' ist eine Schlange im Zoo!",

                    "{user}'s Code ist so unlesbar, selbst der Autor versteht ihn nicht!",

                    "{user} hat mehr ungepushte Commits als Lebensentscheidungen!",

                    "{user} denkt 'Linux' ist eine afrikanische Antilope!"

                ],

                "gamer": [

                    "{user} spielt so schlecht, selbst NPCs looten ihn!",

                    "{user}'s K/D Ratio ist negativ!",

                    "{user} wurde von Minecraft Creepers geblockt!",

                    "{user} hat mehr Lag als ein Dial-Up Internet!",

                    "{user}'s Gaming-Skills sind wie Day-One Patches - immer zu spät!"

                ],

                "weeb": [

                    "{user}'s Waifu existiert nicht mal in 2D!",

                    "{user} denkt 'Baka' ist ein Programmiersprache!",

                    "{user}'s Anime-Liste ist voller Fillers!",

                    "{user} hat mehr Tsundere-Momente als ein Hauptcharakter!",

                    "{user}'s Japanisch-Kenntnisse stammen nur von Untertiteln!"

                ]

            }

        }

    @app_commands.command(name="roast", description="Lass das Ziel selbst entscheiden, wie hart es wird")

    async def roast(self, interaction: discord.Interaction, user: discord.Member):

        """Interaktives Roasting mit Zielauswahl"""

        if user.bot:

            return await interaction.response.send_message("🤖 Bots kann man nicht roasten!", ephemeral=True)

        view = RoastMenu(target=user, roasts=self.roast_db)

        await interaction.response.send_message(

            f"**{user.mention} darf jetzt entscheiden:**\nWie hart soll dein Roast sein?",

            view=view

        )

        

        await view.wait()

        if not view.response:

            await interaction.edit_original_response(

                content=f"⏰ {user.mention} hat zu lange gebraucht... Pech gehabt!",

                view=None

            )

async def setup(bot):

    await bot.add_cog(RoastSystem(bot))
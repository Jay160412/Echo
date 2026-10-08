import discord

from discord.ext import commands

from discord import app_commands, ui

class LanguageButtons(ui.View):

    def __init__(self):

        super().__init__(timeout=None)

    

    @ui.button(label="🇩🇪 Deutsch", style=discord.ButtonStyle.blurple, custom_id="german_rules", emoji="🇩🇪")

    async def german_button(self, interaction: discord.Interaction, button: ui.Button):

        rules_embed = discord.Embed(

            title="📜 Echo's Höllenhunde-Regeln 🇩🇪",

            color=0x5865F2,

            description=(

                "**Sprache / Language:** 🇬🇧 English (Wechsel unten)\n"

                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

                "**1. Seid nett!**\n"

                "> Behandelt andere wie Echo's Codebase – mit viel Geduld und gelegentlichem Neustart.\n\n"

                "**2. Kein Spam!**\n"

                "> Echo ist ein sehr sensibler Bot. 3x 'ping' und er weint sich in den Schlaf (true story).\n\n"

                "**3. Nochmal: Kein Spam!**\n"

                "> Sonst spamt Echo zurück mit 100x 'Never Gonna Give You Up'. *Wir warnen dich nicht nochmal.*\n\n"

                "**4. NSFW? Nice Try!**\n"

                "> Wir sind hier nicht bei 'OnlyBots'. Das Internet ist voller anderer Orte für... sowas.\n\n"

                "**5. Bug-Reports**\n"

                "> Found a bug? Congrats!\n> Öffne ein Ticket mit `/ticket` – Echo's Therapeut liest mit.\n\n"

                "**6. Have fun!**\n"

                "> Sonst verwandelt sich Echo in einen **`/boring-bot`**. Und das will niemand.\n"

                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

                "💡 PS: Echo's `/rps`-Betrugsrate liegt bei nur 87%. Trust us."

            )

        )

        await interaction.response.edit_message(embed=rules_embed, view=self)

    @ui.button(label="🇬🇧 English", style=discord.ButtonStyle.green, custom_id="english_rules", emoji="🇬🇧")

    async def english_button(self, interaction: discord.Interaction, button: ui.Button):

        rules_embed = discord.Embed(

            title="📜 Echo's Hellhounds Rules 🇬🇧",

            color=0x57F287,

            description=(

                "**Language / Sprache:** 🇩🇪 Deutsch (Switch below)\n"

                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

                "**1. Be nice!**\n"

                "> Treat others like Echo's codebase - with patience and occasional reboots.\n\n"

                "**2. No spam!**\n"

                "> Echo is a very sensitive bot. 3 'pings' and he'll cry himself to sleep (true story).\n\n"

                "**3. Again: No spam!**\n"

                "> Or Echo will retaliate with 100x 'Never Gonna Give You Up'. *Last warning.*\n\n"

                "**4. NSFW? Nice Try!**\n"

                "> This isn't 'OnlyBots'. The internet has other places for... that.\n\n"

                "**5. Bug Reports**\n"

                "> Found a bug? Congrats!\n> Open a ticket with `/ticket` - Echo's therapist is watching.\n\n"

                "**6. Have fun!**\n"

                "> Or Echo will transform into a **`/boring-bot`**. Nobody wants that.\n"

                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

                "💡 PS: Echo's `/rps` cheating rate is only 87%. Trust us."

            )

        )

        await interaction.response.edit_message(embed=rules_embed, view=self)

class RulesSystem(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    

    @app_commands.command(name="setrules", description="Erstellt die Regeln-Nachricht")

    @app_commands.default_permissions(administrator=True)

    @app_commands.describe(

        channel="Kanal für die Regeln",

    )

    async def set_rules(self, interaction: discord.Interaction, channel: discord.TextChannel):

        # Starte mit englischen Regeln als Standard

        rules_embed = discord.Embed(

            title="📜 Echo's Hellhounds Rules 🇬🇧",

            color=0x57F287,

            description=(

                "**Language / Sprache:** 🇩🇪 Deutsch (Switch below)\n"

                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

                "**1. Be nice!**\n"

                "> Treat others like Echo's codebase - with patience and occasional reboots.\n\n"

                "**2. No spam!**\n"

                "> Echo is a very sensitive bot. 3 'pings' and he'll cry himself to sleep (true story).\n\n"

                "**3. Again: No spam!**\n"

                "> Or Echo will retaliate with 100x 'Never Gonna Give You Up'. *Last warning.*\n\n"

                "**4. NSFW? Nice Try!**\n"

                "> This isn't 'OnlyBots'. The internet has other places for... that.\n\n"

                "**5. Bug Reports**\n"

                "> Found a bug? Congrats!\n> Open a ticket with `/ticket` - Echo's therapist is watching.\n\n"

                "**6. Have fun!**\n"

                "> Or Echo will transform into a **`/boring-bot`**. Nobody wants that.\n"

                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

                "💡 PS: Echo's `/rps` cheating rate is only 87%. Trust us."

            )

        )

        

        view = LanguageButtons()

        await channel.send(embed=rules_embed, view=view)

        await interaction.response.send_message("✅ Regeln erfolgreich erstellt!", ephemeral=True)

    @commands.Cog.listener()

    async def on_ready(self):

        self.bot.add_view(LanguageButtons())

async def setup(bot):

    await bot.add_cog(RulesSystem(bot))
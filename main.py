import discord
from discord.ext import commands
import os
import logging
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

# Logging konfigurieren
logging.basicConfig(level=logging.INFO)

# Intents konfigurieren
intents = discord.Intents.default()
intents.members = True  # Erforderlich für Welcome-/Bye-Events und vollständige Mitgliederlisten
intents.message_content = True  # Wichtig für das Lesen von Nachrichten

# Bot initialisieren
bot = commands.Bot(command_prefix="!", intents=intents)
bot.owner_id = 1254398312312868945

# Funktion zum Laden aller Cogs
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            cog_name = f"cogs.{filename[:-3]}"  # Entfernt ".py" aus dem Dateinamen
            try:
                await bot.load_extension(cog_name)
                logging.info(f"✅ Cog geladen: {cog_name}")
            except Exception as e:
                logging.error(f"❌ Fehler beim Laden von {cog_name}: {e}")

# Event: Wenn der Bot bereit ist
@bot.event
async def on_ready():
    logging.info(f"{bot.user} ist online!")

    # Slash-Commands synchronisieren
    synced_commands = await bot.tree.sync()
    logging.info(f"✅ {len(synced_commands)} Slash-Commands synchronisiert!")

    # Nachricht im News-Kanal posten (falls BotNews-Cog vorhanden ist)
    botnews_cog = bot.get_cog("BotNews")
    if botnews_cog:
        for guild in bot.guilds:
            await botnews_cog.post_news(str(guild.id), "🎉 Ein neuer Befehl wurde hinzugefügt: `/quiz`!")

# Bot starten
async def start_bot():
    await load_cogs()  # Lade alle Cogs
    await bot.start(TOKEN)
# Hauptprogramm
if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit(
            "DISCORD_TOKEN fehlt. Lege es in Replit unter Secrets an "
            "oder trage es lokal in Echo-main/.env ein."
        )
    import asyncio
    asyncio.run(start_bot())

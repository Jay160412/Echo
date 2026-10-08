import discord
from discord.ext import commands
import os
import logging
from dotenv import load_dotenv

# Wechsle in den Verzeichnis der Datei, damit relative Pfade immer funktionieren
os.chdir(os.path.dirname(os.path.abspath(__file__)))

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

# Flag für Slash-Command-Synchronisierung
_synced_once = False

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

# Setup-Hook für einmalige Initialisierung
async def setup_hook():
    global _synced_once
    if not _synced_once:
        synced_commands = await bot.tree.sync()
        logging.info(f"✅ {len(synced_commands)} Slash-Commands synchronisiert!")
        _synced_once = True

bot.setup_hook = setup_hook

# Event: Wenn der Bot bereit ist
@bot.event
async def on_ready():
    logging.info(f"{bot.user} ist online!")

# Bot starten
async def start_bot():
    await load_cogs()  # Lade alle Cogs
    await bot.start(TOKEN)

# Hauptprogramm
if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit(
            "DISCORD_TOKEN fehlt. Lege es als Umgebungsvariable an oder trage es in .env ein."
        )
    import asyncio
    asyncio.run(start_bot())

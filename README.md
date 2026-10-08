# Echo Discord Bot 🎵

Ein vielseitiger Discord Bot mit KI-Chatbot, Quiz, Ticket-System, Welcome-Events und mehr!

---

## 📋 Features

- 🤖 **KI-Chatbot** mit Groq API
- ❓ **Quiz-Minispiele**
- 🎫 **Ticket-System** für Support
- 📊 **Level- & XP-System**
- ⚠️ **Warn-System** für Moderation
- 👋 **Welcome/Goodbye-Events**
- 🔄 **Auto-Reaktionen & Auto-Reply**
- ⚙️ **Customizable Cogs-System**

---

## 🚀 Schnellstart

### 1️⃣ Lokal (Windows/macOS/Linux)

**Voraussetzungen:**
- Python 3.8+
- pip (Python Package Manager)

**Installation:**

```bash
# Repository klonen
git clone https://github.com/Jay160412/Echo.git
cd Echo

# Virtuelle Umgebung erstellen (optional aber empfohlen)
python -m venv .venv

# Virtuelle Umgebung aktivieren
# Linux/macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Abhängigkeiten installieren
pip install -r requirements.txt
```

### 2️⃣ Environment-Datei erstellen

```bash
# Kopiere die Vorlage
cp .env.example .env
```

Öffne `.env` und füge deine Tokens ein:

```env
DISCORD_TOKEN=dein_discord_bot_token
GROQ_API_KEY=dein_groq_api_key  # Optional, nur für KI-Features
```

> **Token finden:**
> - **DISCORD_TOKEN**: [Discord Developer Portal](https://discord.com/developers/applications) → Bot erstellen → Token kopieren
> - **GROQ_API_KEY**: [Groq Console](https://console.groq.com/keys) → API Key generieren

### 3️⃣ Bot starten

```bash
# Option A: Direkt
python main.py

# Option B: Mit Script (empfohlen)
bash scripts/run-echo-bot.sh
```

Wenn du keine Fehler siehst, ist der Bot erfolgreich gestartet! ✅

---

## ⚙️ Discord Developer Portal Setup

Damit der Bot vollständig funktioniert, musst du folgende Schritte im Discord Developer Portal machen:

1. Gehe zu [Discord Developer Portal](https://discord.com/developers/applications)
2. Wähle deine Bot-Anwendung aus
3. Gehe zu **Bot** → **TOKEN** und kopiere den Token (für `.env` DISCORD_TOKEN)

### Erforderliche Intents aktivieren:

Gehe zu **Bot** → **Privileged Gateway Intents** und aktiviere:
- ✅ **Message Content Intent** (Nachrichten lesen)
- ✅ **Server Members Intent** (für Welcome/Goodbye & vollständige Mitgliederlisten)

### Bot in deinen Server einladen:

1. Gehe zu **OAuth2** → **URL Generator**
2. Wähle folgende Scopes:
   - `bot`
3. Wähle folgende Permissions:
   - `Read/Send Messages`
   - `Manage Messages` (für Moderation)
   - `Add Reactions`
   - `Manage Roles` (für Rollen-Menüs)
   - `Manage Channels` (für Tickets)
4. Kopiere die generierte URL und öffne sie im Browser
5. Wähle deinen Server aus und bestätige

---

## 📝 Befehle testen

Nachdem der Bot online ist, teste diese Befehle:

```
/quiz          - Quiz starten
/help          - Hilfe anzeigen
!owner         - Owner-Befehle (nur für Bot-Owner)
```

Für andere Features schaue in den `cogs/` Dateien nach verfügbaren Befehlen.

---

## 🏗️ Projektstruktur

```
Echo/
├── main.py                 # Bot-Einstiegspunkt
├── requirements.txt        # Python-Abhängigkeiten
├── .env.example           # Template für Environment-Variablen
├── .gitignore             # Git-Ignore-Konfiguration
├── README.md              # Diese Datei
├── cogs/                  # Bot-Module (automatisch geladen)
│   ├── quiz.py
│   ├── ai_chatbot.py
│   ├── ticket_system.py
│   ├── level_system.py
│   ├── warn_system.py
│   ├── welcome.py
│   ├── botnews.py
│   └── ...
└── scripts/               # Deployment & Start-Skripte
    ├── build-echo-bot.sh  # Abhängigkeiten installieren
    └── run-echo-bot.sh    # Bot starten
```

---

## 🔧 Bot-Owner ID konfigurieren

In `main.py` Zeile 21 findest du:

```python
bot.owner_id = 1254398312312868945
```

**Ersetze diese ID mit deiner Discord-ID!** Finde deine ID mit einem dieser Befehle:
- Schreibe im Discord `\@dein_username` und kopiere die angezeigte ID
- Oder aktiviere **Entwickleroptionen** in Discord und nutze "Nutzer-ID kopieren"

Diese ID ist wichtig für Owner-only Befehle.

---

## 📦 Replit-Deployment

Falls du den Bot auf Replit hosten möchtest:

1. Fork dieses Repository auf GitHub
2. Erstelle ein neues Replit-Projekt und verbinde es mit deinem GitHub-Fork
3. Gehe zu **Secrets** (🔐) und trage ein:
   - `DISCORD_TOKEN` = dein Discord Token
   - `GROQ_API_KEY` = dein Groq API Key (optional)
4. Starte den Bot mit dem Befehl:
   ```
   bash scripts/run-echo-bot.sh
   ```
5. Für **Always-On** in Replit:
   - Wähle **Reserved VM** unter Veröffentlichungseinstellungen
   - Build-Command: `bash scripts/build-echo-bot.sh`
   - Run-Command: `bash scripts/run-echo-bot.sh`

---

## 🐛 Troubleshooting

### ❌ "DISCORD_TOKEN fehlt"
**Lösung:** Erstelle `.env` Datei und trage `DISCORD_TOKEN=...` ein
```bash
cp .env.example .env
# Dann .env bearbeiten
```

### ❌ "Module nicht gefunden" (ImportError)
**Lösung:** Installiere die Abhängigkeiten neu
```bash
pip install -r requirements.txt
```

### ❌ Bot ist online, aber Befehle funktionieren nicht
**Lösung:** Prüfe die Discord Developer Portal Intents:
- Message Content Intent ✅
- Server Members Intent ✅

### ❌ "Cog konnte nicht geladen werden"
**Lösung:** Prüfe die Logs in der Konsole. Der Fehler steht da und zeigt welche `.py`-Datei das Problem hat.

### ❌ Bot crasht nach kurzer Zeit
**Lösung:** Stelle sicher, dass:
- DISCORD_TOKEN gültig ist
- Bot-Token nicht geleakt wurde
- Bot hat die richtigen Permissions auf dem Server

---

## 📚 Weitere Ressourcen

- [discord.py Dokumentation](https://discordpy.readthedocs.io/)
- [Groq API Docs](https://console.groq.com/docs)
- [Discord Developer Docs](https://discord.com/developers/docs)

---

## 📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Weitere Infos in `LICENSE`.

---

## 💡 Support & Fragen

Falls du Fragen oder Probleme hast:
1. Schau ins `README.md` Troubleshooting
2. Prüfe die Bot-Logs in der Konsole
3. Schau die Cog-Dateien an für spezifische Befehle

---

**Version:** 1.0.0 | **Letztes Update:** 2026-10-08

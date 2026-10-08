# Echo Discord Bot

Dieser Bot benötigt eine .env Datei mit
einem Groq API Key und einem Discord Token,
So wird sie aufgebaut:

Position: Dort wo auch der cogs Ordner und main.py ist

Aufbau:
DISCORD_TOKEN=(dein_token_hier)
GROQ_API_KEY=(dein_groq_key_hier)I_KEY` ist optional und wird nur für die KI-Chatfunktion benötigt. Ohne
diesen Schlüssel starten die übrigen Bot-Funktionen weiterhin.

## Replit

Für den Betrieb in Replit keine `.env`-Datei mit echten Schlüsseln anlegen.
Stattdessen unter **Secrets** diese Variablen eintragen:

- `DISCORD_TOKEN` — erforderlich, Discord-Bot-Token
- `GROQ_API_KEY` — optional, für die KI-Chatfunktion

Zum dauerhaften Hosting in den Veröffentlichungseinstellungen **Reserved VM**
auswählen. Als Build-Befehl `bash scripts/build-echo-bot.sh` und als
Startbefehl `bash scripts/run-echo-bot.sh` verwenden.

Der Bot benötigt die privilegierten **Message Content Intent** und
**Server Members Intent**. Beide müssen im Discord Developer Portal für die
Bot-Anwendung aktiviert sein. Der Members-Intent wird für Welcome-/Bye-Events
und vollständige Mitgliederlisten benötigt.

Für Auto-Reaktionen braucht der Bot in den jeweiligen Kanälen **Kanal ansehen**,
**Nachrichtenverlauf ansehen** und **Reaktionen hinzufügen**. Für Rollen-Menüs
braucht er **Rollen verwalten**; seine höchste Serverrolle muss über allen
Rollen stehen, die er vergeben soll.
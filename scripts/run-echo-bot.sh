#!/usr/bin/env bash
# Echo Discord Bot - Run Script
# Startet den Discord Bot

set -e

echo "🚀 Starte Echo Discord Bot..."

if [ ! -f .env ]; then
    echo "❌ Fehler: .env wurde nicht gefunden."
    echo "   Kopiere zuerst .env.example nach .env und trage deine Token ein."
    echo "   Befehl: cp .env.example .env"
    exit 1
fi

if ! grep -q '^DISCORD_TOKEN=' .env; then
    echo "❌ Fehler: DISCORD_TOKEN fehlt in .env"
    exit 1
fi

python main.py

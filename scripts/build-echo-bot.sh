#!/usr/bin/env bash
# Echo Discord Bot - Build Script
# Installiert alle Python-Abhängigkeiten

set -e

echo "🔨 Echo Bot wird vorbereitet..."
echo "📦 Installiere Abhängigkeiten aus requirements.txt..."
pip install -r requirements.txt

echo "✅ Build abgeschlossen."
echo "➡️  Starte den Bot mit: bash scripts/run-echo-bot.sh"

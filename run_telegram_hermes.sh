#!/usr/bin/env bash
# Launcher for telegram_hermes.py
# Uses the dedicated venv with python-telegram-bot dependencies

cd "$(dirname "$0")" || exit 1

VENV="./venv_telegram"
if [ ! -d "$VENV" ]; then
    echo "[ERROR] venv_telegram not found. Run setup first:"
    echo "  python3 -m venv venv_telegram"
    echo "  source venv_telegram/bin/activate"
    echo "  pip install python-telegram-bot nest_asyncio requests"
    exit 1
fi

echo "[INFO] Starting LazyOwn Hermes Telegram Bot..."
exec "$VENV/bin/python" telegram_hermes.py "$@"

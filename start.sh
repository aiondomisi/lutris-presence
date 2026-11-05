#!/bin/sh
cd "$(dirname "$0")" || exit 1
pkill -f main.py 2>/dev/null
.venv/bin/python -u main.py "$GAME_NAME" >/tmp/lutris-presence.log 2>&1 &
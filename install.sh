#!/bin/sh

cd "$(dirname "$0")" || exit 1
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
chmod +x start.sh end.shpip
echo
echo "Lutris -> Preferences -> System options:"
echo "  Pre-launch script: $(pwd)/start.sh"
echo "  Post-exit script:  $(pwd)/end.sh"
echo "  Wait for pre-launch script completion: OFF"
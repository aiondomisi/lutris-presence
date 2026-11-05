# lutris-presence

Discord Rich Presence for games launched from Lutris. When a game starts, it shows up on your Discord profile as "Playing <game>", with cover art pulled from SteamGridDB.

## How it works

1. Lutris runs `start.sh` before the game launches and passes the game name in `$GAME_NAME`.
2. `main.py` looks the game up in Discord's detectable games list.
   - **Found:** the presence runs under that game's official Discord app ID.
   - **Not found:** it falls back to your own Discord application ID and fetches cover art from SteamGridDB.
3. Lutris runs `end.sh` when the game exits, which stops the script and clears the presence.

## Requirements

- Linux with Lutris
- Python 3.10+
- Discord desktop app running
- A Discord application (for the fallback ID)
- A SteamGridDB API key (optional, only needed for cover art)

## Configure

Rename `.env.example` to `.env` and fill in the information.

| Variable | Where to get it |
| --- | --- |
| `DISCORD_CLIENT_ID` | [Discord Developer Portal](https://discord.com/developers/applications) → New Application → copy the Application ID |
| `STEAM_GRID_DB_API_KEY` | [SteamGridDB](https://www.steamgriddb.com/profile/preferences/api) → API key |

## Install

Clone this repo, then run `install.sh` in the folder.

## Set up Lutris

Open Lutris → Preferences → System options, and paste the script values printed after running `install.sh`.

- **Wait for pre-launch script completion:** OFF (otherwise the game never starts)
- Turn off Lutris's built-in Discord integration so the two don't conflict.

## Troubleshooting

Watch the log live while launching a game:

```sh
tail -F /tmp/lutris-presence.log
```

## Notes

- Game name matching against Discord's list is an exact, case-insensitive match. To use the official app ID, set the game's name in Lutris to match the official title exactly, as it appears in the `name` field of [Discord's detectable games list](https://discord.com/api/v9/applications/detectable).
- Not working for games imported from your Steam library, or any other game where Lutris ends the session immediately and the game opens in its own launcher. Lutris runs `end.sh` as soon as the session stops, which kills the presence before the game has actually started.
- `.venv` contains absolute paths. If you move the project folder, delete `.venv` and re-run `install.sh`.

## Credits
 
Inspired by [steam-presence](https://github.com/JustTemmie/steam-presence).

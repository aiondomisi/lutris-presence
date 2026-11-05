from pypresence.presence import Presence
from pypresence.types import ActivityType
from time import sleep
from _pydatetime import datetime
from steamgrid import SteamGridDB
import requests
import sys
import os
from dotenv import load_dotenv

load_dotenv()

_clientID = os.environ["DISCORD_CLIENT_ID"]
_steamGRIDDBAPIKEY = os.environ["STEAM_GRID_DB_API_KEY"]


def log(log: str) -> None:
    print(f"[{datetime.now().strftime('%b %d %Y - %H:%M:%S')}] {log}")


def getGameDiscordId(gameName: str) -> dict:
    log(f"getting game discord if for {gameName}")
    gameDetails: dict = {}

    try:
        r = requests.get(
            "https://discord.com/api/v9/applications/detectable",
            headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"},
        )
        response = r.json()
        for i in response:
            if i["name"].lower() == gameName.lower():
                log(f"found the game details for {gameName}")
                gameDetails = i
                break
        else:
            log(f"game discord id not found for {gameName}")
            gameDetails = {"id": _clientID, "name": gameName}

    except Exception as e:
        log(f"error {e}")
        gameDetails = {"id": _clientID, "name": gameName}

    return gameDetails


def setPresenceDetail(gameDetails: dict) -> None:
    log(f"Setting Discord Presence")

    RPC = Presence(client_id=gameDetails["id"])
    RPC.connect()

    cover_art = gameDetails.get("coverArt")
    log(f"here is coverart id : {cover_art}")

    RPC.update(
        activity_type=ActivityType.PLAYING,
        name=gameDetails["name"],
        large_image=(cover_art if cover_art else None),
        # small_image=(cover_art if cover_art else None),
    )
    while True:
        sleep(60)


def getCoverArt(gameDetails: dict) -> str | None:
    log(f"Getting cover art")
    sgdb = SteamGridDB(_steamGRIDDBAPIKEY)
    gridIcons: str | None = None

    results = sgdb.search_game(gameDetails["name"])

    if results is None:
        log(f"No icons found for {gameDetails['name']}")
    else:
        gameId: int = results[0].id
        gridIconsList = sgdb.get_icons_by_gameid(game_ids=[gameId])

        if gridIconsList:

            gridIcons = next(
                (x.url for x in gridIconsList if x.url and not x.url.endswith(".ico")),
                None,
            )

    return gridIcons


def main() -> None:

    if _clientID is None:
        log(f"Please make a bot in discord developer portal and put it in .env file")
        return

    gameName = sys.argv[1]

    log(f"game name: {gameName}")

    # gameName = "Castlevania: Belmont's Curse"
    gameDetails = getGameDiscordId(gameName)
    if gameDetails["id"] == _clientID and _steamGRIDDBAPIKEY is not None:
        coverArt = getCoverArt(gameDetails)
        if coverArt:
            gameDetails["coverArt"] = coverArt

    log(f"current gameDetails: {gameDetails}")
    setPresenceDetail(gameDetails)


main()

import json
from pathlib import Path
import requests
from requests import RequestException

API_URL = "https://api.sleeper.app/v1/players/nfl"
OUTFILE = Path("data/sleeper_players.json")

KEEP_POS = {"QB", "RB", "WR", "TE", "DEF", "DST"}


def main() -> None:
    try:
        r = requests.get(API_URL, timeout=30)
    except RequestException:
        r = None
    if r is None or r.status_code != 200:
        if OUTFILE.exists():
            print("⚠️  Sleeper API unavailable; kept existing JSON")
            return
        OUTFILE.write_text("{}")
        print("⚠️  Sleeper API unavailable; wrote empty JSON")
        return

    all_players = r.json()
    players = {}
    for pid, info in all_players.items():
        if not info.get("active"):
            continue
        pos = info.get("position")
        if pos == "DEF":
            pos = "DST"
        if pos not in KEEP_POS:
            continue
        players[pid] = {
            "full_name": info.get("full_name"),
            "position": pos,
            "team": info.get("team"),
            "injury_status": info.get("injury_status"),
            "age": info.get("age"),
        }

    Path("data").mkdir(exist_ok=True)
    OUTFILE.write_text(json.dumps(players, indent=2))
    print(f"✅  wrote {OUTFILE}")


if __name__ == "__main__":
    main()

import json, pandas as pd, requests, io
from requests import RequestException
from pathlib import Path

TEAM_URL = ("https://raw.githubusercontent.com/nflverse/nflverse-data/master/"
            "fantasy/sos/2025_team_sos.csv")
POS_URL  = ("https://raw.githubusercontent.com/nflverse/nflverse-data/master/"
            "fantasy/sos/2025_player_sos.csv")

def fetch_csv(url: str) -> pd.DataFrame | None:
    try:
        r = requests.get(url, timeout=30)
    except RequestException:
        return None
    return pd.read_csv(io.StringIO(r.text)) if r.status_code == 200 else None

def main() -> None:
    team_df = fetch_csv(TEAM_URL)
    pos_df  = fetch_csv(POS_URL)

    Path("data").mkdir(exist_ok=True)
    team_path = Path("data/team_sched.json")
    pos_path = Path("data/pos_sched.json")

    # if nflverse hasn’t published yet, keep existing JSON or write placeholders
    if team_df is None or pos_df is None:
        if team_path.exists() and pos_path.exists():
            print("⚠️  SOS CSVs unavailable; kept existing JSON")
        else:
            team_path.write_text("{}")
            pos_path.write_text("{}")
            print("⚠️  SOS CSVs unavailable; wrote empty JSON")
        return

    team_adj = (team_df.set_index("team")["ros_fp_allowed"]
               / team_df["ros_fp_allowed"].mean()).round(3).to_dict()
    pos_adj  = (pos_df.set_index("player_name")["ros_fp_allowed"]
               / pos_df["ros_fp_allowed"].mean()).round(3).to_dict()

    Path("data").mkdir(exist_ok=True)
    Path("data/team_sched.json").write_text(json.dumps(team_adj, indent=2))
    Path("data/pos_sched.json").write_text(json.dumps(pos_adj, indent=2))
    print("✅  wrote team_sched.json & pos_sched.json")

if __name__ == "__main__":
    main()

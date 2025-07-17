import pandas as pd, requests, io, zipfile
from pathlib import Path

ZIP_URL = ("https://github.com/nflverse/nflverse-data/releases/latest/"
           "download/play_by_play_2025.zip")

def main():
    raw = requests.get(ZIP_URL, timeout=60).content
    with zipfile.ZipFile(io.BytesIO(raw)) as zf:
        with zf.open("play_by_play_2025.csv") as f:
            pbp = pd.read_csv(f, low_memory=False)

    usage = (pbp.groupby("player_name")["route"]
             .mean()
             .reset_index(name="route_run_share")
             .query("route_run_share > 0"))
    Path("data").mkdir(exist_ok=True)
    usage.to_csv("data/nflverse_usage.csv", index=False)
    print("✅  updated data/nflverse_usage.csv")

if __name__ == "__main__":
    main()

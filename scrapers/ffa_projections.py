import pandas as pd, requests, io
from pathlib import Path

URLS = [
    # primary (2025 raw projections)
    "https://raw.githubusercontent.com/FantasyFootballAnalytics/"
    "ffanalytics/master/data-raw/ffa_2025_projection_raw.csv",
    # fallback (2024 file, still better than nothing)
    "https://raw.githubusercontent.com/FantasyFootballAnalytics/"
    "ffanalytics/master/data-raw/ffa_2024_projection_raw.csv"
]

def fetch_csv():
    for url in URLS:
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            return pd.read_csv(io.StringIO(r.text))
    raise RuntimeError("FFA projection CSV unavailable")

def main():
    df = fetch_csv()
    keep = df[["player_name", "position", "team", "season_proj"]]
    Path("data").mkdir(exist_ok=True)
    keep.to_csv("data/ffa_proj.csv", index=False)
    print("✅  updated data/ffa_proj.csv")

if __name__ == "__main__":
    main()

import pandas as pd, requests, io
from pathlib import Path

URLS = [
    # 2025 projections (not yet posted—kept here for future use)
    "https://raw.githubusercontent.com/FantasyFootballAnalytics/"
    "ffanalytics/master/data-raw/ffa_2025_projection_raw.csv",
    # 2024 projections (still may 404 if repo moved)
    "https://raw.githubusercontent.com/FantasyFootballAnalytics/"
    "ffanalytics/master/data-raw/ffa_2024_projection_raw.csv",
]

OUTFILE = Path("data/ffa_proj.csv")
HEADERS = ["player_name", "position", "team", "season_proj"]

def fetch_first_available() -> pd.DataFrame | None:
    for url in URLS:
        try:
            r = requests.get(url, timeout=30)
        except requests.RequestException:
            continue
        if r.status_code == 200:
            return pd.read_csv(io.StringIO(r.text))
    return None

def main() -> None:
    Path("data").mkdir(exist_ok=True)
    df = fetch_first_available()
    if df is None:
        if OUTFILE.exists():
            print("⚠️  fetch failed; using previous data")
            return
        # Write header-only placeholder so downstream code doesn’t crash
        pd.DataFrame(columns=HEADERS).to_csv(OUTFILE, index=False)
        print("⚠️  fetch failed; wrote empty ffa_proj.csv")
    else:
        df[HEADERS].to_csv(OUTFILE, index=False)
        print("✅  updated data/ffa_proj.csv")

if __name__ == "__main__":
    main()

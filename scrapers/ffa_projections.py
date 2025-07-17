import pandas as pd
from pathlib import Path

URL = ("https://raw.githubusercontent.com/"
       "FantasyFootballAnalytics/ffanalytics/master/data-raw/ffa_2025_proj.csv")

def main():
    df = pd.read_csv(URL)
    df[["player_name", "position", "team", "season_proj"]].to_csv(
        "data/ffa_proj.csv", index=False
    )
    print("✅  updated data/ffa_proj.csv")

if __name__ == "__main__":
    main()

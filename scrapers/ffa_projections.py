import pandas as pd
from pathlib import Path

URL = "https://raw.githubusercontent.com/ryurko/nfl-analytics-with-r/master/data/projections.csv"

def main():
    df = pd.read_csv(URL)
    df = df[["player_name", "season_proj"]]
    df.to_csv("data/ffa_proj.csv", index=False)
    print("Updated data/ffa_proj.csv")

if __name__ == "__main__":
    main()

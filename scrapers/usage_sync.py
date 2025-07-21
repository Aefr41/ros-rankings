import pandas as pd, requests, io
from pathlib import Path

CSV_URL = (
    "https://raw.githubusercontent.com/nflverse/nflverse-data/master/"
    "fantasy/usage/2025_usage_weekly.csv"
)

def fetch_usage() -> pd.DataFrame | None:
    try:
        r = requests.get(CSV_URL, timeout=30)
    except requests.RequestException:
        return None
    if r.status_code != 200:
        return None
    df = pd.read_csv(io.StringIO(r.text))
    # average route-run share YTD
    usage = (df.groupby("player_name")["route_share"]
             .mean()
             .reset_index(name="route_run_share"))
    return usage

def main() -> None:
    usage = fetch_usage()
    Path("data").mkdir(exist_ok=True)
    out_file = Path("data/nflverse_usage.csv")
    if usage is None:
        if out_file.exists():
            print("⚠️  fetch failed; using previous data")
            return
        # write header-only CSV so ranking engine can still run
        pd.DataFrame(columns=["player_name", "route_run_share"]).to_csv(
            out_file, index=False)
        print("⚠️  fetch failed; wrote empty placeholder")
    else:
        usage.to_csv(out_file, index=False)
        print("✅  updated data/nflverse_usage.csv")

if __name__ == "__main__":
    main()

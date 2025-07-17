import csv
from pathlib import Path

# Placeholder usage data
players = [
    {"player_name": "Justin Jefferson", "route_run_share": 0.88},
    {"player_name": "Christian McCaffrey", "route_run_share": 0.76},
    {"player_name": "Travis Kelce", "route_run_share": 0.82}
]

def main():
    Path("data").mkdir(exist_ok=True)
    with open("data/nflverse_usage.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["player_name", "route_run_share"])
        writer.writeheader()
        writer.writerows(players)
    print("Wrote nflverse_usage.csv")

if __name__ == "__main__":
    main()

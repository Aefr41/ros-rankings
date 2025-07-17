import json
from pathlib import Path

# Dummy placeholder data — replace with real SoS later
team_sched = {
    "BUF": 0.9,
    "KC": 1.2,
    "NYJ": 0.8
}
pos_sched = {
    "Justin Jefferson": 0.95,
    "Travis Kelce": 1.1
}

def main():
    Path("data").mkdir(exist_ok=True)
    Path("data/team_sched.json").write_text(json.dumps(team_sched, indent=2))
    Path("data/pos_sched.json").write_text(json.dumps(pos_sched, indent=2))
    print("Wrote team_sched.json and pos_sched.json")

if __name__ == "__main__":
    main()

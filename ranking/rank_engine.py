"""
Minimal Rest-of-Season ranking engine (free-data edition).

Inputs  : ./data/sleeper_players.json,
          ./data/ktc_values.csv,
          ./data/nflverse_usage.csv,
          ./data/odds_totals.json
Output  : Python dict ready for JSON dump.
"""

import json, csv, datetime as dt
from pathlib import Path
import json, csv

def load_sleeper():
    path = Path("data/sleeper_players.json")
    if not path.exists():
        return {}                        # fallback: empty dict
    return json.loads(path.read_text())

def load_ktc():
    path = Path("data/ktc_values.csv")
    if not path.exists():
        return {}                        # fallback: empty dict
    with path.open() as f:
        return {row["player_name"]: float(row["value"])
                for row in csv.DictReader(f)}

def load_usage():
    path = Path("data/nflverse_usage.csv")
    if not path.exists():
        return {}
    with path.open() as f:
        return {row["player_name"]: float(row["route_run_share"])
                for row in csv.DictReader(f)}

def load_odds():
    path = Path("data/odds_totals.json")
    if not path.exists():
        return {}
    return json.loads(path.read_text())

# ---------- core rank logic ----------
def calc_rank():
    players = load_sleeper()
    ktc = load_ktc()
    usage = load_usage()

    ranked = []
    for pid, p in players.items():
        if p["position"] not in {"QB","RB","WR","TE","K","DST"}:
            continue

        base = ktc.get(p["full_name"], 0)
        snap = usage.get(p["full_name"], 0)
        injury = 999 if p["injury_status"] in {"Doubtful","Out","IR"} else 0

        score = base + 10 * snap - injury
        ranked.append((p["position"], score, pid, p["full_name"], p["injury_status"]))

    # sort high->low score inside each position
    final = {}
    for pos in {"QB","RB","WR","TE","K","DST"}:
        seq = [r for r in ranked if r[0]==pos]
        seq.sort(key=lambda x: -x[1])
        final[pos] = [
            dict(rank=i+1,
                 player_id=r[2],
                 name=r[3],
                 injury_status=r[4],
                 score=round(r[1],1))
            for i, r in enumerate(seq)
        ]
    return {"timestamp": dt.datetime.utcnow().isoformat(), "players": final}

if __name__ == "__main__":
    out = calc_rank()
    Path("public").mkdir(exist_ok=True)
    Path("public/current_ros.json").write_text(json.dumps(out, indent=2))
    print("Wrote public/current_ros.json")

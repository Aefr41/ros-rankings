import json, csv, datetime as dt
from pathlib import Path

# ---------- data loaders ----------
def load_sleeper():
    path = Path("data/sleeper_players.json")
    if not path.exists():
        return {}
    return json.loads(path.read_text())

def load_ktc():
    path = Path("data/ktc_values.csv")
    if not path.exists():
        return {}
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

def load_ffa_proj():
    path = Path("data/ffa_proj.csv")
    if not path.exists():
        return {}
    with path.open() as f:
        return {row["player_name"]: float(row["season_proj"])
                for row in csv.DictReader(f)}

def load_team_sched():
    path = Path("data/team_sched.json")
    if not path.exists():
        return {}
    return json.loads(path.read_text())

def load_pos_sched():
    path = Path("data/pos_sched.json")
    if not path.exists():
        return {}
    return json.loads(path.read_text())

def load_weights():
    path = Path("data/weights.json")
    if not path.exists():
        return {
            "season_proj": 1.0,
            "team_sched": 1.0,
            "pos_sched": 1.0,
            "usage": 1.0,
            "injury": 1.0,
            "bye": 1.0,
            "age_penalty": 1.0
        }
    return json.loads(path.read_text())

# ---------- core rank logic ----------
def calc_rank():
    players = load_sleeper()
    ktc = load_ktc()
    usage = load_usage()
    proj = load_ffa_proj()
    t_sched = load_team_sched()
    p_sched = load_pos_sched()
    weights = load_weights()

    ranked = []
    for pid, p in players.items():
        if p["position"] not in {"QB", "RB", "WR", "TE", "K", "DST"}:
            continue

        season_proj = proj.get(p["full_name"], 0)
        team_adj = t_sched.get(p["team"], 1.0)
        pos_adj = p_sched.get(p["full_name"], 1.0)
        snap = usage.get(p["full_name"], 0)
        inj = 1 if p["injury_status"] in {"Doubtful", "Out", "IR"} else 0
        bye = 1 if p.get("bye_week") == dt.datetime.now().isocalendar().week else 0
        age_penalty = 0.95 if p.get("age", 25) > 30 else 1.0

        ros_pts = (
            weights["season_proj"] * season_proj +
            weights["team_sched"] * team_adj * 10 +
            weights["pos_sched"] * pos_adj * 10 +
            weights["usage"] * snap * 10 +
            weights["injury"] * (-10 * inj) +
            weights["bye"] * (-5 * bye) +
            weights["age_penalty"] * age_penalty * 5
        )

        ranked.append((p["position"], ros_pts, pid, p["full_name"], p["injury_status"]))

    final = {}
    for pos in {"QB", "RB", "WR", "TE", "K", "DST"}:
        seq = [r for r in ranked if r[0] == pos]
        seq.sort(key=lambda x: -x[1])
        final[pos] = [
            dict(rank=i + 1,
                 player_id=r[2],
                 name=r[3],
                 injury_status=r[4],
                 ros_pts=round(r[1], 1))
            for i, r in enumerate(seq)
        ]
    return {"timestamp": dt.datetime.utcnow().isoformat(), "players": final}

if __name__ == "__main__":
    out = calc_rank()
    Path("public").mkdir(exist_ok=True)
    Path("public/current_ros.json").write_text(json.dumps(out, indent=2))
    print("Wrote public/current_ros.json")

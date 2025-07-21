import json, csv, datetime as dt
from pathlib import Path

# ---------- data loaders ----------
def load_sleeper():
    path = Path("data/sleeper_players.json")
    return json.loads(path.read_text()) if path.exists() else {}


def load_usage():
    path = Path("data/nflverse_usage.csv")
    if not path.exists(): return {}
    with path.open() as f:
        return {row["player_name"]: float(row["route_run_share"]) for row in csv.DictReader(f)}

def load_ffa_proj():
    path = Path("data/ffa_proj.csv")
    if not path.exists(): return {}
    with path.open() as f:
        return {row["player_name"]: float(row["season_proj"]) for row in csv.DictReader(f)}

def load_team_sched():
    path = Path("data/team_sched.json")
    return json.loads(path.read_text()) if path.exists() else {}

def load_pos_sched():
    path = Path("data/pos_sched.json")
    return json.loads(path.read_text()) if path.exists() else {}

def load_weights():
    path = Path("data/weights.json")
    return json.loads(path.read_text()) if path.exists() else {
        "season_proj": 1.0,
        "team_sched": 1.0,
        "pos_sched": 1.0,
        "usage": 1.0,
        "injury": 1.0,
        "bye": 1.0,
        "age_penalty": 1.0
    }

def load_prev():
    path = Path("public/prev_ros.json")
    return json.loads(path.read_text()) if path.exists() else {}


# ---------- helpers for new export format ----------
def _prev_points_lookup(prev: dict) -> dict:
    """Return mapping of player name -> previous ROS points."""
    pts = {}
    for plist in prev.get("players", {}).values():
        for p in plist:
            pts[p["name"]] = p.get("ros_pts", 0)
    return pts

def _quick_reason(p: dict, trend_val: float) -> str:
    """Return a short explanation for the player's movement."""
    if p.get("injury_status") in {"Doubtful", "Out", "IR"}:
        return "Injury concern"
    if p.get("bye_week") == dt.datetime.now().isocalendar().week:
        return "Bye week"
    if p.get("age", 25) > 30:
        return "Veteran downgrade"
    if trend_val > 1.5:
        return "Trending up"
    if trend_val < -1.5:
        return "Trending down"
    return "Steady"

# ---------- core rank logic ----------
def calc_rank():
    players = load_sleeper()
    usage = load_usage()
    proj = load_ffa_proj()
    t_sched = load_team_sched()
    p_sched = load_pos_sched()
    weights = load_weights()
    prev = load_prev()

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
    for pos in ["QB", "RB", "WR", "TE", "K", "DST"]:
        seq = [r for r in ranked if r[0] == pos]
        seq.sort(key=lambda x: -x[1])

        # build lookup for previous ranks
        prev_ranks = {
            p["name"]: p["rank"]
            for p in prev.get("players", {}).get(pos, [])
        }

        final[pos] = []
        for i, r in enumerate(seq):
            name = r[3]
            new_rank = i + 1
            old_rank = prev_ranks.get(name)
            if old_rank is not None:
                delta = old_rank - new_rank
                trend = "▲" if delta > 0 else ("▼" if delta < 0 else "")
            else:
                delta, trend = 0, ""

            final[pos].append({
                "rank": new_rank,
                "player_id": r[2],
                "name": name,
                "injury_status": r[4],
                "ros_pts": round(r[1], 1),
                "rank_change": delta,
                "trend": trend
            })

    return {"timestamp": dt.datetime.utcnow().isoformat(), "players": final}


def calc_rank_list() -> list:
    """Return simplified ranking list used for publishing."""
    players = load_sleeper()
    usage = load_usage()
    proj = load_ffa_proj()
    t_sched = load_team_sched()
    p_sched = load_pos_sched()
    weights = load_weights()
    prev = load_prev()
    prev_pts = _prev_points_lookup(prev)

    results = []
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

        prev_val = prev_pts.get(p["full_name"])  # type: ignore[index]
        trend_val = ros_pts - prev_val if prev_val is not None else 0.0
        quick = _quick_reason(p, trend_val)

        results.append({
            "player": f"{p['full_name']} ({p['team']})",
            "ros_points": round(ros_pts, 1),
            "trend": f"{trend_val:+.1f}",
            "quick_why": quick,
        })

    results.sort(key=lambda x: -x["ros_points"])
    return results

if __name__ == "__main__":
    out = calc_rank()
    Path("public").mkdir(exist_ok=True)
    Path("public/current_ros.json").write_text(json.dumps(out, indent=2))
    Path("public/prev_ros.json").write_text(json.dumps(out, indent=2))
    Path("public/ros_rankings.json").write_text(
        json.dumps(calc_rank_list(), indent=2)
    )
    print("Wrote public/current_ros.json and ros_rankings.json")

# export_json.py
"""
Runs the ranking engine and writes ./public/current_ros.json
"""

import json, pathlib
from ranking.rank_engine import calc_rank, calc_rank_list

def main():
    data = calc_rank()
    out_dir = pathlib.Path("public")
    out_dir.mkdir(exist_ok=True)
    curr = out_dir / "current_ros.json"
    curr.write_text(json.dumps(data, indent=2))
    print(f"Wrote {curr}")

    flat = calc_rank_list()
    ros = out_dir / "ros_rankings.json"
    ros.write_text(json.dumps(flat, indent=2))
    print(f"Wrote {ros}")

    # stash this run for next time
    prev = out_dir / "prev_ros.json"
    prev.write_text(curr.read_text())
    print(f"Updated {prev}")

if __name__ == "__main__":
    main()

# export_json.py
"""
Runs the ranking engine and writes ./public/current_ros.json
"""

import json, pathlib
from ranking.rank_engine import calc_rank   # make sure function name matches

def main():
    data = calc_rank()
    out_dir = pathlib.Path("public")
    out_dir.mkdir(exist_ok=True)
    outfile = out_dir / "current_ros.json"
    outfile.write_text(json.dumps(data, indent=2))
    print(f"Wrote {outfile}")

if __name__ == "__main__":
    main()

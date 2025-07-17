import json, pandas as pd
from pathlib import Path

TEAM_URL = ("https://raw.githubusercontent.com/nflverse/nflverse-data/"
            "master/fantasy/fantasy_defense_sos_team_2025.csv")
POS_URL = ("https://raw.githubusercontent.com/nflverse/nflverse-data/"
           "master/fantasy/fantasy_defense_sos_player_2025.csv")

def main():
    team_df = pd.read_csv(TEAM_URL)
    pos_df  = pd.read_csv(POS_URL)

    team_adj = (team_df.set_index("team")["ros_fp_allowed"]
               / team_df["ros_fp_allowed"].mean()).round(3).to_dict()
    pos_adj  = (pos_df.set_index("player_name")["ros_fp_allowed"]
               / pos_df["ros_fp_allowed"].mean()).round(3).to_dict()

    Path("data").mkdir(exist_ok=True)
    Path("data/team_sched.json").write_text(json.dumps(team_adj, indent=2))
    Path("data/pos_sched.json").write_text(json.dumps(pos_adj, indent=2))
    print("✅  wrote team_sched.json & pos_sched.json")

if __name__ == "__main__":
    main()

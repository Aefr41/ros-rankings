# Ranking Methodology

The ranking engine uses a points-based formula to score each player for the rest
of the season. Inputs are loaded from the CSV and JSON files created by the
scrapers under `scrapers/`. The key factors are:

1. **Season Projections** – Player projections from FantasyFootballAnalytics
   (FFA) are loaded from `data/ffa_proj.csv`.
2. **Strength of Schedule** – `schedule_weights.py` produces team‐level and
   player-level schedule adjustments (`data/team_sched.json` and
   `data/pos_sched.json`).
3. **Usage Metrics** – Average route-run share from the NFLverse usage data is
   stored in `data/nflverse_usage.csv`.
4. **Injury and Bye Week Adjustments** – Status and bye-week information from
   the Sleeper player JSON influence the final score.
5. **Age Penalty** – Players over 30 receive a small deduction.

Each factor has a weight in `data/weights.json`. The final score is the weighted
sum of the factors above. Players are ranked by position and compared to the
previous run (stored in `public/prev_ros.json`) to compute rank changes and
trends.

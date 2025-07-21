# Data Sources

Several public datasets feed into the rest-of-season rankings:

- **FantasyFootballAnalytics (FFA)** – Player projections are fetched from the
  FFA GitHub repository. The scraper `ffa_projections.py` writes them to
  `data/ffa_proj.csv`.
- **NFLverse** – Strength-of-schedule and usage metrics come from the NFLverse
  project. `schedule_weights.py` pulls positional and team adjustments while
  `usage_sync.py` downloads weekly usage statistics.
- **Sleeper** – A JSON dump of player metadata (position, team, bye week and
  injury status) is expected at `data/sleeper_players.json`.

Each scraper gracefully handles missing data by writing placeholder files so the
ranking engine can still run even if a source is temporarily unavailable.

# Data Sources

Several public datasets feed into the rest-of-season rankings:

- **FantasyFootballAnalytics (FFA)** – Player projections are fetched from the
  FFA GitHub repository. The scraper `ffa_projections.py` writes them to
  `data/ffa_proj.csv`.
- **NFLverse** – Strength-of-schedule and usage metrics come from the NFLverse
  project. `schedule_weights.py` pulls positional and team adjustments while
  `usage_sync.py` downloads weekly usage statistics.
- **Sleeper** – Player metadata is pulled from the Sleeper API via
   `scrapers/sleeper_players.py` and written to `data/sleeper_players.json`.

Each scraper gracefully handles missing data. If a request fails and prior
output exists, the scraper keeps the existing file. A placeholder is written
only when no previous data is available so the ranking engine can continue.

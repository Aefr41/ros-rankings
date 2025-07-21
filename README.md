ros-rankings/
├── .github/
│   └── workflows/
│       └── ros.yml            # GitHub-Actions workflow
├── scrapers/
│   ├── ffa_projections.py
│   ├── schedule_weights.py
│   └── usage_sync.py
├── ranking/
│   ├── changelog.py
│   └── rank_engine.py         # sample below
├── data/
├── public/
├── export_json.py
├── requirements.txt
└── README.md

## Prerequisites

- Python 3 (the workflow uses Python&nbsp;3.11)
- [pandas](https://pandas.pydata.org/)
- [requests](https://docs.python-requests.org/)

Install the dependencies with:

```bash
pip install -r requirements.txt
```

## Running the scrapers

Each scraper pulls data from public sources and saves it under `data/`:

```bash
python scrapers/ffa_projections.py   # projections from FFA
python scrapers/schedule_weights.py  # strength of schedule
python scrapers/usage_sync.py        # usage data from nflverse
```

## How rankings are produced

Run `python export_json.py` to execute `ranking/rank_engine.py`. The
engine combines the downloaded datasets, computes the rest-of-season
rankings and writes them to `public/current_ros.json`.

## Publishing the JSON

The GitHub Actions workflow defined in `.github/workflows/ros.yml`
automatically runs the scrapers and ranking engine on a schedule. The
generated `public/current_ros.json` file is then pushed to the
`gh-pages` branch so it can be served as a publicly accessible JSON
feed.

The ranking engine consumes projections and usage metrics from the scrapers
under `scrapers/`. Previous revisions referenced KeepTradeCut (KTC) values, but
that data is no longer loaded or used in the scoring formula.

## License

This project is licensed under the [MIT License](LICENSE).

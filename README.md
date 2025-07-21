ros-rankings/
├── .github/
│   └── workflows/
│       └── ros.yml            # GitHub-Actions workflow
├── scrapers/
│   ├── sleeper_poll.py
│   ├── pushshift_stream.py
│   ├── nflverse_sync.py
│   └── oddsapi_poll.py
├── ranking/
│   └── rank_engine.py         # sample below
├── export_json.py
├── requirements.txt
└── README.md

The ranking engine consumes projections and usage metrics from the scrapers
under `scrapers/`. Previous revisions referenced KeepTradeCut (KTC) values, but
that data is no longer loaded or used in the scoring formula.

import json
import logging
import datetime as dt
from pathlib import Path


def load_latest(path: str | Path, max_age_hours: int = 12) -> dict:
    """Return rankings JSON and whether it is older than max_age_hours."""
    p = Path(path)
    data = json.loads(p.read_text()) if p.exists() else []
    stale = False
    if p.exists():
        mtime = dt.datetime.fromtimestamp(p.stat().st_mtime)
        stale = (dt.datetime.now() - mtime) > dt.timedelta(hours=max_age_hours)
    else:
        logging.warning("%s does not exist", p)
    return {"data": data, "stale": stale}

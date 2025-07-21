"""Example GPT summary step.
Loads the latest ROS rankings and warns if the JSON is stale."""

import logging
from ranking.freshness import load_latest

logging.basicConfig(level=logging.INFO)

def main():
    result = load_latest("public/ros_rankings.json")
    if result["stale"]:
        logging.warning("ros_rankings.json is older than expected")
    data = result["data"]
    logging.info("Loaded %d ranking entries", len(data))
    # downstream GPT call would go here

if __name__ == "__main__":
    main()

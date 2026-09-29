"""Summarise metrics.jsonl against the wifi thresholds. Standard library only.

Usage: summarise.py <metrics.jsonl>

Each line is one JSON object; every numeric field is compared against the
thresholds table and breaches are listed. The script reads the workspace
file it is given and nothing else.
"""

import json
import sys

THRESHOLDS = {
    "retry_rate": (0.15, "above"),
    "noise_floor_dbm": (-85, "above"),
    "client_rssi_dbm": (-70, "below"),
    "channel_utilisation": (0.60, "above"),
    "disconnects_per_hour": (3, "above"),
}


def walk(obj, prefix=""):
    if isinstance(obj, dict):
        for key, value in obj.items():
            yield from walk(value, f"{prefix}{key}.")
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            yield from walk(value, f"{prefix}{index}.")
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        yield prefix.rstrip("."), obj


def main(argv):
    if len(argv) != 2:
        print("usage: summarise.py <metrics.jsonl>", file=sys.stderr)
        return 2
    breaches = []
    metrics = 0
    with open(argv[1], encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            for path, value in walk(json.loads(line)):
                metrics += 1
                leaf = path.rsplit(".", 1)[-1]
                rule = THRESHOLDS.get(leaf)
                if rule is None:
                    continue
                limit, direction = rule
                if (direction == "above" and value > limit) or (
                    direction == "below" and value < limit
                ):
                    breaches.append(f"{path}={value} ({direction} {limit})")
    print(f"metrics: {metrics}")
    print(f"breaches: {len(breaches)}")
    for breach in breaches:
        print(f"  {breach}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

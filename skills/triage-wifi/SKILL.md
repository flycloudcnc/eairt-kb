---
name: triage-wifi
description: Triage a wifi complaint - gather the wifi and client metrics that matter, collect them into the workspace, and summarise against the thresholds.
allowed-tools: Read, Bash
---

# Triage a wifi complaint

Use this skill when the request is about slow, dropping or unreliable wifi at a site.

## Steps

1. Read `references/thresholds.md` for the numbers that count as a problem.
2. Gather the telemetry: call `get_wifi_metrics` and `get_client_metrics` for the site.
3. Write the two results, one JSON object per line, to `metrics.jsonl` in your workspace.
4. Run `scripts/collect.sh metrics.jsonl` - it writes `collected.txt` with one line per metric.
5. Run `scripts/summarise.py metrics.jsonl` - it prints the summary and the thresholds breached.
6. Answer with the summary, citing the calls you made.

## Notes

- The scripts read only what is in the workspace; they take no credentials and need none.
- `collect.sh` uses `sort` and `wc`; `summarise.py` uses the standard library only.

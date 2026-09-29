#!/usr/bin/env bash
# Collect the numeric metrics out of metrics.jsonl into collected.txt, one
# "key=value" per line, sorted, and report how many there were.
#
# Usage: collect.sh <metrics.jsonl>
#
# Uses sort and wc - coreutils the worker image installs. Reads the
# workspace file it is given; writes beside it; nothing else.
set -eu

input="${1:-metrics.jsonl}"
if [ ! -f "$input" ]; then
  echo "collect.sh: no such file: $input" >&2
  exit 1
fi

# Pull "key": number pairs out of each JSON line without a JSON parser:
# enough for flat metric objects, which is what the tools return.
grep -o '"[A-Za-z_]*": *-\?[0-9][0-9.]*' "$input" \
  | sed -e 's/"//g' -e 's/: */=/' \
  | sort > collected.txt

count=$(wc -l < collected.txt | tr -d ' ')
echo "collected ${count} metrics into collected.txt"

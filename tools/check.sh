#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m unittest discover -s skills/kb-tree/tests -p 'test_*.py'
for tree in trees/computer trees/vendor-entity trees/career; do
  python3 skills/kb-tree/scripts/lint.py "$tree"
done

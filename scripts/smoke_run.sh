#!/usr/bin/env bash
set -euo pipefail

export PYTHONPATH="${PYTHONPATH:-}:src"

python3 -m unittest discover -s tests -p 'test_*.py'
python3 -m agents_framework.cli scan
python3 -m agents_framework.cli validate
python3 -m agents_framework.cli guidelines generate all
python3 -m agents_framework.cli prompt generate all
python3 -m agents_framework.cli run test --projects dor-react-app --dry-run || true


#!/usr/bin/env bash
# Minimal launcher for trainjob.py submit --cmd "bash $EXP_DIR/run_smoke.sh"
set -euo pipefail
cd "$(dirname "$0")"

# Ensure outputs land in this experiment directory
export OUT_DIR="$(pwd)"

echo "[run] starting in $PWD"
python3 app/hello.py
echo "[run] done"

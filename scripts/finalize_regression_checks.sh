#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ -n "${PYTHON_CMD:-}" ]]; then
  PYTHON_BIN="$PYTHON_CMD"
elif [[ -x "$REPO_ROOT/../.venv/bin/python" ]]; then
  PYTHON_BIN="$REPO_ROOT/../.venv/bin/python"
else
  PYTHON_BIN="$REPO_ROOT/../../.venv/bin/python"
fi

cd "$REPO_ROOT"

echo "[1/3] Running full eaggl test suite"
"$PYTHON_BIN" -m pytest -q tests

echo "[2/3] Regenerating deterministic workflow effective-config baselines"
./scripts/freeze_factor_workflow_effective_configs.sh

echo "[3/3] Verifying baseline fixtures have no drift"
git diff --exit-code -- tests/data/reference/factor_workflow_effective_config

echo "EAGGL regression checks passed with no fixture drift"

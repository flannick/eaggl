#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON_CMD="${ROOT_DIR}/../.venv/bin/python"
OUT_DIR="${ROOT_DIR}/reports/release_v1"

mkdir -p "${OUT_DIR}"

echo "[release] ROOT_DIR=${ROOT_DIR}"
echo "[release] OUT_DIR=${OUT_DIR}"

echo "[release] Running full eaggl test suite"
/usr/bin/time -l "${PYTHON_CMD}" -m pytest -q > "${OUT_DIR}/pytest.full.out" 2> "${OUT_DIR}/pytest.full.time"

echo "[release] Running finalize regression checks"
/usr/bin/time -l "${ROOT_DIR}/scripts/finalize_regression_checks.sh" > "${OUT_DIR}/finalize_checks.out" 2> "${OUT_DIR}/finalize_checks.time"

echo "[release] Completed. Logs are in ${OUT_DIR}"

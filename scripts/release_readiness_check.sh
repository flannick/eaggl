#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
OUT_DIR="${ROOT_DIR}/reports/release_v1"

PYTHON_CMD=""
for candidate in "${ROOT_DIR}/../.venv/bin/python" "${ROOT_DIR}/../../.venv/bin/python"; do
    if [ -x "${candidate}" ]; then
        PYTHON_CMD="${candidate}"
        break
    fi
done

if [ -z "${PYTHON_CMD}" ]; then
    echo "[release] ERROR: could not find venv python at ../.venv/bin/python or ../../.venv/bin/python" >&2
    exit 1
fi

mkdir -p "${OUT_DIR}"

echo "[release] ROOT_DIR=${ROOT_DIR}"
echo "[release] OUT_DIR=${OUT_DIR}"

echo "[release] Running full eaggl test suite"
/usr/bin/time -l "${PYTHON_CMD}" -m pytest -q > "${OUT_DIR}/pytest.full.out" 2> "${OUT_DIR}/pytest.full.time"

echo "[release] Running finalize regression checks"
/usr/bin/time -l "${ROOT_DIR}/scripts/finalize_regression_checks.sh" > "${OUT_DIR}/finalize_checks.out" 2> "${OUT_DIR}/finalize_checks.time"

echo "[release] Completed. Logs are in ${OUT_DIR}"

#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PIGEAN_ROOT="${1:-${REPO_ROOT}/../pigean}"

SRC_DIR="${REPO_ROOT}/src/shared"
DST_DIR="${PIGEAN_ROOT}/src/shared"

if [[ ! -d "${PIGEAN_ROOT}" ]]; then
  echo "pigean repo not found at: ${PIGEAN_ROOT}" >&2
  exit 1
fi

mkdir -p "${DST_DIR}"
cp "${SRC_DIR}/io_tables.py" "${DST_DIR}/io_tables.py"
cp "${SRC_DIR}/__init__.py" "${DST_DIR}/__init__.py"
echo "Synced shared I/O files to ${DST_DIR}"

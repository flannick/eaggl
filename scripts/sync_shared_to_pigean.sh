#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PIGEAN_ROOT="${1:-${REPO_ROOT}/../pigean}"

PHEWAS_SRC="${REPO_ROOT}/src/pegs_utils_phewas.py"
PHEWAS_DST="${PIGEAN_ROOT}/src/pegs_utils_phewas.py"
BUNDLE_SRC="${REPO_ROOT}/src/pegs_utils_bundle.py"
BUNDLE_DST="${PIGEAN_ROOT}/src/pegs_utils_bundle.py"
SYNC_GUARD_SRC="${REPO_ROOT}/src/pegs_sync_guard.py"
SYNC_GUARD_DST="${PIGEAN_ROOT}/src/pegs_sync_guard.py"

if [[ ! -d "${PIGEAN_ROOT}" ]]; then
  echo "pigean repo not found at: ${PIGEAN_ROOT}" >&2
  exit 1
fi

cp "${PHEWAS_SRC}" "${PHEWAS_DST}"
cp "${BUNDLE_SRC}" "${BUNDLE_DST}"
cp "${SYNC_GUARD_SRC}" "${SYNC_GUARD_DST}"
echo "Synced shared files to ${PIGEAN_ROOT}/src"

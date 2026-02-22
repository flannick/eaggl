#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def _resolve_pigean_script() -> Path:
    override = os.environ.get("EAGGL_PIGEAN_PATH")
    candidates = []
    if override:
        candidates.append(Path(override))

    repo_root = Path(__file__).resolve().parents[1]
    candidates.extend(
        [
            repo_root / "vendor/pigean/src/pigean.py",
            repo_root.parent / "pigean/src/pigean.py",
        ]
    )

    for path in candidates:
        resolved = path.expanduser().resolve()
        if resolved.exists():
            return resolved

    raise FileNotFoundError(
        "Unable to locate pigean.py. Set EAGGL_PIGEAN_PATH to your pigean/src/pigean.py "
        "or clone pigean as ../pigean."
    )


def main() -> int:
    pigean_script = _resolve_pigean_script()
    env = dict(os.environ)
    env["PIGEAN_APP_ROLE"] = "eaggl"
    cmd = [sys.executable, str(pigean_script), *sys.argv[1:]]
    proc = subprocess.run(cmd, env=env)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())

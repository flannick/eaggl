# eaggl

Standalone EAGGL repository split from `pigean`.

## Current state

- `src/eaggl.py` is a thin launcher that runs `pigean.py` in EAGGL mode (`PIGEAN_APP_ROLE=eaggl`).
- This keeps behavior identical during the split.
- You can point it at a specific `pigean.py` with `EAGGL_PIGEAN_PATH`.

## Run

From this repo:

```bash
../.venv/bin/python src/eaggl.py --help
```

If `pigean` is in a non-default location:

```bash
EAGGL_PIGEAN_PATH=/path/to/pigean/src/pigean.py ../.venv/bin/python src/eaggl.py factor --help
```

## Shared code strategy (recommended)

Use a small shared-code repo for table I/O (`gene_stats`, `gene_set_stats`, `phewas`) and vendor it into both repos with `git subtree`.

Why this is the best fit here:

- no runtime install requirement (both repos remain simple scripts),
- single source of truth for shared parser logic,
- explicit/pinned syncs in git history.

Details and commands are in `docs/SHARED_CODE.md`.

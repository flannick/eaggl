# EAGGL

Standalone EAGGL repository split from `pigean`.

## Current state

- `src/eaggl.py` is a standalone script (duplicated from current `pigean.py` code path).
- It only accepts EAGGL modes: `factor` and `naive_factor`.
- No runtime dependency on a sibling `pigean` checkout.

## Run

From this repo:

```bash
../../.venv/bin/python src/eaggl.py factor --help
```

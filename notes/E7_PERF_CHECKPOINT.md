# E7 Performance Checkpoint (Local)

Date: 2026-03-02
Host: local development machine (results are environment-specific)

## Command 1: full E7 regression check

Command:

```bash
/usr/bin/time -l ./scripts/finalize_regression_checks.sh
```

Result summary:

1. Wall time (`real`): `22.95s`
2. CPU time: `11.80s user`, `2.29s sys`
3. Max RSS (`maximum resident set size`): `141,787,136` bytes (~135.2 MB)

## Command 2: representative F4 workflow resolution

Command:

```bash
/usr/bin/time -l ../../.venv/bin/python src/eaggl.py factor \
  --hide-opts \
  --deterministic \
  --print-effective-config \
  --anchor-phenos T2D,T2D_ALT \
  --gene-phewas-stats-in dummy_gene_phewas.tsv \
  --gene-set-phewas-stats-in dummy_gene_set_phewas.tsv
```

Result summary:

1. Wall time (`real`): `0.85s`
2. CPU time: `0.49s user`, `0.09s sys`
3. Max RSS (`maximum resident set size`): `139,362,304` bytes (~132.9 MB)

## Notes

1. These checkpoints are intentionally informational and not CI gating.
2. Deterministic mode (`--deterministic`) was used to reduce run-to-run variance.

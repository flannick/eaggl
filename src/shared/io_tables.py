from __future__ import annotations

import csv
import gzip
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class TsvTable:
    columns: list[str]
    rows: list[dict[str, str]]
    key_column: str | None = None
    by_key: dict[str, dict[str, str]] | None = None


def _open_text(path: str | Path):
    p = str(path)
    if p.endswith(".gz"):
        return gzip.open(p, "rt")
    return open(p, "r")


def read_tsv(
    path: str | Path,
    key_column: str | None = None,
    required_columns: Iterable[str] | None = None,
) -> TsvTable:
    required = set(required_columns or [])
    with _open_text(path) as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        if reader.fieldnames is None:
            raise ValueError(f"No header found in TSV: {path}")

        missing = required.difference(reader.fieldnames)
        if missing:
            missing_fmt = ", ".join(sorted(missing))
            raise ValueError(f"Missing required columns ({missing_fmt}) in {path}")

        rows: list[dict[str, str]] = []
        by_key: dict[str, dict[str, str]] | None = {} if key_column else None
        for row in reader:
            rows.append(row)
            if key_column:
                key = row.get(key_column, "")
                if key in by_key:
                    raise ValueError(f"Duplicate key '{key}' in {path} ({key_column})")
                by_key[key] = row

    return TsvTable(columns=list(reader.fieldnames), rows=rows, key_column=key_column, by_key=by_key)


def write_tsv(path: str | Path, columns: Iterable[str], rows: Iterable[dict[str, str]]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    cols = list(columns)
    if str(path).endswith(".gz"):
        with gzip.open(path, "wt", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=cols, delimiter="\t", extrasaction="ignore")
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
    else:
        with path.open("w", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=cols, delimiter="\t", extrasaction="ignore")
            writer.writeheader()
            for row in rows:
                writer.writerow(row)


def read_gene_stats(path: str | Path) -> TsvTable:
    return read_tsv(path, key_column="Gene", required_columns=["Gene"])


def read_gene_set_stats(path: str | Path) -> TsvTable:
    return read_tsv(path, key_column="Gene_Set", required_columns=["Gene_Set"])


def read_gene_phewas_stats(path: str | Path) -> TsvTable:
    return read_tsv(path, key_column="Gene", required_columns=["Gene"])


def read_gene_set_phewas_stats(path: str | Path) -> TsvTable:
    return read_tsv(path, key_column="Gene_Set", required_columns=["Gene_Set"])


def read_factor_phewas_stats(path: str | Path) -> TsvTable:
    return read_tsv(path, required_columns=[])

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from src.shared.io_tables import read_gene_set_stats, read_gene_stats, write_tsv


class SharedIoTest(unittest.TestCase):
    def test_read_write_gene_stats_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "gene_stats.tsv"
            rows = [
                {"Gene": "INS", "prior": "2.3", "combined": "2.0"},
                {"Gene": "HNF1A", "prior": "1.8", "combined": "1.7"},
            ]
            write_tsv(path, ["Gene", "prior", "combined"], rows)
            table = read_gene_stats(path)
            self.assertEqual(len(table.rows), 2)
            self.assertEqual(table.by_key["INS"]["prior"], "2.3")

    def test_read_gene_set_stats_gz(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "gene_set_stats.tsv.gz"
            rows = [
                {"Gene_Set": "set_a", "beta_uncorrected": "0.1"},
                {"Gene_Set": "set_b", "beta_uncorrected": "0.2"},
            ]
            write_tsv(path, ["Gene_Set", "beta_uncorrected"], rows)
            table = read_gene_set_stats(path)
            self.assertEqual(table.by_key["set_b"]["beta_uncorrected"], "0.2")


if __name__ == "__main__":
    unittest.main()

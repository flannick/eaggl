from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


class EagglCliTest(unittest.TestCase):
    def _run(self, *args: str) -> subprocess.CompletedProcess[str]:
        repo_root = Path(__file__).resolve().parents[1]
        cmd = [sys.executable, "src/eaggl.py", *args]
        return subprocess.run(cmd, cwd=repo_root, capture_output=True, text=True, check=False)

    def test_help_usage_uses_eaggl_name(self) -> None:
        proc = self._run("factor", "--help")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("Usage: eaggl.py", proc.stdout)

    def test_non_factor_modes_fail_with_routing_message(self) -> None:
        proc = self._run("gibbs")
        self.assertNotEqual(proc.returncode, 0)
        err = (proc.stderr or "") + (proc.stdout or "")
        self.assertIn("belongs to pigean.py", err)

    def test_removed_gene_zs_flag_is_rejected(self) -> None:
        proc = self._run("factor", "--gene-zs-in", "dummy.tsv")
        self.assertNotEqual(proc.returncode, 0)
        err = (proc.stderr or "") + (proc.stdout or "")
        self.assertIn("option --gene-zs-in has been removed and is no longer supported", err)

    def test_factor_workflow_ids_in_effective_config(self) -> None:
        cases = [
            ("F1", []),
            ("F2", ["--positive-controls-list", "INS"]),
            ("F3", ["--gene-phewas-stats-in", "dummy_gene_phewas.tsv"]),
            (
                "F4",
                [
                    "--anchor-phenos",
                    "T2D,T2D_ALT",
                    "--gene-phewas-stats-in",
                    "dummy_gene_phewas.tsv",
                    "--gene-set-phewas-stats-in",
                    "dummy_gene_set_phewas.tsv",
                ],
            ),
            (
                "F5",
                [
                    "--anchor-any-pheno",
                    "--gene-phewas-stats-in",
                    "dummy_gene_phewas.tsv",
                    "--gene-set-phewas-stats-in",
                    "dummy_gene_set_phewas.tsv",
                ],
            ),
            (
                "F6",
                [
                    "--anchor-gene",
                    "INS",
                    "--gene-phewas-stats-in",
                    "dummy_gene_phewas.tsv",
                    "--gene-set-phewas-stats-in",
                    "dummy_gene_set_phewas.tsv",
                ],
            ),
            (
                "F7",
                [
                    "--anchor-genes",
                    "INS,GCK",
                    "--gene-phewas-stats-in",
                    "dummy_gene_phewas.tsv",
                    "--gene-set-phewas-stats-in",
                    "dummy_gene_set_phewas.tsv",
                ],
            ),
            (
                "F8",
                [
                    "--anchor-any-gene",
                    "--gene-phewas-stats-in",
                    "dummy_gene_phewas.tsv",
                    "--gene-set-phewas-stats-in",
                    "dummy_gene_set_phewas.tsv",
                ],
            ),
            (
                "F9",
                [
                    "--anchor-gene-set",
                    "--run-phewas-from-gene-phewas-stats-in",
                    "dummy_gene_phewas.tsv",
                ],
            ),
        ]

        for expected_id, args in cases:
            with self.subTest(workflow=expected_id):
                proc = self._run("factor", "--deterministic", "--print-effective-config", *args)
                self.assertEqual(proc.returncode, 0, msg=(proc.stderr or "") + (proc.stdout or ""))
                payload = json.loads(proc.stdout)
                self.assertIn("factor_workflow", payload)
                self.assertEqual(payload["factor_workflow"]["id"], expected_id)

    def test_factor_workflow_missing_inputs_fails_fast(self) -> None:
        proc = self._run("factor", "--anchor-gene", "INS")
        self.assertNotEqual(proc.returncode, 0)
        err = (proc.stderr or "") + (proc.stdout or "")
        self.assertIn("Require --gene-set-phewas-stats-in and --gene-phewas-stats-in", err)


if __name__ == "__main__":
    unittest.main()

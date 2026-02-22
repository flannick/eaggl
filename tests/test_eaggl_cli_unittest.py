from __future__ import annotations

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


if __name__ == "__main__":
    unittest.main()

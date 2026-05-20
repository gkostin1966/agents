from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agents_framework.guidelines import merge_guidelines


class GuidelinesMergeTests(unittest.TestCase):
    def _write(self, tmp: Path, name: str, content: str) -> Path:
        p = tmp / name
        p.write_text(content, encoding="utf-8")
        return p

    def test_base_sections_kept_when_no_override(self):
        import tempfile

        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            base = self._write(
                tmp,
                "base.md",
                "# Base\n\n## File Access\n\nStay in project.\n\n## Git Commits\n\nNever amend.\n",
            )
            proj = self._write(
                tmp,
                "proj.md",
                "# Project — project-specific additions\n\n> Base applies first.\n\n## Extra\n\nOnly here.\n",
            )
            merged = merge_guidelines(base, proj)
            self.assertIn("Stay in project.", merged)
            self.assertIn("Never amend.", merged)
            self.assertIn("Only here.", merged)

    def test_project_section_overrides_base(self):
        import tempfile

        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            base = self._write(
                tmp,
                "base.md",
                "# Base\n\n## Git Commits\n\nNever amend. This is the base rule.\n",
            )
            proj = self._write(
                tmp,
                "proj.md",
                "# Project\n\n## Git Commits\n\nCustom git rule for this project.\n",
            )
            merged = merge_guidelines(base, proj)
            self.assertIn("Custom git rule", merged)
            self.assertNotIn("This is the base rule", merged)

    def test_section_order_base_first_then_project_only(self):
        import tempfile

        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            base = self._write(
                tmp, "base.md", "# Base\n\n## Section A\n\nA content.\n\n## Section B\n\nB content.\n"
            )
            proj = self._write(
                tmp, "proj.md", "# Project\n\n## Section C\n\nC content.\n"
            )
            merged = merge_guidelines(base, proj)
            pos_a = merged.index("A content.")
            pos_b = merged.index("B content.")
            pos_c = merged.index("C content.")
            self.assertLess(pos_a, pos_b)
            self.assertLess(pos_b, pos_c)

    def test_real_base_and_project_files_exist_and_merge(self):
        base = ROOT / "guidelines" / "base" / "AGENTS.md"
        proj = ROOT / "guidelines" / "projects" / "deepblue-documents-kube" / "AGENTS.md"

        if not base.exists() or not proj.exists():
            self.skipTest("Real guidelines files not present")

        merged = merge_guidelines(base, proj)
        self.assertIn("## File Access", merged)
        self.assertIn("## Kubernetes Cluster Topology", merged)
        # Project overrides the Email Drafts section (Markdown vs RTF)
        self.assertIn("email", merged.lower())


if __name__ == "__main__":
    unittest.main()


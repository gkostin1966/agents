from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agents_framework.cli import build_parser
from agents_framework.prompts import merge_prompts


class PromptMergeTests(unittest.TestCase):
    def _write(self, tmp: Path, name: str, content: str) -> Path:
        p = tmp / name
        p.write_text(content, encoding="utf-8")
        return p

    def test_project_section_overrides_base(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            base = self._write(
                tmp,
                "base.md",
                "# Base\n\n## Task Files\n\nBase task location.\n",
            )
            project = self._write(
                tmp,
                "project.md",
                "# Project\n\n## Task Files\n\nProject task location.\n",
            )

            merged = merge_prompts(base, project)
            self.assertIn("Project task location.", merged)
            self.assertNotIn("Base task location.", merged)

    def test_project_only_sections_are_appended(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            base = self._write(
                tmp,
                "base.md",
                "# Base\n\n## Startup Workflow\n\nBase startup.\n",
            )
            project = self._write(
                tmp,
                "project.md",
                "# Project\n\n## Session Context\n\nProject context.\n",
            )

            merged = merge_prompts(base, project)
            self.assertIn("Base startup.", merged)
            self.assertIn("Project context.", merged)
            self.assertLess(merged.index("Base startup."), merged.index("Project context."))

    def test_cli_parser_accepts_prompt_generate(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["prompt", "generate", "dor-react-app"])
        self.assertEqual(args.which, "prompt")
        self.assertEqual(args.project, "dor-react-app")

    def test_real_base_and_project_prompts_merge(self) -> None:
        base = ROOT / "guidelines" / "base" / "AGENT_PROMPT.md"
        project = ROOT / "guidelines" / "projects" / "deepblue-documents-kube" / "AGENT_PROMPT.md"

        if not base.exists() or not project.exists():
            self.skipTest("Real prompt files not present")

        merged = merge_prompts(base, project)
        self.assertIn("## Required Developer Input", merged)
        self.assertIn("## Task Files", merged)
        self.assertIn("deepblue-documents-kube", merged)


if __name__ == "__main__":
    unittest.main()


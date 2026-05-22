from __future__ import annotations

import io
import sys
import unittest
from contextlib import redirect_stderr
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import prompt_from_git  # type: ignore


class PromptFromGitTests(unittest.TestCase):
    def test_truncate_marks_when_limited(self) -> None:
        text, truncated = prompt_from_git._truncate("x" * 100, 20)
        self.assertTrue(truncated)
        self.assertIn("[diff truncated]", text)

    def test_build_prompt_contains_branch_files_and_diff_block(self) -> None:
        prompt = prompt_from_git.build_prompt(
            branch="dor-depot",
            status_lines=["M\tsrc/app.py", "A\tREADME.md"],
            diff_text="diff --git a/src/app.py b/src/app.py\n+line",
            max_diff_chars=5000,
        )
        self.assertIn("Branch: `dor-depot`", prompt)
        self.assertIn("`M\tsrc/app.py`", prompt)
        self.assertIn("```diff", prompt)

    def test_main_errors_when_diff_limit_too_small(self) -> None:
        err = io.StringIO()
        with redirect_stderr(err):
            code = prompt_from_git.main(["--max-diff-chars", "10"])
        self.assertEqual(code, 2)
        self.assertIn("must be >= 500", err.getvalue())


if __name__ == "__main__":
    unittest.main()


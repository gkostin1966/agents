from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TokenBudgetScriptTests(unittest.TestCase):
    def _run(self, *args: str) -> subprocess.CompletedProcess[str]:
        cmd = [sys.executable, str(ROOT / "scripts" / "check_token_budgets.py"), *args]
        return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False)

    def test_budget_script_passes_with_defaults(self) -> None:
        proc = self._run()
        self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
        self.assertIn("Budget check passed.", proc.stdout)

    def test_budget_script_fails_for_tight_custom_budget(self) -> None:
        proc = self._run("--check", "AGENTS.md:1:1")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("TOO_BIG AGENTS.md", proc.stdout)


class TerseDefaultsTests(unittest.TestCase):
    def test_required_terse_defaults_present(self) -> None:
        path = ROOT / ".github" / "copilot-instructions.md"
        content = path.read_text(encoding="utf-8")

        required = (
            "Code only, no explanation.",
            "Bullets over paragraphs. No explanations unless asked.",
            "Fragments OK. Short synonyms. Code unchanged.",
        )
        for line in required:
            self.assertIn(line, content)


if __name__ == "__main__":
    unittest.main()


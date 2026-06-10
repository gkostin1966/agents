from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agents_framework.sync_base import (
    SECTION_STATUS_CUSTOMIZED,
    SECTION_STATUS_MISSING,
    SECTION_STATUS_PROJECT_ONLY,
    SECTION_STATUS_SAME,
    diff_base,
    sync_base,
)


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


BASE_TEXT = """\
# Base

## File Access

Base file-access rules.

## Git Commits

Base git rules.

## Markdown Tables

Base table rules.
"""

PROJECT_SAME = """\
# Agent Rules — demo

## File Access

Base file-access rules.

## Git Commits

Base git rules.

## Markdown Tables

Base table rules.

## Project Only

Custom project section.
"""

PROJECT_CUSTOMIZED = """\
# Agent Rules — demo

## File Access

Base file-access rules.

## Git Commits

Custom git rules for demo.

## Markdown Tables

Base table rules.

## Project Only

Custom project section.
"""

PROJECT_MISSING_SECTION = """\
# Agent Rules — demo

## File Access

Base file-access rules.

## Project Only

Custom project section.
"""


class DiffBaseTests(unittest.TestCase):
    def _setup(self, base: str, project: str) -> Path:
        tmp = Path(tempfile.mkdtemp())
        _write(tmp / "guidelines" / "base" / "AGENTS.md", base)
        _write(tmp / "guidelines" / "projects" / "demo" / "AGENTS.md", project)
        return tmp

    def test_all_same(self) -> None:
        root = self._setup(BASE_TEXT, PROJECT_SAME)
        diffs = diff_base(root, "demo")
        statuses = {d.key: d.status for d in diffs}
        self.assertEqual(statuses["File Access"], SECTION_STATUS_SAME)
        self.assertEqual(statuses["Git Commits"], SECTION_STATUS_SAME)
        self.assertEqual(statuses["Markdown Tables"], SECTION_STATUS_SAME)
        self.assertEqual(statuses["Project Only"], SECTION_STATUS_PROJECT_ONLY)

    def test_customized_section(self) -> None:
        root = self._setup(BASE_TEXT, PROJECT_CUSTOMIZED)
        diffs = diff_base(root, "demo")
        statuses = {d.key: d.status for d in diffs}
        self.assertEqual(statuses["Git Commits"], SECTION_STATUS_CUSTOMIZED)
        self.assertEqual(statuses["File Access"], SECTION_STATUS_SAME)

    def test_missing_section(self) -> None:
        root = self._setup(BASE_TEXT, PROJECT_MISSING_SECTION)
        diffs = diff_base(root, "demo")
        statuses = {d.key: d.status for d in diffs}
        self.assertEqual(statuses["Git Commits"], SECTION_STATUS_MISSING)
        self.assertEqual(statuses["Markdown Tables"], SECTION_STATUS_MISSING)


class SyncBaseTests(unittest.TestCase):
    def _setup(self, base: str, project: str) -> Path:
        tmp = Path(tempfile.mkdtemp())
        _write(tmp / "guidelines" / "base" / "AGENTS.md", base)
        _write(tmp / "guidelines" / "projects" / "demo" / "AGENTS.md", project)
        return tmp

    def test_inserts_missing_section(self) -> None:
        root = self._setup(BASE_TEXT, PROJECT_MISSING_SECTION)
        messages = sync_base(root, "demo")
        proj_text = (root / "guidelines" / "projects" / "demo" / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("## Git Commits", proj_text)
        self.assertIn("inserted", " ".join(messages))

    def test_skips_customized_section(self) -> None:
        root = self._setup(BASE_TEXT, PROJECT_CUSTOMIZED)
        messages = sync_base(root, "demo")
        proj_text = (root / "guidelines" / "projects" / "demo" / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("Custom git rules for demo", proj_text)
        self.assertIn("skipped", " ".join(messages))

    def test_force_replaces_customized(self) -> None:
        root = self._setup(BASE_TEXT, PROJECT_CUSTOMIZED)
        sync_base(root, "demo", force=True)
        proj_text = (root / "guidelines" / "projects" / "demo" / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("Base git rules", proj_text)
        self.assertNotIn("Custom git rules for demo", proj_text)

    def test_project_only_sections_preserved(self) -> None:
        root = self._setup(BASE_TEXT, PROJECT_SAME)
        sync_base(root, "demo")
        proj_text = (root / "guidelines" / "projects" / "demo" / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("## Project Only", proj_text)
        self.assertIn("Custom project section.", proj_text)

    def test_no_changes_when_already_current(self) -> None:
        root = self._setup(BASE_TEXT, PROJECT_SAME)
        messages = sync_base(root, "demo")
        self.assertIn("no changes", " ".join(messages))


if __name__ == "__main__":
    unittest.main()


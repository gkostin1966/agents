from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agents_framework.config import FrameworkConfig, ProjectConfig
from agents_framework.framework import detect_markers, resolve_project_path, scan_projects


class FrameworkTests(unittest.TestCase):
    def test_detect_markers_for_react_stack(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text("{}", encoding="utf-8")
            (root / "vite.config.js").write_text("export default {}", encoding="utf-8")

            markers = detect_markers(root, "react-vite")
            self.assertEqual(markers, ("package.json", "vite.config.js"))

    def test_scan_projects_marks_missing_mounts(self) -> None:
        cfg = FrameworkConfig(
            projects_root=Path("mounted-projects"),
            projects=(
                ProjectConfig(
                    name="demo",
                    stack="react-vite",
                    relative_path="demo",
                    commands={},
                ),
            ),
        )

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            statuses = scan_projects(root, cfg)
            self.assertEqual(len(statuses), 1)
            self.assertFalse(statuses[0].mounted)

    def test_resolve_project_path(self) -> None:
        cfg = FrameworkConfig(projects_root=Path("mounted-projects"), projects=())
        p = ProjectConfig("demo", "react-vite", "demo", {})
        with tempfile.TemporaryDirectory() as tmp:
            resolved = resolve_project_path(Path(tmp), cfg, p)
            self.assertTrue(str(resolved).endswith("mounted-projects/demo"))


if __name__ == "__main__":
    unittest.main()


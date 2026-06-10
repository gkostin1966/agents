from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_agents_link.py"


class CheckAgentsLinkScriptTests(unittest.TestCase):
    def _write_config(self, root: Path) -> None:
        config_dir = root / "config"
        config_dir.mkdir(parents=True)
        data = {
            "projects_root": "mounted-projects",
            "projects": [
                {
                    "name": "demo",
                    "stack": "react-vite",
                    "relative_path": "demo",
                    "commands": {},
                }
            ],
        }
        (config_dir / "projects.json").write_text(json.dumps(data), encoding="utf-8")

    def test_passes_when_agents_link_is_correct(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_config(root)

            source_demo = root / "sources" / "demo"
            source_demo.mkdir(parents=True)
            mount_demo = root / "mounted-projects" / "demo"
            mount_demo.parent.mkdir(parents=True)
            mount_demo.symlink_to(source_demo, target_is_directory=True)

            project_guidelines = root / "guidelines" / "projects" / "demo"
            (project_guidelines / "tasks").mkdir(parents=True)
            (project_guidelines / "AGENTS.md").write_text("", encoding="utf-8")
            (project_guidelines / "AGENT_PROMPT.md").write_text("", encoding="utf-8")
            (project_guidelines / "tasks" / "README.md").write_text("", encoding="utf-8")

            (mount_demo / ".agents").symlink_to(project_guidelines, target_is_directory=True)

            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--repo-root",
                    str(root),
                    "--project",
                    "demo",
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(proc.returncode, 0)
            self.assertIn("Integrity check passed", proc.stdout)

    def test_fails_when_agents_link_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_config(root)

            source_demo = root / "sources" / "demo"
            source_demo.mkdir(parents=True)
            mount_demo = root / "mounted-projects" / "demo"
            mount_demo.parent.mkdir(parents=True)
            mount_demo.symlink_to(source_demo, target_is_directory=True)

            project_guidelines = root / "guidelines" / "projects" / "demo"
            (project_guidelines / "tasks").mkdir(parents=True)
            (project_guidelines / "AGENTS.md").write_text("", encoding="utf-8")
            (project_guidelines / "AGENT_PROMPT.md").write_text("", encoding="utf-8")
            (project_guidelines / "tasks" / "README.md").write_text("", encoding="utf-8")

            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--repo-root",
                    str(root),
                    "--project",
                    "demo",
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(proc.returncode, 0)
            self.assertIn(".agents missing", proc.stdout)


if __name__ == "__main__":
    unittest.main()


from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agents_framework.cli import build_parser
from agents_framework.config import FrameworkConfig, ProjectConfig, load_config
from agents_framework.framework import init_mounts, run_task, scan_projects
from agents_framework.guidelines import generate_merged_file
from agents_framework.prompts import generate_merged_prompt
from agents_framework.validate import validate_projects


class InitMountsTests(unittest.TestCase):
    def _make_cfg(self, name: str) -> FrameworkConfig:
        return FrameworkConfig(
            projects_root=Path("mounted-projects"),
            projects=(ProjectConfig(name=name, stack="react-vite", relative_path=name, commands={}),),
        )

    def test_creates_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_root = root / "sources"
            source_root.mkdir()
            (source_root / "demo").mkdir()

            cfg = self._make_cfg("demo")
            results = init_mounts(root, cfg, source_root)
            self.assertEqual(len(results), 1)
            self.assertIn("linked", results[0])
            link = root / "mounted-projects" / "demo"
            self.assertTrue(link.is_symlink())

    def test_skips_when_already_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_root = root / "sources"
            source_root.mkdir()
            (source_root / "demo").mkdir()

            cfg = self._make_cfg("demo")
            init_mounts(root, cfg, source_root)
            results = init_mounts(root, cfg, source_root)
            self.assertIn("skip", results[0])

    def test_skips_when_source_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_root = root / "sources"
            source_root.mkdir()

            cfg = self._make_cfg("demo")
            results = init_mounts(root, cfg, source_root)
            self.assertIn("skip", results[0])
            self.assertIn("source missing", results[0])


class RunTaskTests(unittest.TestCase):
    def _make_status(self, tmp: Path, cmd: str):
        from agents_framework.framework import ProjectStatus
        p = ProjectConfig(name="demo", stack="react-vite", relative_path="demo", commands={"test": cmd})
        return ProjectStatus(project=p, path=tmp, mounted=True, detected_markers=())

    def test_dry_run_returns_command_string(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            status = self._make_status(Path(tmp), "echo hello")
            code, out = run_task(status, task="test", dry_run=True)
            self.assertEqual(code, 0)
            self.assertIn("echo hello", out)

    def test_missing_task_returns_code_2(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            status = self._make_status(Path(tmp), "echo hello")
            code, out = run_task(status, task="nonexistent", dry_run=True)
            self.assertEqual(code, 2)

    def test_real_execution(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            status = self._make_status(Path(tmp), "echo framework-test-ok")
            code, out = run_task(status, task="test", dry_run=False)
            self.assertEqual(code, 0)
            self.assertIn("framework-test-ok", out)


class LoadConfigTests(unittest.TestCase):
    def test_loads_valid_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config_dir = root / "config"
            config_dir.mkdir()
            data = {
                "projects_root": "mounted-projects",
                "projects": [
                    {"name": "demo", "stack": "react-vite", "relative_path": "demo", "commands": {}}
                ],
            }
            (config_dir / "projects.json").write_text(json.dumps(data), encoding="utf-8")
            cfg = load_config(root)
            self.assertEqual(len(cfg.projects), 1)
            self.assertEqual(cfg.projects[0].name, "demo")

    def test_missing_file_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileNotFoundError):
                load_config(Path(tmp))


class GenerateMergedFileWriteTests(unittest.TestCase):
    def test_writes_merged_guidelines_to_disk(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base_dir = root / "guidelines" / "base"
            base_dir.mkdir(parents=True)
            proj_dir = root / "guidelines" / "projects" / "demo"
            proj_dir.mkdir(parents=True)

            (base_dir / "AGENTS.md").write_text(
                "# Base\n\n## File Access\n\nBase rule.\n", encoding="utf-8"
            )
            (proj_dir / "AGENTS.md").write_text(
                "# Demo\n\n## Extra\n\nProject only.\n", encoding="utf-8"
            )

            result = generate_merged_file(root, "demo")
            self.assertIsNotNone(result)
            self.assertTrue(result.exists())
            content = result.read_text(encoding="utf-8")
            self.assertIn("Base rule.", content)
            self.assertIn("Project only.", content)
            self.assertIn("auto-generated", content)

    def test_writes_merged_prompt_to_disk(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base_dir = root / "guidelines" / "base"
            base_dir.mkdir(parents=True)
            proj_dir = root / "guidelines" / "projects" / "demo"
            proj_dir.mkdir(parents=True)

            (base_dir / "AGENT_PROMPT.md").write_text(
                "# Base Prompt\n\n## Startup Workflow\n\nBase workflow.\n", encoding="utf-8"
            )
            (proj_dir / "AGENT_PROMPT.md").write_text(
                "# Demo Prompt\n\n## Task Files\n\nDemo tasks.\n", encoding="utf-8"
            )

            result = generate_merged_prompt(root, "demo")
            self.assertIsNotNone(result)
            self.assertTrue(result.exists())
            content = result.read_text(encoding="utf-8")
            self.assertIn("Base workflow.", content)
            self.assertIn("Demo tasks.", content)


class ValidateTests(unittest.TestCase):
    def test_all_required_present(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            proj_dir = root / "guidelines" / "projects" / "demo"
            proj_dir.mkdir(parents=True)
            (proj_dir / "AGENTS.md").write_text("", encoding="utf-8")
            (proj_dir / "AGENT_PROMPT.md").write_text("", encoding="utf-8")

            cfg = FrameworkConfig(
                projects_root=Path("mounted-projects"),
                projects=(ProjectConfig(name="demo", stack="react-vite", relative_path="demo", commands={}),),
            )
            results = validate_projects(root, cfg)
            self.assertEqual(len(results), 1)
            self.assertTrue(results[0].ok)

    def test_missing_required_flagged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            proj_dir = root / "guidelines" / "projects" / "demo"
            proj_dir.mkdir(parents=True)
            (proj_dir / "AGENTS.md").write_text("", encoding="utf-8")
            # AGENT_PROMPT.md deliberately absent

            cfg = FrameworkConfig(
                projects_root=Path("mounted-projects"),
                projects=(ProjectConfig(name="demo", stack="react-vite", relative_path="demo", commands={}),),
            )
            results = validate_projects(root, cfg)
            self.assertFalse(results[0].ok)
            self.assertIn("AGENT_PROMPT.md", results[0].missing_required)

    def test_missing_recommended_does_not_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            proj_dir = root / "guidelines" / "projects" / "demo"
            proj_dir.mkdir(parents=True)
            (proj_dir / "AGENTS.md").write_text("", encoding="utf-8")
            (proj_dir / "AGENT_PROMPT.md").write_text("", encoding="utf-8")
            # No quiz files

            cfg = FrameworkConfig(
                projects_root=Path("mounted-projects"),
                projects=(ProjectConfig(name="demo", stack="react-vite", relative_path="demo", commands={}),),
            )
            results = validate_projects(root, cfg)
            self.assertTrue(results[0].ok)
            self.assertIn("AGENT_QUIZ.md", results[0].missing_recommended)

    def test_cli_validate_parser(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["validate"])
        self.assertEqual(args.which, "validate")
        self.assertEqual(args.projects, "all")


if __name__ == "__main__":
    unittest.main()


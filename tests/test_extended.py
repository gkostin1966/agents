from __future__ import annotations

import json
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agents_framework.cli import ALL_PROJECTS, _resolve_repo_root, _run_generate, build_parser, cmd_bootstrap
from agents_framework.config import FrameworkConfig, ProjectConfig, load_config
from agents_framework.framework import init_mounts, run_task
from agents_framework.guidelines import generate_merged_file
from agents_framework.prompts import generate_merged_prompt
from agents_framework.validate import validate_projects


class InitMountsTests(unittest.TestCase):
    def _make_cfg(self, name: str, relative_path: Optional[str] = None) -> FrameworkConfig:
        rel = relative_path if relative_path is not None else name
        return FrameworkConfig(
            projects_root=Path("mounted-projects"),
            projects=(ProjectConfig(name=name, stack="react-vite", relative_path=rel, commands={}),),
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

    def test_uses_relative_path_for_source_lookup(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_root = root / "sources"
            source_root.mkdir()
            # Source exists at relative_path, not at project name.
            (source_root / "custom-path").mkdir()

            cfg = self._make_cfg("demo-project", relative_path="custom-path")
            results = init_mounts(root, cfg, source_root)
            self.assertEqual(len(results), 1)
            self.assertIn("linked", results[0])
            self.assertTrue((root / "mounted-projects" / "custom-path").is_symlink())

    def test_creates_parent_dirs_for_nested_relative_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_root = root / "sources"
            source_root.mkdir()
            nested = source_root / "team" / "demo"
            nested.mkdir(parents=True)

            cfg = self._make_cfg("demo", relative_path="team/demo")
            results = init_mounts(root, cfg, source_root)
            self.assertEqual(len(results), 1)
            self.assertIn("linked", results[0])
            self.assertTrue((root / "mounted-projects" / "team" / "demo").is_symlink())

    def test_creates_agents_link_for_mounted_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_root = root / "sources"
            source_root.mkdir()
            (source_root / "demo").mkdir()

            guidelines_dir = root / "guidelines" / "projects" / "demo"
            guidelines_dir.mkdir(parents=True)

            cfg = self._make_cfg("demo")
            results = init_mounts(root, cfg, source_root)

            agents_link = root / "mounted-projects" / "demo" / ".agents"
            self.assertTrue(agents_link.is_symlink())
            self.assertEqual(agents_link.resolve(), guidelines_dir.resolve())
            self.assertTrue(any(".agents" in line for line in results))

    def test_keeps_existing_agents_link(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_root = root / "sources"
            source_root.mkdir()
            (source_root / "demo").mkdir()

            guidelines_dir = root / "guidelines" / "projects" / "demo"
            guidelines_dir.mkdir(parents=True)

            cfg = self._make_cfg("demo")
            init_mounts(root, cfg, source_root)
            results = init_mounts(root, cfg, source_root)

            agents_link = root / "mounted-projects" / "demo" / ".agents"
            self.assertTrue(agents_link.is_symlink())
            self.assertEqual(agents_link.resolve(), guidelines_dir.resolve())
            self.assertTrue(any("skip .agents: already exists" in line for line in results))


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
            self.assertIn("guidelines/projects/demo/AGENTS.md", content)
            self.assertNotIn(str(root), content)

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
            self.assertIn("guidelines/projects/demo/AGENT_PROMPT.md", content)
            self.assertNotIn(str(root), content)


class ValidateTests(unittest.TestCase):
    def _cfg(self) -> FrameworkConfig:
        return FrameworkConfig(
            projects_root=Path("mounted-projects"),
            projects=(
                ProjectConfig(name="demo", stack="react-vite", relative_path="demo", commands={}),
                ProjectConfig(name="demo2", stack="react-vite", relative_path="demo2", commands={}),
            ),
        )

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

    def test_empty_project_filter_validates_none(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            # Create files for one project; empty filter should still validate none.
            proj_dir = root / "guidelines" / "projects" / "demo"
            proj_dir.mkdir(parents=True)
            (proj_dir / "AGENTS.md").write_text("", encoding="utf-8")
            (proj_dir / "AGENT_PROMPT.md").write_text("", encoding="utf-8")

            results = validate_projects(root, self._cfg(), [])
            self.assertEqual(results, [])

    def test_none_project_filter_validates_all(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            # No files; both configured projects should be reported as missing required files.
            results = validate_projects(root, self._cfg(), None)
            self.assertEqual(len(results), 2)


class GenerateCliSafetyTests(unittest.TestCase):
    def _cfg(self) -> FrameworkConfig:
        return FrameworkConfig(
            projects_root=Path("mounted-projects"),
            projects=(
                ProjectConfig(name="one", stack="react-vite", relative_path="one", commands={}),
                ProjectConfig(name="two", stack="react-vite", relative_path="two", commands={}),
            ),
        )

    def test_rejects_output_with_all_projects(self) -> None:
        calls: list[tuple[str, object, bool]] = []

        def fake_generate(name: str, out: object, print_only: bool) -> object:
            calls.append((name, out, print_only))
            return None

        code = _run_generate(
            self._cfg(),
            ALL_PROJECTS,
            "/tmp/out.md",
            False,
            fake_generate,
        )
        self.assertEqual(code, 2)
        self.assertEqual(calls, [])

    def test_allows_output_with_single_project(self) -> None:
        calls: list[tuple[str, object, bool]] = []

        def fake_generate(name: str, out: object, print_only: bool) -> object:
            calls.append((name, out, print_only))
            return None

        code = _run_generate(
            self._cfg(),
            "one",
            "/tmp/out.md",
            False,
            fake_generate,
        )
        self.assertEqual(code, 0)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][0], "one")


class RepoRootResolutionTests(unittest.TestCase):
    def test_parser_accepts_repo_root_option(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--repo-root", "/tmp/demo", "scan"])
        self.assertEqual(args.repo_root, "/tmp/demo")
        self.assertEqual(args.which, "scan")

    def test_resolve_repo_root_uses_cwd_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path.cwd()
            try:
                os.chdir(tmp)
                resolved = _resolve_repo_root(None)
                self.assertEqual(resolved, Path(tmp).resolve())
            finally:
                os.chdir(cwd)

    def test_resolve_repo_root_uses_explicit_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            resolved = _resolve_repo_root(tmp)
            self.assertEqual(resolved, Path(tmp).resolve())


class BootstrapCommandTests(unittest.TestCase):
    def _cfg(self) -> FrameworkConfig:
        return FrameworkConfig(
            projects_root=Path("mounted-projects"),
            projects=(
                ProjectConfig(name="demo", stack="react-vite", relative_path="demo", commands={}),
            ),
        )

    def test_cli_bootstrap_parser(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["bootstrap", "demo"])
        self.assertEqual(args.which, "bootstrap")
        self.assertEqual(args.project, "demo")

    def test_bootstrap_generates_files_and_prints_one_shot_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base_dir = root / "guidelines" / "base"
            base_dir.mkdir(parents=True)
            proj_dir = root / "guidelines" / "projects" / "demo"
            proj_dir.mkdir(parents=True)

            (base_dir / "AGENTS.md").write_text("# Base\n\n## File Access\n\nBase.\n", encoding="utf-8")
            (base_dir / "AGENT_PROMPT.md").write_text("# Base Prompt\n\n## Startup Workflow\n\nBase prompt.\n", encoding="utf-8")
            (proj_dir / "AGENTS.md").write_text("# Demo\n\n## Extra\n\nProject.\n", encoding="utf-8")
            (proj_dir / "AGENT_PROMPT.md").write_text("# Demo Prompt\n\n## Task Files\n\nProject prompt.\n", encoding="utf-8")

            out = io.StringIO()
            with redirect_stdout(out):
                code = cmd_bootstrap(self._cfg(), root, "demo")

            self.assertEqual(code, 0)
            self.assertTrue((proj_dir / "AGENTS_MERGED.md").exists())
            self.assertTrue((proj_dir / "AGENT_PROMPT_MERGED.md").exists())

            text = out.getvalue()
            self.assertIn("Copy/paste into a new coding-agent chat", text)
            self.assertIn("AGENT_PROMPT_MERGED.md", text)
            self.assertIn("AGENTS_MERGED.md", text)

    def test_bootstrap_rejects_unknown_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = io.StringIO()
            with redirect_stdout(out):
                code = cmd_bootstrap(self._cfg(), Path(tmp), "unknown")
            self.assertEqual(code, 2)
            self.assertIn("unknown project", out.getvalue())


if __name__ == "__main__":
    unittest.main()


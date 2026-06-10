#!/usr/bin/env python3
"""Validate a mounted project's `.agents` link and key files.

Usage:
  python3 scripts/check_agents_link.py --project boxwalker | cat
  python3 scripts/check_agents_link.py --repo-root /path/to/agents --project boxwalker | cat
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Optional


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate mounted-project `.agents` link integrity")
    parser.add_argument("--repo-root", default=".", help="Path to agents repository root (default: current directory)")
    parser.add_argument("--project", required=True, help="Project name from config/projects.json")
    return parser


def _load_project_relative_path(repo_root: Path, project_name: str) -> Optional[str]:
    config_path = repo_root / "config" / "projects.json"
    if not config_path.exists():
        return None

    raw: dict[str, Any] = json.loads(config_path.read_text(encoding="utf-8"))
    for item in raw.get("projects", []):
        if item.get("name") == project_name:
            return str(item.get("relative_path", project_name))
    return None


def main() -> int:
    args = _build_parser().parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()

    relative_path = _load_project_relative_path(repo_root, args.project)
    if relative_path is None:
        print(f"ERROR: project '{args.project}' not found in config/projects.json")
        return 1

    mount_root = repo_root / "mounted-projects" / relative_path
    agents_link = mount_root / ".agents"
    expected_target = repo_root / "guidelines" / "projects" / args.project

    failures = 0

    if not mount_root.exists():
        print(f"ERROR: mounted project missing: {mount_root}")
        failures += 1
    else:
        print(f"OK: mounted project exists: {mount_root}")

    if not agents_link.exists() and not agents_link.is_symlink():
        print(f"ERROR: .agents missing: {agents_link}")
        failures += 1
    elif not agents_link.is_symlink():
        print(f"ERROR: .agents is not a symlink: {agents_link}")
        failures += 1
    else:
        actual_target = agents_link.resolve(strict=False)
        if actual_target != expected_target.resolve(strict=False):
            print(f"ERROR: .agents points to {actual_target}, expected {expected_target}")
            failures += 1
        else:
            print(f"OK: .agents target: {actual_target}")

    required_files = (
        agents_link / "AGENTS.md",
        agents_link / "AGENT_PROMPT.md",
        agents_link / "tasks" / "README.md",
    )
    for path in required_files:
        if path.exists():
            print(f"OK: found {path}")
        else:
            print(f"ERROR: missing {path}")
            failures += 1

    scripts_readme = agents_link / "scripts" / "README.md"
    if scripts_readme.exists():
        print(f"OK: found {scripts_readme}")
    else:
        print(f"WARN: optional missing {scripts_readme}")

    if failures:
        print(f"\nIntegrity check failed with {failures} error(s).")
        return 1

    print("\nIntegrity check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


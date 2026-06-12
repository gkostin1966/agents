from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ProjectConfig:
    name: str
    stack: str
    relative_path: str
    commands: dict[str, str]
    source_path: str | None = None


@dataclass(frozen=True)
class FrameworkConfig:
    projects_root: Path
    projects: tuple[ProjectConfig, ...]


def _config_path(repo_root: Path) -> Path:
    return repo_root / "config" / "projects.json"


def load_config(repo_root: Path) -> FrameworkConfig:
    config_path = _config_path(repo_root)
    raw: dict[str, Any] = json.loads(config_path.read_text(encoding="utf-8"))

    projects_raw = raw.get("projects", [])
    projects_list: list[ProjectConfig] = []
    required_keys = ("name", "stack", "relative_path", "source_path")
    for index, item in enumerate(projects_raw):
        missing = [key for key in required_keys if key not in item]
        if missing:
            raise ValueError(
                f"config/projects.json project[{index}] missing required key(s): {', '.join(missing)}"
            )

        projects_list.append(
            ProjectConfig(
                name=item["name"],
                stack=item["stack"],
                relative_path=item["relative_path"],
                commands=item.get("commands", {}),
                source_path=item["source_path"],
            )
        )

    projects = tuple(projects_list)

    return FrameworkConfig(
        projects_root=Path(raw.get("projects_root", "mounted-projects")),
        projects=projects,
    )


def add_project_to_config(
    repo_root: Path,
    *,
    name: str,
    stack: str,
    relative_path: str,
    source_path: str,
) -> tuple[bool, str]:
    config_path = _config_path(repo_root)
    raw: dict[str, Any] = json.loads(config_path.read_text(encoding="utf-8"))

    projects = raw.setdefault("projects", [])
    if any(p.get("name") == name for p in projects):
        return False, f"project '{name}' already exists in config/projects.json"

    entry: dict[str, Any] = {
        "name": name,
        "stack": stack,
        "relative_path": relative_path,
        "commands": {},
    }
    entry["source_path"] = source_path

    projects.append(entry)
    config_path.write_text(json.dumps(raw, indent=2) + "\n", encoding="utf-8")
    return True, f"added project '{name}' to config/projects.json"

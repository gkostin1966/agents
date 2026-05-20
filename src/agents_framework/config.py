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

    @property
    def marker_path(self) -> Path:
        return Path(self.relative_path)


@dataclass(frozen=True)
class FrameworkConfig:
    projects_root: Path
    projects: tuple[ProjectConfig, ...]


def load_config(repo_root: Path) -> FrameworkConfig:
    config_path = repo_root / "config" / "projects.json"
    raw: dict[str, Any] = json.loads(config_path.read_text(encoding="utf-8"))

    projects = tuple(
        ProjectConfig(
            name=item["name"],
            stack=item["stack"],
            relative_path=item["relative_path"],
            commands=item.get("commands", {}),
        )
        for item in raw.get("projects", [])
    )

    return FrameworkConfig(
        projects_root=Path(raw.get("projects_root", "mounted-projects")),
        projects=projects,
    )


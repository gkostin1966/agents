from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .config import FrameworkConfig, ProjectConfig


STACK_MARKERS: dict[str, tuple[str, ...]] = {
    "k8s-gitops": ("jsonnetfile.json", "environments"),
    "java-spring": ("build.gradle", "src"),
    "react-vite": ("package.json", "vite.config.js"),
    "dspace-docker": ("docker-compose.yml", "Makefile"),
    "rails-arclight": ("Gemfile", "docker-compose.yml"),
}


@dataclass(frozen=True)
class ProjectStatus:
    project: ProjectConfig
    path: Path
    mounted: bool
    detected_markers: tuple[str, ...]


def resolve_project_path(repo_root: Path, config: FrameworkConfig, project: ProjectConfig) -> Path:
    return repo_root / config.projects_root / project.relative_path


def detect_markers(path: Path, stack: str) -> tuple[str, ...]:
    markers = STACK_MARKERS.get(stack, ())
    found: list[str] = []
    for marker in markers:
        if (path / marker).exists():
            found.append(marker)
    return tuple(found)


def scan_projects(repo_root: Path, config: FrameworkConfig) -> list[ProjectStatus]:
    statuses: list[ProjectStatus] = []
    for project in config.projects:
        path = resolve_project_path(repo_root, config, project)
        mounted = path.exists()
        markers = detect_markers(path, project.stack) if mounted else ()
        statuses.append(
            ProjectStatus(
                project=project,
                path=path,
                mounted=mounted,
                detected_markers=markers,
            )
        )
    return statuses


def init_mounts(repo_root: Path, config: FrameworkConfig, source_root: Path) -> list[str]:
    target_root = repo_root / config.projects_root
    target_root.mkdir(parents=True, exist_ok=True)

    results: list[str] = []
    for project in config.projects:
        src = source_root / project.name
        dst = target_root / project.relative_path
        if dst.exists() or dst.is_symlink():
            results.append(f"skip {project.name}: already exists")
            continue
        if not src.exists():
            results.append(f"skip {project.name}: source missing")
            continue
        os.symlink(src, dst, target_is_directory=True)
        results.append(f"linked {project.name} -> {src}")
    return results


def run_task(status: ProjectStatus, task: str, dry_run: bool = False) -> tuple[int, str]:
    cmd = status.project.commands.get(task)
    if not cmd:
        return 2, f"no '{task}' task configured"
    if dry_run:
        return 0, f"[dry-run] {cmd}"

    proc = subprocess.run(
        cmd,
        cwd=status.path,
        shell=True,
        check=False,
        text=True,
        capture_output=True,
    )

    output = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, output.strip()


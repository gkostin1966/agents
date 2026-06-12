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
    agents_linked: bool = False
    detected_markers: tuple[str, ...] = ()


def resolve_project_path(repo_root: Path, config: FrameworkConfig, project: ProjectConfig) -> Path:
    return repo_root / config.projects_root / project.relative_path


def _project_guidelines_path(repo_root: Path, project: ProjectConfig) -> Path:
    return repo_root / "guidelines" / "projects" / project.name


def _ensure_symlink(link: Path, target: Path) -> bool:
    if link.is_symlink():
        if link.resolve(strict=False) == target.resolve(strict=False):
            return False
        link.unlink()
    elif link.exists():
        return False

    os.symlink(target, link, target_is_directory=target.is_dir())
    return True


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
        agents_linked = mounted and (path / ".agents").exists()
        markers = detect_markers(path, project.stack) if mounted else ()
        statuses.append(
            ProjectStatus(
                project=project,
                path=path,
                mounted=mounted,
                agents_linked=agents_linked,
                detected_markers=markers,
            )
        )
    return statuses


def _resolve_project_source(repo_root: Path, project: ProjectConfig) -> Path | None:
    if project.source_path:
        configured = Path(project.source_path).expanduser()
        return configured if configured.is_absolute() else (repo_root / configured)
    return None


def init_mounts(
    repo_root: Path,
    config: FrameworkConfig,
    selected_projects: set[str] | None = None,
) -> list[str]:
    target_root = repo_root / config.projects_root
    target_root.mkdir(parents=True, exist_ok=True)

    results: list[str] = []
    for project in config.projects:
        if selected_projects is not None and project.name not in selected_projects:
            continue

        src = _resolve_project_source(repo_root, project)
        dst = target_root / project.relative_path
        guidelines_dir = _project_guidelines_path(repo_root, project)
        dst.parent.mkdir(parents=True, exist_ok=True)
        messages: list[str] = []

        if src is None:
            results.append(f"skip {project.name}: source missing (set project.source_path)")
            continue

        if dst.exists() or dst.is_symlink():
            messages.append("skip mount: already exists")
        elif not src.exists():
            results.append(f"skip {project.name}: source missing")
            continue

        if not (dst.exists() or dst.is_symlink()):
            os.symlink(src, dst, target_is_directory=True)
            messages.append(f"linked mount -> {src}")

        agents_link = dst / ".agents"
        if not guidelines_dir.exists():
            messages.append("skip .agents: guidelines missing")
        elif _ensure_symlink(agents_link, guidelines_dir):
            messages.append(f"linked .agents -> {guidelines_dir}")
        elif agents_link.exists() or agents_link.is_symlink():
            messages.append("skip .agents: already exists")

        results.append(f"{project.name}: {'; '.join(messages)}")
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

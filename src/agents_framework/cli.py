from __future__ import annotations

import argparse
from pathlib import Path
from typing import Callable, Optional

from .config import FrameworkConfig, add_project_to_config, load_config
from .framework import STACK_MARKERS, init_mounts, run_task, scan_projects
from .guidelines import generate_merged_file
from .prompts import generate_merged_prompt
from .sync_base import (
    SECTION_STATUS_CUSTOMIZED,
    SECTION_STATUS_MISSING,
    SECTION_STATUS_PROJECT_ONLY,
    SECTION_STATUS_SAME,
    diff_base,
    sync_base,
)
from .validate import validate_projects


ALL_PROJECTS = "all"
SUPPORTED_STACKS = tuple(sorted(STACK_MARKERS.keys()))


def _resolve_repo_root(repo_root: Optional[str]) -> Path:
    if repo_root:
        return Path(repo_root).expanduser().resolve()
    return Path.cwd().resolve()


def _select_projects(cfg: FrameworkConfig, selected: str) -> set[str]:
    if selected == ALL_PROJECTS:
        return {p.name for p in cfg.projects}
    return {name.strip() for name in selected.split(",") if name.strip()}


def _run_generate(
    cfg: FrameworkConfig,
    project: str,
    output: Optional[str],
    print_only: bool,
    generate_fn: Callable,
) -> int:
    if project == ALL_PROJECTS and output:
        print("Error: --output cannot be used when project is 'all'.")
        return 2

    names = [p.name for p in cfg.projects] if project == ALL_PROJECTS else [project]
    output_path = Path(output) if output else None
    exit_code = 0
    for name in names:
        try:
            result = generate_fn(name, output_path, print_only)
            if result:
                print(f"Written: {result}")
        except FileNotFoundError as exc:
            print(f"Error: {exc}")
            exit_code = 1
    return exit_code


def _bootstrap_prompt_text(prompt_path: Path, guidelines_path: Path) -> str:
    prompt_ref = prompt_path.resolve()
    guidelines_ref = guidelines_path.resolve()
    return (
        "Copy/paste into a new coding-agent chat:\n\n"
        f"Read {prompt_ref} and follow it.\n"
        f"Then read {guidelines_ref} and follow those rules for all code changes.\n"
    )


def _ensure_project_guidelines(root: Path, project: str) -> list[str]:
    project_dir = root / "guidelines" / "projects" / project
    project_dir.mkdir(parents=True, exist_ok=True)

    messages: list[str] = []
    for filename, fallback in (
        (
            "AGENTS.md",
            f"# {project}\n\n## Project Notes\n\nAdd project-specific rules here.\n",
        ),
        (
            "AGENT_PROMPT.md",
            f"# {project} prompt\n\n## Startup Workflow\n\nAdd project startup instructions here.\n",
        ),
    ):
        target = project_dir / filename
        if target.exists():
            messages.append(f"keep {target}: already exists")
            continue

        base_path = root / "guidelines" / "base" / filename
        if base_path.exists():
            target.write_text(base_path.read_text(encoding="utf-8"), encoding="utf-8")
            messages.append(f"created {target} from {base_path}")
        else:
            target.write_text(fallback, encoding="utf-8")
            messages.append(f"created {target} with minimal starter content")
    return messages


def cmd_bootstrap(cfg: FrameworkConfig, root: Path, project: str) -> int:
    """Print startup text for a project session without generating merge artifacts."""
    configured = {p.name for p in cfg.projects}
    if project not in configured:
        print(f"Error: unknown project '{project}'.")
        return 2

    proj_dir = root / "guidelines" / "projects" / project
    prompt_path = proj_dir / "AGENT_PROMPT.md"
    guidelines_path = proj_dir / "AGENTS.md"

    missing = [str(p) for p in (prompt_path, guidelines_path) if not p.exists()]
    if missing:
        for m in missing:
            print(f"Error: missing file: {m}")
        return 1

    print(f"Project:    {project}")
    print(f"Guidelines: {guidelines_path}")
    print(f"Prompt:     {prompt_path}")
    print()
    print(_bootstrap_prompt_text(prompt_path, guidelines_path))
    return 0


def cmd_sync_base(
    cfg: FrameworkConfig,
    root: Path,
    project: str,
    filename: str,
    force: bool,
) -> int:
    configured = {p.name for p in cfg.projects}
    if project not in configured:
        print(f"Error: unknown project '{project}'.")
        return 2

    for fname in ([filename] if filename != "all" else ["AGENTS.md", "AGENT_PROMPT.md"]):
        try:
            messages = sync_base(root, project, fname, force=force)
        except FileNotFoundError as exc:
            print(f"Error: {exc}")
            return 1
        print(f"\n{project}/{fname}")
        for msg in messages:
            print(f"  {msg}")
    return 0


def cmd_diff_base(cfg: FrameworkConfig, root: Path, project: str, filename: str) -> int:
    configured = {p.name for p in cfg.projects}
    if project not in configured:
        print(f"Error: unknown project '{project}'.")
        return 2

    STATUS_ICON = {
        SECTION_STATUS_SAME: "=",
        SECTION_STATUS_CUSTOMIZED: "~",
        SECTION_STATUS_MISSING: "!",
        SECTION_STATUS_PROJECT_ONLY: "+",
    }

    exit_code = 0
    for fname in ([filename] if filename != "all" else ["AGENTS.md", "AGENT_PROMPT.md"]):
        try:
            diffs = diff_base(root, project, fname)
        except FileNotFoundError as exc:
            print(f"Error: {exc}")
            return 1
        print(f"\n{project}/{fname}")
        for d in diffs:
            icon = STATUS_ICON.get(d.status, "?")
            print(f"  {icon} {d.status:12} {d.key}")
            if d.status == SECTION_STATUS_MISSING:
                exit_code = 1
    return exit_code


def cmd_validate(cfg: FrameworkConfig, root: Path, projects: str) -> int:
    names = list(_select_projects(cfg, projects)) if projects != ALL_PROJECTS else None
    results = validate_projects(root, cfg, names)
    exit_code = 0
    for r in results:
        status = "OK      " if r.ok else "MISSING "
        print(f"{r.name:26} {status}", end="")
        if r.missing_required:
            print(f"  required: {', '.join(r.missing_required)}", end="")
        if r.missing_recommended:
            print(f"  recommended: {', '.join(r.missing_recommended)}", end="")
        print()
        if not r.ok:
            exit_code = 1
    return exit_code


def cmd_scan(cfg: FrameworkConfig, root: Path) -> int:
    statuses = scan_projects(root, cfg)
    for status in statuses:
        marker_note = ",".join(status.detected_markers) if status.detected_markers else "none"
        state = "mounted" if status.mounted else "missing"
        print(f"{status.project.name:26} {state:8} stack={status.project.stack:12} markers={marker_note}")
    return 0


def cmd_init_mounts(
    cfg: FrameworkConfig,
    root: Path,
    project: Optional[str],
) -> int:
    selected: set[str] | None = None
    if project:
        configured = {p.name for p in cfg.projects}
        if project not in configured:
            print(f"Error: unknown project '{project}'.")
            return 2
        selected = {project}

    results = init_mounts(root, cfg, selected_projects=selected)
    for line in results:
        print(line)
    return 0


def cmd_project_add(
    root: Path,
    name: str,
    stack: str,
    relative_path: str,
    source_path: str,
    mount: bool,
) -> int:
    if stack not in SUPPORTED_STACKS:
        print(
            f"Error: unknown stack '{stack}'. Supported stacks: {', '.join(SUPPORTED_STACKS)}"
        )
        return 2

    added, message = add_project_to_config(
        root,
        name=name,
        stack=stack,
        relative_path=relative_path,
        source_path=source_path,
    )
    if not added:
        print(f"Error: {message}")
        return 1

    print(message)
    for line in _ensure_project_guidelines(root, name):
        print(line)

    if not mount:
        return 0

    cfg = load_config(root)
    results = init_mounts(root, cfg, selected_projects={name})
    for line in results:
        print(line)
    return 0


def cmd_run(cfg: FrameworkConfig, root: Path, projects: str, task: str, dry_run: bool) -> int:
    selected = _select_projects(cfg, projects)
    statuses = [s for s in scan_projects(root, cfg) if s.project.name in selected]

    if not statuses:
        print("No matching projects selected.")
        return 1

    exit_code = 0
    for status in statuses:
        if not status.mounted:
            print(f"[{status.project.name}] skipped: not mounted at {status.path}")
            exit_code = max(exit_code, 1)
            continue

        code, out = run_task(status, task=task, dry_run=dry_run)
        prefix = f"[{status.project.name}]"
        print(f"{prefix} exit={code}")
        if out:
            print(out)
        exit_code = max(exit_code, code)

    return exit_code


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agentsfw", description="Multi-project mounted repo framework")
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Path to agents repository root (defaults to current working directory)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    scan = sub.add_parser("scan", help="Show mounted project status")
    scan.set_defaults(which="scan")

    mounts = sub.add_parser("init-mounts", help="Create symlink mounts from configured source paths")
    mounts.add_argument("--project", default=None, help="Only mount one configured project")
    mounts.set_defaults(which="init-mounts")

    project_cmd = sub.add_parser("project", help="Manage project entries in config/projects.json")
    project_sub = project_cmd.add_subparsers(dest="project_command", required=True)

    project_add = project_sub.add_parser("add", help="Add a project entry and optionally create its mount")
    project_add.add_argument("name", help="Project name key")
    project_add.add_argument(
        "--stack",
        required=True,
        choices=SUPPORTED_STACKS,
        help="Project stack identifier",
    )
    project_add.add_argument(
        "--relative-path",
        default=None,
        help="Path under mounted-projects/ (defaults to project name)",
    )
    project_add.add_argument(
        "--source-path",
        required=True,
        help="Absolute or repo-relative source project path",
    )
    project_add.add_argument(
        "--no-mount",
        action="store_true",
        help="Only update config/projects.json; do not create mounted-projects symlink",
    )
    project_add.set_defaults(which="project-add")

    run = sub.add_parser("run", help="Run a configured task on selected projects")
    run.add_argument("task", help="Task key in project commands (e.g. test, dev, lint)")
    run.add_argument("--projects", default="all", help="Comma-separated project names or 'all'")
    run.add_argument("--dry-run", action="store_true", help="Print command instead of running it")
    run.set_defaults(which="run")

    validate = sub.add_parser("validate", help="Check per-project agent-file completeness")
    validate.add_argument(
        "--projects", default=ALL_PROJECTS,
        help="Comma-separated project names or 'all' (default: all)",
    )
    validate.set_defaults(which="validate")

    bootstrap = sub.add_parser(
        "bootstrap",
        help="Print one-shot startup prompt text for a project (no merge artifacts generated)",
    )
    bootstrap.add_argument("project", help="Project name")
    bootstrap.set_defaults(which="bootstrap")

    sync = sub.add_parser(
        "sync-base",
        help="Propagate base section changes into a self-contained project file",
    )
    sync.add_argument("project", help="Project name")
    sync.add_argument(
        "--file",
        default="all",
        dest="filename",
        help="File to sync: AGENTS.md | AGENT_PROMPT.md | all (default: all)",
    )
    sync.add_argument(
        "--force",
        action="store_true",
        help="Replace customized sections too (not just unchanged ones)",
    )
    sync.set_defaults(which="sync-base")

    diff = sub.add_parser(
        "diff-base",
        help="Show drift between base sections and a self-contained project file",
    )
    diff.add_argument("project", help="Project name")
    diff.add_argument(
        "--file",
        default="all",
        dest="filename",
        help="File to diff: AGENTS.md | AGENT_PROMPT.md | all (default: all)",
    )
    diff.set_defaults(which="diff-base")

    guidelines = sub.add_parser("guidelines", help="Generate or print merged AGENTS.md for a project")
    g_sub = guidelines.add_subparsers(dest="g_command", required=True)

    g_gen = g_sub.add_parser("generate", help="Merge base + project guidelines into AGENTS_MERGED.md")
    g_gen.add_argument("project", help="Project name or 'all'")
    g_gen.add_argument("--print", dest="print_only", action="store_true",
                       help="Print merged content to stdout instead of writing a file")
    g_gen.add_argument("--output", default=None, help="Custom output file path")
    g_gen.set_defaults(which="guidelines")

    prompt = sub.add_parser("prompt", help="Generate or print merged AGENT_PROMPT.md for a project")
    p_sub = prompt.add_subparsers(dest="p_command", required=True)

    p_gen = p_sub.add_parser("generate", help="Merge base + project prompts into AGENT_PROMPT_MERGED.md")
    p_gen.add_argument("project", help="Project name or 'all'")
    p_gen.add_argument("--print", dest="print_only", action="store_true",
                       help="Print merged content to stdout instead of writing a file")
    p_gen.add_argument("--output", default=None, help="Custom output file path")
    p_gen.set_defaults(which="prompt")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    root = _resolve_repo_root(args.repo_root)
    config_path = root / "config" / "projects.json"
    if not config_path.exists():
        print(f"Error: repo root does not contain config/projects.json: {root}")
        return 2

    cfg = load_config(root)

    if args.which == "scan":
        return cmd_scan(cfg, root)
    if args.which == "validate":
        return cmd_validate(cfg, root, args.projects)
    if args.which == "init-mounts":
        return cmd_init_mounts(cfg, root, args.project)
    if args.which == "project-add":
        relative_path = args.relative_path or args.name
        return cmd_project_add(
            root,
            name=args.name,
            stack=args.stack,
            relative_path=relative_path,
            source_path=args.source_path,
            mount=not args.no_mount,
        )
    if args.which == "bootstrap":
        return cmd_bootstrap(cfg, root, args.project)
    if args.which == "sync-base":
        return cmd_sync_base(cfg, root, args.project, args.filename, args.force)
    if args.which == "diff-base":
        return cmd_diff_base(cfg, root, args.project, args.filename)
    if args.which == "run":
        return cmd_run(cfg, root, args.projects, args.task, args.dry_run)
    if args.which == "guidelines":
        return _run_generate(
            cfg, args.project, args.output, args.print_only,
            lambda name, out, p: generate_merged_file(root, name, out, print_only=p),
        )
    if args.which == "prompt":
        return _run_generate(
            cfg, args.project, args.output, args.print_only,
            lambda name, out, p: generate_merged_prompt(root, name, out, print_only=p),
        )

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

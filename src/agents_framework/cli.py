from __future__ import annotations

import argparse
from pathlib import Path
from typing import Callable, Optional

from .config import FrameworkConfig, load_config
from .framework import init_mounts, run_task, scan_projects
from .guidelines import generate_merged_file
from .prompts import generate_merged_prompt
from .validate import validate_projects


ALL_PROJECTS = "all"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


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


def cmd_init_mounts(cfg: FrameworkConfig, root: Path, source_root: str) -> int:
    results = init_mounts(root, cfg, Path(source_root))
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
    sub = parser.add_subparsers(dest="command", required=True)

    scan = sub.add_parser("scan", help="Show mounted project status")
    scan.set_defaults(which="scan")

    mounts = sub.add_parser("init-mounts", help="Create symlink mounts from a source root")
    mounts.add_argument("--source-root", required=True, help="Path containing source projects")
    mounts.set_defaults(which="init-mounts")

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

    root = _repo_root()
    cfg = load_config(root)

    if args.which == "scan":
        return cmd_scan(cfg, root)
    if args.which == "validate":
        return cmd_validate(cfg, root, args.projects)
    if args.which == "init-mounts":
        return cmd_init_mounts(cfg, root, args.source_root)
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

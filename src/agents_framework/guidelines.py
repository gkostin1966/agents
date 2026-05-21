from __future__ import annotations

"""Merge base + project-specific agent guidelines into a single AGENTS.md."""

from pathlib import Path
import re

from .merge import read_and_merge


def _stable_project_ref(project_path: Path) -> str:
    """Return a deterministic, non-absolute project reference path for headers."""
    parts = project_path.parts
    try:
        idx = parts.index("guidelines")
        if idx + 1 < len(parts) and parts[idx + 1] == "projects":
            return Path(*parts[idx:]).as_posix()
    except ValueError:
        pass
    return project_path.name


def merge_guidelines(base_path: Path, project_path: Path) -> str:
    """Return the merged AGENTS.md text for *project_path* on top of *base_path*."""
    _base_header, project_header, merged_chunks = read_and_merge(base_path, project_path)

    header = project_header if project_header.strip() else _base_header
    title_match = re.search(r"^# .+$", header, flags=re.MULTILINE)
    title = title_match.group(0) if title_match else "# Agent Rules"

    clean_title = re.sub(
        r"\s*[\u2014\-]+\s*.*\(project-specific additions\)", "", title
    ).strip()
    if not clean_title.endswith("— Merged Agent Guidelines"):
        clean_title = clean_title + " — Merged Agent Guidelines"

    project_ref = _stable_project_ref(project_path)

    provenance = (
        f"{clean_title}\n\n"
        "> **This file is auto-generated.** Do not edit it directly.\n"
        "> Edit `guidelines/base/AGENTS.md` (shared rules) or\n"
        f"> `{project_ref}` (project overrides), then regenerate.\n\n"
    )

    return provenance + "".join(merged_chunks)


def generate_merged_file(
    repo_root: Path,
    project_name: str,
    output_path: Path | None = None,
    *,
    print_only: bool = False,
) -> Path | None:
    """Generate the merged AGENTS.md for *project_name*.

    If *output_path* is given, write the file there and return it.
    If *print_only* is True, print to stdout and return None.
    """
    base_path = repo_root / "guidelines" / "base" / "AGENTS.md"
    project_path = repo_root / "guidelines" / "projects" / project_name / "AGENTS.md"

    if not base_path.exists():
        raise FileNotFoundError(f"Base guidelines not found: {base_path}")
    if not project_path.exists():
        raise FileNotFoundError(f"Project guidelines not found: {project_path}")

    merged = merge_guidelines(base_path, project_path)

    if print_only:
        print(merged)
        return None

    if output_path is None:
        output_path = repo_root / "guidelines" / "projects" / project_name / "AGENTS_MERGED.md"

    output_path.write_text(merged, encoding="utf-8")
    return output_path

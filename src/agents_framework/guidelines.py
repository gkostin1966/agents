from __future__ import annotations

"""Merge base + project-specific agent guidelines into a single AGENTS.md.

Merge semantics
---------------
Both the base file and the project file are organised as ``## Heading`` sections.
When a section heading appears in *both* files the project version **replaces** the
base version entirely.  Sections present only in the base are kept as-is; sections
present only in the project file are appended after the merged base body.

The file header (everything before the first ``## ``) is taken from the project file
when it exists, otherwise from the base.
"""

from pathlib import Path
import re


def _split_sections(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Return (header, [(heading, body), ...]) from a markdown document."""
    parts = re.split(r"(?=^## )", text, flags=re.MULTILINE)
    header = parts[0]
    sections: list[tuple[str, str]] = []
    for chunk in parts[1:]:
        # heading is the first line; body is everything after
        newline = chunk.find("\n")
        if newline == -1:
            heading, body = chunk.strip(), ""
        else:
            heading = chunk[:newline].strip()
            body = chunk[newline:]
        # Strip the "## " prefix so we can compare headings case-insensitively
        key = heading.lstrip("# ").strip()
        sections.append((key, chunk))
    return header, sections


def merge_guidelines(base_path: Path, project_path: Path) -> str:
    """Return the merged AGENTS.md text for *project_path* on top of *base_path*."""
    base_text = base_path.read_text(encoding="utf-8")
    project_text = project_path.read_text(encoding="utf-8")

    base_header, base_sections = _split_sections(base_text)
    proj_header, proj_sections = _split_sections(project_text)

    # Build lookup: normalised heading → full section chunk (project wins)
    proj_index: dict[str, str] = {key.lower(): chunk for key, chunk in proj_sections}

    merged_chunks: list[str] = []

    # Walk base sections in order; replace any overridden by project
    seen_keys: set[str] = set()
    for key, base_chunk in base_sections:
        norm = key.lower()
        seen_keys.add(norm)
        if norm in proj_index:
            merged_chunks.append(proj_index[norm])
        else:
            merged_chunks.append(base_chunk)

    # Append project-only sections (not in base) in their original order
    for key, proj_chunk in proj_sections:
        if key.lower() not in seen_keys:
            merged_chunks.append(proj_chunk)

    # Choose header: project header if it has a meaningful title line
    header = proj_header if proj_header.strip() else base_header

    # Strip the metadata block from the project header (lines starting with "> ")
    # but keep it if the caller wants the raw project header for provenance.
    # For the merged output we produce a clean header drawn from the project's
    # intent (first "# " line) plus a short provenance note.
    title_match = re.search(r"^# .+$", header, flags=re.MULTILINE)
    if title_match:
        title = title_match.group(0)
    else:
        title = "# Agent Rules"

    # Strip "project-specific additions" from the title for the merged file
    clean_title = re.sub(r"\s*[\u2014\-]+\s*.*\(project-specific additions\)", "", title).strip()
    if not clean_title.endswith("— Merged Agent Guidelines"):
        clean_title = clean_title + " — Merged Agent Guidelines"

    provenance = (
        f"{clean_title}\n\n"
        "> **This file is auto-generated.** Do not edit it directly.\n"
        "> Edit `guidelines/base/AGENTS.md` (shared rules) or\n"
        f"> `{project_path}` (project overrides), then regenerate.\n\n"
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


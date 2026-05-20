from __future__ import annotations

"""Merge base + project startup prompts into a single AGENT_PROMPT.md.

Merge semantics
---------------
Both files are organised as ``## Heading`` sections.
When a heading appears in both files, the project section replaces the base section.
Base-only sections are retained, and project-only sections are appended in order.
"""

from pathlib import Path
import re
from typing import Optional


def _split_sections(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Return (header, [(heading, body), ...]) from a markdown document."""
    parts = re.split(r"(?=^## )", text, flags=re.MULTILINE)
    header = parts[0]
    sections: list[tuple[str, str]] = []
    for chunk in parts[1:]:
        newline = chunk.find("\n")
        if newline == -1:
            heading = chunk.strip()
        else:
            heading = chunk[:newline].strip()
        key = heading.lstrip("# ").strip()
        sections.append((key, chunk))
    return header, sections


def merge_prompts(base_path: Path, project_path: Path) -> str:
    """Return merged startup prompt text for *project_path* on top of *base_path*."""
    base_text = base_path.read_text(encoding="utf-8")
    project_text = project_path.read_text(encoding="utf-8")

    base_header, base_sections = _split_sections(base_text)
    project_header, project_sections = _split_sections(project_text)

    project_index: dict[str, str] = {key.lower(): chunk for key, chunk in project_sections}

    merged_chunks: list[str] = []
    seen: set[str] = set()

    for key, base_chunk in base_sections:
        norm = key.lower()
        seen.add(norm)
        merged_chunks.append(project_index.get(norm, base_chunk))

    for key, project_chunk in project_sections:
        if key.lower() not in seen:
            merged_chunks.append(project_chunk)

    header = project_header if project_header.strip() else base_header
    title_match = re.search(r"^# .+$", header, flags=re.MULTILINE)
    title = title_match.group(0) if title_match else "# New Session Startup Prompt"

    provenance = (
        f"{title}\n\n"
        "> **This file is auto-generated.** Do not edit it directly.\n"
        "> Edit `guidelines/base/AGENT_PROMPT.md` (shared startup blocks) or\n"
        f"> `{project_path}` (project prompt overrides), then regenerate.\n\n"
    )

    return provenance + "".join(merged_chunks)


def generate_merged_prompt(
    repo_root: Path,
    project_name: str,
    output_path: Optional[Path] = None,
    *,
    print_only: bool = False,
) -> Optional[Path]:
    """Generate merged AGENT_PROMPT.md for *project_name*."""
    base_path = repo_root / "guidelines" / "base" / "AGENT_PROMPT.md"
    project_path = repo_root / "guidelines" / "projects" / project_name / "AGENT_PROMPT.md"

    if not base_path.exists():
        raise FileNotFoundError(f"Base prompt not found: {base_path}")
    if not project_path.exists():
        raise FileNotFoundError(f"Project prompt not found: {project_path}")

    merged = merge_prompts(base_path, project_path)

    if print_only:
        print(merged)
        return None

    if output_path is None:
        output_path = repo_root / "guidelines" / "projects" / project_name / "AGENT_PROMPT_MERGED.md"

    output_path.write_text(merged, encoding="utf-8")
    return output_path


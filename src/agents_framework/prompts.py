from __future__ import annotations

"""Merge base + project startup prompts into a single AGENT_PROMPT.md."""

from pathlib import Path
from typing import Optional

from .merge import read_and_merge


def merge_prompts(base_path: Path, project_path: Path) -> str:
    """Return merged startup prompt text for *project_path* on top of *base_path*."""
    _base_header, project_header, merged_chunks = read_and_merge(base_path, project_path)

    header = project_header if project_header.strip() else _base_header
    import re

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
        output_path = (
            repo_root / "guidelines" / "projects" / project_name / "AGENT_PROMPT_MERGED.md"
        )

    output_path.write_text(merged, encoding="utf-8")
    return output_path

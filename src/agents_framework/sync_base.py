from __future__ import annotations

"""Two-hat sync utilities for self-contained project agent files.

Provides ``sync_base`` and ``diff_base`` to let the framework hat propagate
base-rule changes into self-contained per-project files without a merge artifact.
"""

from dataclasses import dataclass
from pathlib import Path

from .merge import split_sections


SECTION_STATUS_SAME = "SAME"
SECTION_STATUS_CUSTOMIZED = "CUSTOMIZED"
SECTION_STATUS_MISSING = "MISSING"
SECTION_STATUS_PROJECT_ONLY = "PROJECT_ONLY"


@dataclass
class SectionDiff:
    key: str
    status: str  # one of the SECTION_STATUS_* constants


def _read_sections(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    _, sections = split_sections(text)
    return {key.lower(): (key, chunk) for key, chunk in sections}


def diff_base(
    repo_root: Path,
    project_name: str,
    filename: str = "AGENTS.md",
) -> list[SectionDiff]:
    """Compare base sections against a project file.

    Returns a list of SectionDiff describing the status of each section.
    """
    base_path = repo_root / "guidelines" / "base" / filename
    proj_path = repo_root / "guidelines" / "projects" / project_name / filename

    if not base_path.exists():
        raise FileNotFoundError(f"Base file not found: {base_path}")
    if not proj_path.exists():
        raise FileNotFoundError(f"Project file not found: {proj_path}")

    base_sections = _read_sections(base_path)
    proj_sections = _read_sections(proj_path)

    diffs: list[SectionDiff] = []

    for norm_key, (display_key, base_chunk) in base_sections.items():
        if norm_key not in proj_sections:
            diffs.append(SectionDiff(key=display_key, status=SECTION_STATUS_MISSING))
        else:
            _, proj_chunk = proj_sections[norm_key]
            if proj_chunk.strip() == base_chunk.strip():
                diffs.append(SectionDiff(key=display_key, status=SECTION_STATUS_SAME))
            else:
                diffs.append(SectionDiff(key=display_key, status=SECTION_STATUS_CUSTOMIZED))

    for norm_key, (display_key, _) in proj_sections.items():
        if norm_key not in base_sections:
            diffs.append(SectionDiff(key=display_key, status=SECTION_STATUS_PROJECT_ONLY))

    return diffs


def sync_base(
    repo_root: Path,
    project_name: str,
    filename: str = "AGENTS.md",
    *,
    force: bool = False,
) -> list[str]:
    """Propagate base section changes into a project file.

    For each section in the base file:
    - If the project section is SAME as base → update (no actual change needed, but
      ensures latest wording).
    - If the project section is CUSTOMIZED → skip (preserve project customization)
      unless *force* is True.
    - If the project section is MISSING → insert from base.

    Returns a list of status messages.
    """
    base_path = repo_root / "guidelines" / "base" / filename
    proj_path = repo_root / "guidelines" / "projects" / project_name / filename

    if not base_path.exists():
        raise FileNotFoundError(f"Base file not found: {base_path}")
    if not proj_path.exists():
        raise FileNotFoundError(f"Project file not found: {proj_path}")

    base_text = base_path.read_text(encoding="utf-8")
    proj_text = proj_path.read_text(encoding="utf-8")

    proj_header, proj_section_list = split_sections(proj_text)
    _, base_section_list = split_sections(base_text)

    base_index: dict[str, str] = {key.lower(): chunk for key, chunk in base_section_list}
    proj_index: dict[str, str] = {key.lower(): chunk for key, chunk in proj_section_list}

    messages: list[str] = []
    updated_proj_sections: list[str] = []

    # Walk base sections to determine insert order and update matching project sections.
    base_norms = [key.lower() for key, _ in base_section_list]

    for norm in base_norms:
        base_chunk = base_index[norm]
        if norm in proj_index:
            proj_chunk = proj_index[norm]
            if proj_chunk.strip() == base_chunk.strip():
                # Keep project's exact whitespace; no update needed.
                updated_proj_sections.append(proj_chunk)
                messages.append(f"up-to-date  {norm}")
            elif force:
                updated_proj_sections.append(base_chunk)
                messages.append(f"forced      {norm}")
            else:
                updated_proj_sections.append(proj_chunk)
                messages.append(f"skipped     {norm}  (customized)")
        else:
            updated_proj_sections.append(base_chunk)
            messages.append(f"inserted    {norm}  (was missing)")

    # Append project-only sections (not in base) at the end, preserving order.
    for key, chunk in proj_section_list:
        if key.lower() not in base_norms:
            updated_proj_sections.append(chunk)

    new_text = proj_header + "".join(updated_proj_sections)

    if new_text != proj_text:
        proj_path.write_text(new_text, encoding="utf-8")
        messages.append("written")
    else:
        messages.append("no changes")

    return messages


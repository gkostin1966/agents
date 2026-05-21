from __future__ import annotations

"""Shared section-merge engine for Markdown agent files.

Both ``guidelines.py`` (AGENTS.md) and ``prompts.py`` (AGENT_PROMPT.md) use
the same heading-based merge model.  This module provides the shared primitives
so the logic lives in exactly one place.

Merge semantics
---------------
Both the *base* file and the *project* file are organised as ``## Heading``
sections.  When a heading appears in **both** files the project section replaces
the base section entirely.  Sections present only in the base are kept; sections
present only in the project are appended in their original order after the
merged base sections.
"""

import re
from pathlib import Path


def split_sections(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Return ``(header, [(key, chunk), ...])`` from a Markdown document.

    *header* is everything before the first ``## `` section.
    Each tuple contains a normalised heading key (stripped of ``#`` and
    leading/trailing whitespace) and the raw chunk (heading line + body).
    """
    parts = re.split(r"(?=^## )", text, flags=re.MULTILINE)
    header = parts[0]
    sections: list[tuple[str, str]] = []
    for chunk in parts[1:]:
        newline = chunk.find("\n")
        heading = chunk.strip() if newline == -1 else chunk[:newline].strip()
        key = heading.lstrip("# ").strip()
        sections.append((key, chunk))
    return header, sections


def merge_sections(
    base_text: str,
    project_text: str,
) -> tuple[str, str, list[str]]:
    """Merge *base_text* and *project_text* section-by-section.

    Returns ``(base_header, project_header, merged_chunks)`` where
    *merged_chunks* is the ordered list of raw section chunks ready to be
    joined.  Callers are responsible for prepending a provenance header.
    """
    base_header, base_sections = split_sections(base_text)
    project_header, project_sections = split_sections(project_text)

    project_index: dict[str, str] = {
        key.lower(): chunk for key, chunk in project_sections
    }

    merged_chunks: list[str] = []
    seen: set[str] = set()

    for key, base_chunk in base_sections:
        norm = key.lower()
        seen.add(norm)
        merged_chunks.append(project_index.get(norm, base_chunk))

    for key, project_chunk in project_sections:
        if key.lower() not in seen:
            merged_chunks.append(project_chunk)

    return base_header, project_header, merged_chunks


def read_and_merge(base_path: Path, project_path: Path) -> tuple[str, str, list[str]]:
    """Read both files from disk and return the result of :func:`merge_sections`."""
    return merge_sections(
        base_path.read_text(encoding="utf-8"),
        project_path.read_text(encoding="utf-8"),
    )


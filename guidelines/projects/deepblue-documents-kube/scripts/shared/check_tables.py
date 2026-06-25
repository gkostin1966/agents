#!/usr/bin/env python3
"""Validate Markdown table formatting.

Usage:
  python3 .agents/scripts/shared/check_tables.py README.md [OTHER.md ...] | cat

Validation strategy:
- Parse each pipe-table block (header + separator + optional data rows).
- Reformat the block with the same algorithm as format_table.py.
- Report line ranges where actual content differs from normalized output.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from typing import List, Tuple

SEPARATOR_RE = re.compile(r"^\s*\|(?:\s*:?-{3,}:?\s*\|)+\s*$")


def is_table_row(line: str) -> bool:
    s = line.strip()
    return s.startswith("|") and s.endswith("|") and s.count("|") >= 2


def split_cells(line: str) -> List[str]:
    core = line.strip()[1:-1]
    return [p.strip() for p in core.split("|")]


def format_row(cells: List[str], widths: List[int]) -> str:
    return "| " + " | ".join(c.ljust(w) for c, w in zip(cells, widths)) + " |"


def format_sep(widths: List[int]) -> str:
    return "| " + " | ".join("-" * w for w in widths) + " |"


def format_table_block(block: List[str]) -> List[str]:
    rows = [split_cells(x) for x in block]
    col_count = len(rows[0])
    for idx, row in enumerate(rows, start=1):
        if len(row) != col_count:
            raise ValueError(f"inconsistent column count at table row {idx}")

    header = rows[0]
    data_rows = rows[2:] if len(rows) > 2 else []
    width_basis = data_rows if data_rows else [header]

    widths = [0] * col_count
    for row in width_basis:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))
    widths = [max(3, w) for w in widths]

    out = [format_row(header, widths), format_sep(widths)]
    out.extend(format_row(r, widths) for r in data_rows)
    return out


def find_table_issues(text: str) -> List[Tuple[int, int, str]]:
    lines = text.splitlines()
    issues: List[Tuple[int, int, str]] = []
    i = 0
    while i < len(lines):
        if i + 1 < len(lines) and is_table_row(lines[i]) and SEPARATOR_RE.match(lines[i + 1]):
            start = i
            i += 2
            while i < len(lines) and is_table_row(lines[i]):
                i += 1
            end = i
            block = lines[start:end]
            try:
                expected = format_table_block(block)
            except ValueError as exc:
                issues.append((start + 1, end, str(exc)))
                continue
            if expected != block:
                issues.append((start + 1, end, "table formatting mismatch"))
        else:
            i += 1
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Markdown table formatting.")
    parser.add_argument("files", nargs="+", help="Markdown files to validate")
    args = parser.parse_args()

    had_errors = False
    for file_name in args.files:
        path = pathlib.Path(file_name)
        if not path.exists():
            print(f"ERROR: file not found: {path}")
            had_errors = True
            continue
        text = path.read_text(encoding="utf-8")
        issues = find_table_issues(text)
        if not issues:
            print(f"OK: {path}")
            continue
        had_errors = True
        print(f"ERROR: {path}")
        for start, end, msg in issues:
            print(f"  lines {start}-{end}: {msg}")

    return 1 if had_errors else 0


if __name__ == "__main__":
    sys.exit(main())


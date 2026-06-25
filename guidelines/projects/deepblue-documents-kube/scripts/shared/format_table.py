#!/usr/bin/env python3
"""Rewrite Markdown tables with normalized padding.

Usage:
  python3 .agents/scripts/shared/format_table.py README.md [OTHER.md ...] | cat

Rules implemented:
- Detect pipe tables with a separator row.
- Keep column count consistent across rows in a table block.
- Column widths are driven by data rows when present; otherwise header row.
- Header/data rows are padded to widths; separator row uses dashes with width.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from typing import List

SEPARATOR_RE = re.compile(r"^\s*\|(?:\s*:?-{3,}:?\s*\|)+\s*$")


def is_table_row(line: str) -> bool:
    s = line.strip()
    return s.startswith("|") and s.endswith("|") and s.count("|") >= 2


def split_cells(line: str) -> List[str]:
    core = line.strip()[1:-1]
    parts = core.split("|")
    return [p.strip() for p in parts]


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

    # Ensure minimum visible width.
    widths = [max(3, w) for w in widths]

    out = [format_row(header, widths), format_sep(widths)]
    for row in data_rows:
        out.append(format_row(row, widths))
    return out


def format_markdown(text: str) -> str:
    lines = text.splitlines()
    out: List[str] = []
    i = 0
    while i < len(lines):
        if i + 1 < len(lines) and is_table_row(lines[i]) and SEPARATOR_RE.match(lines[i + 1]):
            start = i
            i += 2
            while i < len(lines) and is_table_row(lines[i]):
                i += 1
            block = lines[start:i]
            out.extend(format_table_block(block))
        else:
            out.append(lines[i])
            i += 1
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def main() -> int:
    parser = argparse.ArgumentParser(description="Format Markdown tables in-place.")
    parser.add_argument("files", nargs="+", help="Markdown files to format")
    args = parser.parse_args()

    exit_code = 0
    for file_name in args.files:
        path = pathlib.Path(file_name)
        if not path.exists():
            print(f"ERROR: file not found: {path}")
            exit_code = 1
            continue
        original = path.read_text(encoding="utf-8")
        try:
            formatted = format_markdown(original)
        except ValueError as exc:
            print(f"ERROR: {path}: {exc}")
            exit_code = 1
            continue
        if formatted != original:
            path.write_text(formatted, encoding="utf-8")
            print(f"UPDATED: {path}")
        else:
            print(f"OK: {path}")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())


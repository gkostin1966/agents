#!/usr/bin/env python3
"""Second-pass DSpace 7 harvest crosswalk fixer.

Usage:
  python3 .agents/scripts/shared/fix_harvest_crosswalk_dspace7.py \
    --input harvest-patched.xml --output harvest-final.xml | cat

Built-in conservative fixes:
- Replace XPath handle expression `//handle[1]` with JSONPath `$.handle`.

This script is intentionally minimal and safe for framework bootstrapping.
Add new deterministic replacements as needed.
"""

from __future__ import annotations

import argparse
import pathlib
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply second-pass harvest crosswalk fixes.")
    parser.add_argument("--input", required=True, help="Input XML file")
    parser.add_argument("--output", required=True, help="Output XML file")
    args = parser.parse_args()

    src = pathlib.Path(args.input)
    dst = pathlib.Path(args.output)
    if not src.exists():
        print(f"ERROR: input file not found: {src}")
        return 1

    text = src.read_text(encoding="utf-8")

    replacements = [
        ("//handle[1]", "$.handle"),
    ]

    total = 0
    for old, new in replacements:
        count = text.count(old)
        if count:
            text = text.replace(old, new)
            total += count
            print(f"PATCH: {old} -> {new} ({count})")

    dst.write_text(text, encoding="utf-8")
    print(f"WROTE: {dst}")
    print(f"CHANGES: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())


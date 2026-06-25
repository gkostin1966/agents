#!/usr/bin/env python3
"""First-pass harvest crosswalk patcher.

Usage:
  python3 .agents/scripts/shared/patch_harvest_crosswalk.py \
    --input harvest.xml --output harvest-patched.xml | cat

Transform:
- Replace select-using="xpath" with select-using="jsonpath".
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

PATTERN = re.compile(r'(select-using\s*=\s*["\'])xpath(["\'])')


def main() -> int:
    parser = argparse.ArgumentParser(description="Patch harvest crosswalk to jsonpath selectors.")
    parser.add_argument("--input", required=True, help="Input XML file")
    parser.add_argument("--output", required=True, help="Output XML file")
    args = parser.parse_args()

    src = pathlib.Path(args.input)
    dst = pathlib.Path(args.output)

    if not src.exists():
        print(f"ERROR: input file not found: {src}")
        return 1

    text = src.read_text(encoding="utf-8")
    patched, count = PATTERN.subn(r"\1jsonpath\2", text)
    dst.write_text(patched, encoding="utf-8")

    print(f"WROTE: {dst}")
    print(f"CHANGES: {count} selector(s) xpath -> jsonpath")
    return 0


if __name__ == "__main__":
    sys.exit(main())


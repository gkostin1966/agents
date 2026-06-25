#!/usr/bin/env python3
"""Patch deposit crosswalk collection IDs.

Usage:
  python3 .agents/scripts/shared/patch_deposit_crosswalk.py \
    --input deposit.xml --output deposit-patched.xml \
    --collection-id 80ca6e1d-fcc4-407f-9484-d3c64a420c73 | cat

Transform:
- Add `id="<uuid>"` to `<collection ...>` elements that do not already define id.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

COLLECTION_NO_ID_RE = re.compile(r"<collection(?![^>]*\bid\s*=)([^>]*)>")


def main() -> int:
    parser = argparse.ArgumentParser(description="Patch deposit crosswalk collection IDs.")
    parser.add_argument("--input", required=True, help="Input XML file")
    parser.add_argument("--output", required=True, help="Output XML file")
    parser.add_argument("--collection-id", required=True, help="Collection UUID to inject")
    args = parser.parse_args()

    src = pathlib.Path(args.input)
    dst = pathlib.Path(args.output)
    if not src.exists():
        print(f"ERROR: input file not found: {src}")
        return 1

    text = src.read_text(encoding="utf-8")
    patched, count = COLLECTION_NO_ID_RE.subn(
        rf'<collection id="{args.collection_id}"\1>',
        text,
    )

    dst.write_text(patched, encoding="utf-8")
    print(f"WROTE: {dst}")
    print(f"CHANGES: {count} collection element(s) received id")
    return 0


if __name__ == "__main__":
    sys.exit(main())


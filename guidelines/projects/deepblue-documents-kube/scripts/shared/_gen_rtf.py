#!/usr/bin/env python3
"""Generate a simple RTF draft template.

Usage:
  python3 .agents/scripts/shared/_gen_rtf.py --output communications/email-template.rtf | cat
"""

from __future__ import annotations

import argparse
import pathlib
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a basic RTF draft template.")
    parser.add_argument("--output", required=True, help="Output .rtf path")
    args = parser.parse_args()

    out_path = pathlib.Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    content = r"""{\rtf1\ansi
{\fonttbl{\f0 Arial;}{\f1 Courier New;}}
\f0\fs24
\b Subject:\b0 [fill in]\par
\b To:\b0 [fill in]\par
\b CC:\b0 [fill in]\par
\par
Hello,\par
\par
[Write message body]\par
\par
\b Technical details:\b0\par
\f1 [paste IDs, URLs, commands]\f0\par
\par
Thanks,\par
[Your name]\par
}
"""

    out_path.write_text(content, encoding="utf-8")
    print(f"WROTE: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())


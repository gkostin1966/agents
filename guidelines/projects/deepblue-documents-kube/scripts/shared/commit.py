#!/usr/bin/env python3
"""Create a git commit from a message file.

Usage:
  python3 .agents/scripts/shared/commit.py | cat
  python3 .agents/scripts/shared/commit.py --message-file .agents/scripts/shared/commit-msg.txt | cat

Notes:
- This script does not stage files.
- It runs `git commit -F <message-file>` in the current working directory.
"""

from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Commit with a message file.")
    parser.add_argument(
        "--message-file",
        default=".agents/scripts/shared/commit-msg.txt",
        help="Path to commit message file (default: .agents/scripts/shared/commit-msg.txt)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the git command and validate inputs without running commit.",
    )
    args = parser.parse_args()

    message_path = pathlib.Path(args.message_file)
    if not message_path.exists():
        print(f"ERROR: message file not found: {message_path}")
        return 1

    message = message_path.read_text(encoding="utf-8").strip()
    if not message:
        print(f"ERROR: message file is empty: {message_path}")
        return 1

    cmd = ["git", "commit", "-F", str(message_path)]
    if args.dry_run:
        print("DRY-RUN:", " ".join(cmd))
        return 0

    proc = subprocess.run(cmd)
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())


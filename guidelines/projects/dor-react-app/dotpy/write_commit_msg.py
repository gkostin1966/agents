#!/usr/bin/env python3
"""Write a commit message to .agents/dotpy/commit_msg.txt.

Usage:
  python3 .agents/dotpy/write_commit_msg.py < message.txt
  echo "subject line" | python3 .agents/dotpy/write_commit_msg.py

Reads the message from stdin and writes it to .agents/dotpy/commit_msg.txt,
then prints 'commit_msg.txt written.' to stdout.

After running this script, commit with:
  python3 .agents/dotpy/commit.py | cat
"""

import sys
from pathlib import Path

MSG_FILE = Path(__file__).parent / "commit_msg.txt"

msg = sys.stdin.read()
if not msg.strip():
    print("Error: no message provided on stdin.", file=sys.stderr)
    raise SystemExit(1)

MSG_FILE.write_text(msg, encoding="utf-8")
print("commit_msg.txt written.")


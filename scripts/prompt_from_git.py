#!/usr/bin/env python3
"""Build a compact AI-ready prompt from staged git changes.

Usage:
  python3 scripts/prompt_from_git.py | cat
  python3 scripts/prompt_from_git.py --max-diff-chars 4000 | cat
  python3 scripts/prompt_from_git.py --output /tmp/prompt.txt
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def _run_git(args: list[str]) -> str:
    proc = subprocess.run(
        ["git", "--no-pager", *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        stderr = (proc.stderr or "").strip()
        raise RuntimeError(stderr or f"git command failed: {' '.join(args)}")
    return proc.stdout


def _truncate(text: str, max_chars: int) -> tuple[str, bool]:
    if len(text) <= max_chars:
        return text, False
    suffix = "\n\n[diff truncated]\n"
    keep = max(0, max_chars - len(suffix))
    return text[:keep] + suffix, True


def build_prompt(branch: str, status_lines: list[str], diff_text: str, max_diff_chars: int) -> str:
    if not status_lines:
        raise ValueError("No staged files")

    truncated_diff, _ = _truncate(diff_text, max_diff_chars)

    files_block = "\n".join(f"- `{line}`" for line in status_lines)
    return (
        "Task: Review staged changes and produce implementation guidance.\n"
        "Constraints: concise bullets, code-only suggestions unless explanation requested.\n\n"
        f"Branch: `{branch}`\n\n"
        "Staged files:\n"
        f"{files_block}\n\n"
        "Staged diff:\n"
        "```diff\n"
        f"{truncated_diff}"
        "\n```\n"
    )


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Generate compact prompt text from staged git diff")
    p.add_argument("--max-diff-chars", type=int, default=6000, help="Max characters from staged diff")
    p.add_argument("--output", default=None, help="Write output to file instead of stdout")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.max_diff_chars < 500:
        print("Error: --max-diff-chars must be >= 500", file=sys.stderr)
        return 2

    try:
        branch = _run_git(["branch", "--show-current"]).strip() or "(detached)"
        status_raw = _run_git(["diff", "--cached", "--name-status"]).strip()
        if not status_raw:
            print("Error: no staged changes found", file=sys.stderr)
            return 1
        status_lines = [line for line in status_raw.splitlines() if line.strip()]
        diff_text = _run_git(["diff", "--cached"])
        prompt = build_prompt(branch, status_lines, diff_text, args.max_diff_chars)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.output:
        Path(args.output).write_text(prompt, encoding="utf-8")
        print(f"Written: {args.output}")
        return 0

    print(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


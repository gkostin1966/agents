#!/usr/bin/env python3
"""Check always-on instruction file size budgets.

Usage:
  python3 scripts/check_token_budgets.py | cat
  python3 scripts/check_token_budgets.py --repo-root /path/to/agents | cat
  python3 scripts/check_token_budgets.py --check AGENTS.md:80:4500 --check .github/copilot-instructions.md:8:300 | cat
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BudgetCheck:
    relative_path: str
    max_lines: int
    max_bytes: int


DEFAULT_CHECKS: tuple[BudgetCheck, ...] = (
    BudgetCheck("AGENTS.md", 90, 5000),
    BudgetCheck("guidelines/base/AGENTS.md", 70, 3500),
    BudgetCheck(".github/copilot-instructions.md", 10, 500),
)


@dataclass(frozen=True)
class CheckResult:
    check: BudgetCheck
    lines: int
    bytes_size: int
    exists: bool

    @property
    def ok(self) -> bool:
        return self.exists and self.lines <= self.check.max_lines and self.bytes_size <= self.check.max_bytes


def _parse_check(value: str) -> BudgetCheck:
    parts = value.split(":")
    if len(parts) != 3:
        raise argparse.ArgumentTypeError(
            f"Invalid --check '{value}'. Expected format: path:max_lines:max_bytes"
        )
    path, max_lines, max_bytes = parts
    try:
        lines = int(max_lines)
        bytes_size = int(max_bytes)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"Invalid limits in --check '{value}'. max_lines and max_bytes must be integers"
        ) from exc

    if lines < 1 or bytes_size < 1:
        raise argparse.ArgumentTypeError(
            f"Invalid limits in --check '{value}'. max_lines and max_bytes must be >= 1"
        )

    return BudgetCheck(path, lines, bytes_size)


def _run_check(repo_root: Path, check: BudgetCheck) -> CheckResult:
    path = repo_root / check.relative_path
    if not path.exists():
        return CheckResult(check, 0, 0, False)

    data = path.read_text(encoding="utf-8")
    lines = len(data.splitlines())
    bytes_size = len(data.encode("utf-8"))
    return CheckResult(check, lines, bytes_size, True)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check always-on instruction file budgets")
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Path to agents repository root (default: current directory)",
    )
    parser.add_argument(
        "--check",
        action="append",
        type=_parse_check,
        default=None,
        help="Custom check in format path:max_lines:max_bytes (repeatable)",
    )
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    repo_root = Path(args.repo_root).expanduser().resolve()
    checks = tuple(args.check) if args.check else DEFAULT_CHECKS

    failures = 0
    for check in checks:
        result = _run_check(repo_root, check)
        if not result.exists:
            print(f"MISSING  {check.relative_path}")
            failures += 1
            continue

        status = "OK     " if result.ok else "TOO_BIG"
        print(
            f"{status} {check.relative_path} "
            f"lines={result.lines}/{check.max_lines} bytes={result.bytes_size}/{check.max_bytes}"
        )
        if not result.ok:
            failures += 1

    if failures:
        print(f"\nBudget check failed: {failures} file(s) exceeded limits or were missing.")
        return 1

    print("\nBudget check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


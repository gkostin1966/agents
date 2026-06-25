#!/usr/bin/env python3
"""Validate encoded backend ConfigMap keys.

Usage:
  python3 .agents/scripts/shared/validate_cm_keys.py | cat
  python3 .agents/scripts/shared/validate_cm_keys.py --upstream path/to/upstream.dspace.cfg | cat

Checks:
- Finds keys in backend-cm jsonnet files that contain __P__ / __D__ encoding.
- Decodes to dotted DSpace property names.
- Flags suspicious token patterns as ERRORS.
- Optionally compares decoded properties to upstream cfg keys and reports WARNINGS.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from dataclasses import dataclass
from typing import Iterable, List, Set

KEY_RE = re.compile(r"^\s*(?:'([^']+)'|\"([^\"]+)\"|([A-Za-z0-9_]+))\s*:")
UPSTREAM_KEY_RE = re.compile(r"^\s*([A-Za-z0-9_.-]+)\s*=")


@dataclass
class Finding:
    level: str
    file: pathlib.Path
    line_no: int
    key: str
    detail: str


def iter_backend_cm_files(repo_root: pathlib.Path) -> Iterable[pathlib.Path]:
    candidates = [repo_root / "lib" / "deepblue-backend-cm.jsonnet"]
    env_dir = repo_root / "environments" / "deepblue-documents"
    if env_dir.exists():
        for child in sorted(env_dir.iterdir()):
            path = child / "backend-cm.jsonnet"
            if path.exists():
                candidates.append(path)
    return candidates


def decode_key(key: str) -> str:
    return key.replace("__P__", ".").replace("__D__", "-")


def parse_upstream_keys(path: pathlib.Path) -> Set[str]:
    keys: Set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        m = UPSTREAM_KEY_RE.match(line)
        if m:
            keys.add(m.group(1))
    return keys


def validate_file(path: pathlib.Path, upstream_keys: Set[str] | None) -> List[Finding]:
    findings: List[Finding] = []
    lines = path.read_text(encoding="utf-8").splitlines()

    for idx, line in enumerate(lines, start=1):
        m = KEY_RE.match(line)
        if not m:
            continue
        key = m.group(1) or m.group(2) or m.group(3) or ""

        if "__P__" not in key and "__D__" not in key:
            continue

        decoded = decode_key(key)

        if "__" in decoded:
            findings.append(Finding("ERROR", path, idx, key, "decoded key still contains '__' token"))
            continue

        if re.search(r"[^A-Za-z0-9_.-]", decoded):
            findings.append(Finding("ERROR", path, idx, key, f"decoded key has invalid character(s): {decoded}"))
            continue

        if upstream_keys is not None and decoded not in upstream_keys:
            findings.append(Finding("WARN", path, idx, key, f"decoded property not found in upstream list: {decoded}"))

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate backend ConfigMap encoded keys.")
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root (default: current directory)",
    )
    parser.add_argument(
        "--upstream",
        default="",
        help="Optional path to upstream dspace.cfg for warning-level cross-check",
    )
    args = parser.parse_args()

    repo_root = pathlib.Path(args.repo_root).resolve()
    upstream_keys: Set[str] | None = None
    if args.upstream:
        upstream_path = pathlib.Path(args.upstream)
        if not upstream_path.exists():
            print(f"ERROR: upstream file not found: {upstream_path}")
            return 1
        upstream_keys = parse_upstream_keys(upstream_path)

    findings: List[Finding] = []
    files = list(iter_backend_cm_files(repo_root))
    if not files:
        print("ERROR: no backend-cm jsonnet files found")
        return 1

    for path in files:
        findings.extend(validate_file(path, upstream_keys))

    errors = [f for f in findings if f.level == "ERROR"]
    warns = [f for f in findings if f.level == "WARN"]

    for f in findings:
        print(f"{f.level}: {f.file}:{f.line_no}: {f.key} -> {f.detail}")

    print(f"\nChecked {len(files)} files. ERRORS={len(errors)} WARNINGS={len(warns)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())


#!/usr/bin/env python3
"""Basic DSpace RT2 readiness checks.

Usage:
  python3 .agents/scripts/shared/check_dspace_rt2.py \
    --api-url https://backend.demo.../server/api \
    --oai-url https://backend.demo.../server/oai/request | cat

This is a lightweight non-destructive checker for:
- API endpoint reachability
- OAI-PMH endpoint reachability
"""

from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.request


def check_url(url: str, timeout: int) -> tuple[bool, str]:
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return True, f"HTTP {resp.status}"
    except urllib.error.HTTPError as exc:
        return False, f"HTTP {exc.code}"
    except Exception as exc:  # pragma: no cover - diagnostic path
        return False, str(exc)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check DSpace RT2 endpoint readiness.")
    parser.add_argument("--api-url", required=True, help="DSpace REST API base URL")
    parser.add_argument("--oai-url", required=True, help="DSpace OAI-PMH URL")
    parser.add_argument("--timeout", type=int, default=15, help="HTTP timeout seconds")
    args = parser.parse_args()

    checks = [
        ("REST API", args.api_url),
        ("OAI-PMH", args.oai_url),
    ]

    failures = 0
    for label, url in checks:
        ok, detail = check_url(url, args.timeout)
        status = "PASS" if ok else "FAIL"
        print(f"{status}: {label}: {url} ({detail})")
        if not ok:
            failures += 1

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())


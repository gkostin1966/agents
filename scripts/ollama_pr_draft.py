#!/usr/bin/env python3
"""Generate a concise PR draft from diff/context text using local Ollama.

Usage:
  git --no-pager diff --staged | python3 scripts/ollama_pr_draft.py | cat
  python3 scripts/ollama_pr_draft.py --input /tmp/diff.txt --title "feat: sample" | cat
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib import error, request


DEFAULT_MODEL = "qwen2.5-coder:7b"
DEFAULT_HOST = "http://localhost:11434"


def _build_payload(diff_text: str, model: str, title_hint: str | None) -> dict[str, object]:
    title_line = f"Title hint: {title_hint}\n" if title_hint else ""
    prompt = (
        "Write a concise markdown PR draft.\n"
        "Format exactly:\n"
        "## <Title>\n"
        "### Summary\n"
        "### Changes\n"
        "### Notes\n"
        "Use short bullets. No filler.\n\n"
        f"{title_line}"
        "Diff/context:\n"
        f"{diff_text}"
    )
    return {"model": model, "prompt": prompt, "stream": False}


def request_ollama(payload: dict[str, object], host: str, timeout: float) -> str:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        f"{host.rstrip('/')}/api/generate",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except error.URLError as exc:
        raise RuntimeError(f"Failed to reach Ollama at {host}: {exc}") from exc

    output = data.get("response")
    if not isinstance(output, str) or not output.strip():
        raise RuntimeError("Ollama response missing 'response' text")
    return output.strip()


def _read_input(path: str | None) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8")
    return sys.stdin.read()


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Generate PR draft markdown using local Ollama")
    p.add_argument("--input", default=None, help="Diff/context text file path (default: stdin)")
    p.add_argument("--title", default=None, help="Optional title hint")
    p.add_argument("--model", default=DEFAULT_MODEL, help=f"Ollama model (default: {DEFAULT_MODEL})")
    p.add_argument("--host", default=DEFAULT_HOST, help=f"Ollama host (default: {DEFAULT_HOST})")
    p.add_argument("--timeout", type=float, default=90.0, help="HTTP timeout seconds (default: 90)")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    diff_text = _read_input(args.input)
    if not diff_text.strip():
        print("Error: input text is empty", file=sys.stderr)
        return 2

    payload = _build_payload(diff_text, args.model, args.title)
    try:
        result = request_ollama(payload, args.host, args.timeout)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


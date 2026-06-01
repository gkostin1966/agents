#!/usr/bin/env python3
"""Compress a verbose prompt using a local Ollama model.

Usage:
  python3 scripts/ollama_prompt_compress.py < prompt.txt | cat
  python3 scripts/ollama_prompt_compress.py --input prompt.txt --model qwen2.5-coder:7b | cat
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib import error, request


DEFAULT_MODEL = "qwen2.5-coder:7b"
DEFAULT_HOST = "http://localhost:11434"
DEFAULT_INSTRUCTION = (
    "Rewrite the user text as a compact coding prompt. Keep technical meaning exact. "
    "Drop filler and pleasantries. Use short imperative style."
)


def _build_payload(text: str, instruction: str, model: str) -> dict[str, object]:
    prompt = (
        f"{instruction}\n\n"
        "Output only rewritten prompt. No explanation.\n\n"
        "User text:\n"
        f"{text}"
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
    p = argparse.ArgumentParser(description="Compress a prompt using local Ollama")
    p.add_argument("--input", default=None, help="Input text file path (default: stdin)")
    p.add_argument("--model", default=DEFAULT_MODEL, help=f"Ollama model (default: {DEFAULT_MODEL})")
    p.add_argument("--host", default=DEFAULT_HOST, help=f"Ollama host (default: {DEFAULT_HOST})")
    p.add_argument("--timeout", type=float, default=60.0, help="HTTP timeout seconds (default: 60)")
    p.add_argument(
        "--instruction",
        default=DEFAULT_INSTRUCTION,
        help="Compression instruction prefix",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    text = _read_input(args.input)
    if not text.strip():
        print("Error: input text is empty", file=sys.stderr)
        return 2

    payload = _build_payload(text, args.instruction, args.model)
    try:
        result = request_ollama(payload, args.host, args.timeout)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


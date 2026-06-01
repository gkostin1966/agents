from __future__ import annotations

import io
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ollama_pr_draft  # type: ignore
import ollama_prompt_compress  # type: ignore


class OllamaPromptCompressTests(unittest.TestCase):
    def test_build_payload_contains_instruction_and_text(self) -> None:
        payload = ollama_prompt_compress._build_payload("hello", "Compress now", "demo")
        self.assertEqual(payload["model"], "demo")
        self.assertIn("Compress now", str(payload["prompt"]))
        self.assertIn("hello", str(payload["prompt"]))

    def test_main_prints_result_from_mocked_request(self) -> None:
        original_request = ollama_prompt_compress.request_ollama
        original_stdin = sys.stdin
        try:
            ollama_prompt_compress.request_ollama = lambda payload, host, timeout: "short prompt"
            sys.stdin = io.StringIO("Verbose request text")
            out = io.StringIO()
            with redirect_stdout(out):
                code = ollama_prompt_compress.main([])
            self.assertEqual(code, 0)
            self.assertIn("short prompt", out.getvalue())
        finally:
            ollama_prompt_compress.request_ollama = original_request
            sys.stdin = original_stdin


class OllamaPrDraftTests(unittest.TestCase):
    def test_build_payload_includes_title_hint_when_present(self) -> None:
        payload = ollama_pr_draft._build_payload("diff content", "demo", "feat: title")
        text = str(payload["prompt"])
        self.assertIn("Title hint: feat: title", text)
        self.assertIn("diff content", text)

    def test_main_errors_on_empty_input(self) -> None:
        original_stdin = sys.stdin
        try:
            sys.stdin = io.StringIO("")
            err = io.StringIO()
            with redirect_stderr(err):
                code = ollama_pr_draft.main([])
            self.assertEqual(code, 2)
            self.assertIn("input text is empty", err.getvalue())
        finally:
            sys.stdin = original_stdin


if __name__ == "__main__":
    unittest.main()


# Agent Rules — agents (meta-framework project)

> Read at start of every session. Governs framework work only — not mounted projects.

## Scope

Two roles: (1) guidelines/prompt/task-tracking store for mounted projects; (2) `agentsfw` Python CLI.

Project catalog: `config/projects.json`. First-time mount → add entry there first.
File layout: `src/agents_framework/`, `guidelines/base/`, `guidelines/projects/<name>/`, `tests/`, `scripts/`.

## File Access — Landmines

- `mounted-projects/` is **read-only**. Never create/edit/delete files there.
- Never read `AGENT_QUIZ_ANSWERS.md` until all quiz answers written **and** developer explicitly says to compare.

## Guidelines Architecture — Key Rules

- `guidelines/base/AGENTS.md` — shared; `guidelines/projects/<name>/AGENTS.md` — per-project overrides.
- Root `AGENTS.md` — meta-rules for framework work only.
- Matching `## Heading` in project file **replaces** the base section entirely.
- Edit base → regenerate all: `PYTHONPATH=src python3 -m agents_framework.cli guidelines generate all`
- Edit project → regenerate one: `PYTHONPATH=src python3 -m agents_framework.cli guidelines generate <name>`
- Same pattern for prompts: `prompt generate all / <name>`

## Task Tracking — Rules

- Add task to `AGENT_TODO.md` **before** executing any multi-step plan.
- Every task must end with `- [ ] Verify with the developer that the task is complete`.
- Only when all subtasks done: remove from `AGENT_TODO.md`, prepend to `AGENT_DONE.md` with timestamp.
- Reorder tasks with Python only — never string-replace.

## CLI — Landmines

- Paging: `git --no-pager <cmd>` or `| cat`. Never rely on interactive input.
- **No multiline code via `-c` flags** — zsh mangling triggers `dquote>` mode, corrupts session.
- **No shell heredocs** (`<< 'MARKER'`) — same corruption risk.
- Fix for both: write to file (`scripts/<name>.py` or `/tmp/run.py`), run with `python3 <path> | cat`.
- If terminal is stuck (no output / garbled): run the heredoc end-marker (`EOF`, `PYEOF`, etc.) as a standalone command to escape.
- Framework CLI: always `PYTHONPATH=src python3 -m agents_framework.cli <subcommand>`.

## Framework Code — Landmines

- **Always run tests** after modifying framework code: `PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py'`
- **No external dependencies** — stdlib only. No third-party packages without developer approval.
- Python 3.10+: use `list[str]`, `dict[str, str]` — not `typing.List`/`typing.Dict`.
- New module → add to `src/agents_framework/`, import in `cli.py`, add `tests/test_<module>.py`.
- New CLI subcommand → `sub.add_parser(...)` in `build_parser()`, wire in `main()`, add tests.

## Git — Landmines

- Never `git commit -m "..."` for multiline messages — zsh mangles them.
- Write message to `/tmp/commit-msg.txt`, then `git commit -F /tmp/commit-msg.txt | cat`.
- Single-line only exception: `git commit -m "chore: one line" | cat`.
- Never amend, never force-push, never push to `main`.

## PR Summary

Write to `pr-summary.md` (gitignored). Structure: `## Title`, `### Summary`, `### Changes`, `### Notes`. Delete after use.

## Markdown Tables

Data rows define required column width. Pad header and separator to match widest data cell.


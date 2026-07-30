# Agent Rules - Base Guidelines

> Shared rules for mounted projects. Matching `## Heading` in project files replaces base sections.

## Quick Session Checklist

- `[always]` Run startup orientation commands; stop for unexpected branch or working state.
- `[always]` Read local `AGENTS.md` and apply project overrides.
- `[when-bookkeeping]` Read/update task files before and after substantive work.
- `[when-committing]` Base commit guidance on tracked/staged files only.

## .agents Policy

- Treat `.agents/` as shared framework metadata and long-term memory.
- Keep `.agents/` updates separate from normal app-code commit scope.
- Do not commit `.agents/` files in mounted repos unless the developer explicitly asks.

## File Access

- Stay in the project directory; outside files are read-only and only when explicitly requested.
- Never read `AGENT_QUIZ_ANSWERS.md` until all quiz answers are written and permission is explicit.
- Temporary files go in `.agents/tmp/` (for example `.agents/tmp/run.py`, `.agents/tmp/commit-msg.txt`), not system `/tmp`.

## Command-Line Safety

- Use `git --no-pager <cmd>` or `| cat`; avoid interactive paging.
- Never use multiline code with `-c` flags in zsh.
- Never use shell heredocs (`<< 'MARKER'`) in zsh sessions.
- Write code to a file, then run it (for example `python3 scripts/myscript.py | cat` or `python3 .agents/tmp/run.py | cat`).
- If terminal output is stuck/garbled, run the heredoc end marker (`EOF`, `PYEOF`, and similar) as a standalone command.

## Python Utility Scripts

- Check `scripts/README.md` or `dotpy/README.md` before creating ad-hoc helpers.
- Save reusable scripts in the project utility dir with shebang, Usage docstring, and README entry.
- If no utility dir exists, use `.agents/tmp/run.py`.

## Git Commits

- Never amend, force-push, or push to `main`.
- Commit suggestions must come from current tracked/staged state (`git status`, `git diff --staged`).
- Do not suggest speculative commits or include untracked `.agents/` files.
- For multiline messages, write `.agents/tmp/commit-msg.txt`, then run `git commit -F .agents/tmp/commit-msg.txt | cat`.
- If available, prefer `scripts/commit.py` or `dotpy/commit.py` for multiline commit flow.
- Single-line exception: `git commit -m "chore: one line" | cat`.

## Pull Request Summaries

- Write to `pr-summary.md` (gitignored): `## Title`, `### Summary`, `### Changes`, `### Notes`.

## Email Drafts

- Write drafts as Markdown under `communications/<channel>-<topic>.md`.
- `communications/` is tracked; do not gitignore individual draft files.

## Markdown Tables

Data rows define required column width. Pad header and separator to the widest data cell.

## Response Hygiene

- Separate verified facts from assumptions; label unknowns explicitly.
- Do not suggest next steps that conflict with repository rules.
- If task metadata is clearly stale or inconsistent, fix it proactively and report the correction.


# Agent Rules — Base Guidelines

> Shared rules for all mounted projects. Project `## Heading` overrides replace base sections.

## Quick Session Checklist

- `[always]` Run startup orientation commands and stop for unexpected branch/working state.
- `[always]` Read local project `AGENTS.md` and follow project-specific overrides.
- `[always]` Identify the active ticket key from branch naming rules.
- `[when-bookkeeping]` Read/update task state files before and after substantive work.
- `[when-committing]` Base commit guidance on tracked/staged files only.

## Rule Tags

- `[always]` Applies to every session/task.
- `[when-bookkeeping]` Applies when maintaining `.agents` task/status metadata.
- `[when-committing]` Applies when preparing, suggesting, or executing commit actions.

## `.agents` Policy (Canonical)

- `[always]` Treat `.agents/` as shared agent-framework metadata and long-term memory.
- `[always]` Maintain relevant `.agents/` files in place when required for the active task.
- `[always]` Do not treat `.agents/` updates as normal app-code commit content in mounted repositories.
- `[always]` Agents do not commit `.agents/` files in mounted repositories unless the developer explicitly directs otherwise.

## File Access

- Stay within the project directory. Outside file: read only the specific file requested — no browsing.
- **Never read `AGENT_QUIZ_ANSWERS.md`** until all quiz answers written **and** developer explicitly grants permission.
- Create temporary files in `.agents/tmp/` only (for example `.agents/tmp/run.py`, `.agents/tmp/commit-msg.txt`) — never system `/tmp`.
- Follow `## .agents Policy (Canonical)` for ownership and commit-boundary rules.

## Command-Line Tool Usage

- Paging: `git --no-pager <cmd>` or `| cat`. Never interactive input.
- **Never multiline code via `-c` flags** — zsh triggers `dquote>` heredoc mode, corrupts session silently.
- **Never shell heredocs** (`<< 'MARKER'`) — same corruption risk; previous unclosed `<<` swallows all subsequent commands.
- Fix for both: write to file, run the file:
  ```shell
  python3 scripts/myscript.py | cat   # reusable
  python3 .agents/tmp/run.py | cat    # one-off
  ```
- If terminal stuck (no output / garbled): run the heredoc end-marker (`EOF`, `PYEOF`, etc.) as a standalone command to escape.

## Python Utility Scripts

- Check project utility-script dir first (`scripts/README.md` or `dotpy/README.md`) before writing ad-hoc helpers.
- Save reusable scripts there; add shebang + Usage docstring + README entry.
- No utility dir → write to `.agents/tmp/run.py`.

## Git Commits

- Never amend. Never force-push. Never push to `main`.
- When preparing or discussing commits in this repository, reason only from the current tracked/staged file set (`git status` / `git diff --staged`). Do not ask to commit `.agents/` files when they are not trackable/staged.
- Do not make speculative commit suggestions. Only suggest commit actions grounded in the current tracked/staged set.
- **Never `git commit -m "..."` for multiline** — write to `.agents/tmp/commit-msg.txt`, then `git commit -F .agents/tmp/commit-msg.txt | cat`.
- If project has `scripts/commit.py` or `dotpy/commit.py`, use that instead.
- Single-line exception: `git commit -m "chore: one line" | cat`.

## Pull Request Summaries

- Write to `pr-summary.md` (gitignored). Structure: `## Title`, `### Summary`, `### Changes`, `### Notes`. Delete after use.

## Email Drafts for Third Parties

- Write drafts as `.md` files under `communications/<channel>-<topic>.md` (e.g. `communications/email-its-request.md`).
- `communications/` is tracked in git. Do not gitignore individual draft files.

## Markdown Tables

Data rows define required column width. Pad header and separator to match widest data cell.

## Response Hygiene

- Distinguish verified facts from assumptions. If something is not verified, label it explicitly.
- Do not suggest next steps that conflict with repository rules.
- If task metadata is clearly stale or inconsistent (for example ticket index summary/status drift, or `STATUS.md` not matching `TODO.md`), fix it proactively and report the change. Do not ask for permission first when the correction is clear and non-destructive.


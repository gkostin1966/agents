# AGENTS.md — dspace-angular (mlibrary/dspace-angular)

> Project-specific rules. Sections with matching `## Heading` values override the base guidelines.

## Project Context

| Item               | Value                                                                |
|--------------------|----------------------------------------------------------------------|
| Repo               | `mlibrary/dspace-angular`                                            |
| Framework          | Angular 14 / DSpace 7.6                                              |
| Language           | TypeScript + HTML templates                                          |
| Base branch        | `umich`                                                              |
| Ticket prefix      | `DEEPBLUE-`                                                          |
| Commit convention  | `feat|fix|chore|docs|test: message (DEEPBLUE-NNN)`                   |

## Quick Session Checklist

- `[always]` Run startup orientation commands and stop for unexpected branch/working state.
- `[always]` Read this file (`.agents/AGENTS.md`) — **not** a root-level `AGENTS.md` (none exists).
- `[always]` Identify the active ticket key from branch naming rules.
- `[when-bookkeeping]` Read/update `.agents/AGENT_TODO.md` and `.agents/AGENT_DONE.md` before and after substantive work.
- `[when-committing]` Base commit guidance on tracked/staged files only.

## Task Files

| File                                    | Purpose                                     |
|-----------------------------------------|---------------------------------------------|
| `.agents/AGENT_TODO.md`                 | Remaining tasks — work top to bottom        |
| `.agents/AGENT_DONE.md`                 | Completed task archive                      |
| `.agents/PLAN_DSPACE_ANGULAR_PASSWORD_LOGIN.md` | DEEPBLUE-466 design rationale & code snippets |
| `.agents/DEEPBLUE-466-PR.md`            | PR description for DEEPBLUE-466             |
| `.agents/DEEPBLUE-466-AGENTS.md`        | Archived feature-specific agent context for DEEPBLUE-466 |

**Always check `.agents/AGENT_TODO.md` first** to see what still needs doing.
**After completing and committing each task**, move it from `AGENT_TODO.md` to `AGENT_DONE.md`.

## Branch Naming

Branch names map to ticket keys:
- `show-password-login` → DEEPBLUE-466 (merged to `umich` ✅)

Cut new feature branches from `umich`:
```shell
git checkout umich && git pull && git checkout -b my-feature-name
```

## Test Commands

```shell
# Run a single spec file (non-interactive):
npx ng test --include='**/log-in/log-in.component.spec.ts' \
  --watch=false --configuration test --browsers=ChromeHeadless

# Full test suite (slow — use only when needed):
npx ng test --watch=false --configuration test --browsers=ChromeHeadless
```

## Rule Tags

- `[always]` Applies to every session/task.
- `[when-bookkeeping]` Applies when maintaining `.agents` task/status metadata.
- `[when-committing]` Applies when preparing, suggesting, or executing commit actions.

## `.agents` Policy (Canonical)

- `[always]` Treat `.agents/` as shared agent-framework metadata and long-term memory.
- `[always]` Maintain relevant `.agents/` files in place when required for the active task.
- `[always]` Do not treat `.agents/` updates as normal app-code commit content in mounted repositories.
- `[always]` Agents do not commit `.agents/` files in mounted repositories unless the developer explicitly directs otherwise.
- `[always]` Agent files (`AGENT_TODO.md`, `AGENT_DONE.md`, plans, etc.) live in `.agents/` — **not** the project root.

## File Access

- Stay within the project directory. Outside file: read only the specific file requested — no browsing.
- **Never read `AGENT_QUIZ_ANSWERS.md`** until all quiz answers written **and** developer explicitly grants permission.
- Create temporary files in `.agents/tmp/` only (for example `.agents/tmp/run.py`, `.agents/tmp/commit-msg.txt`) — never system `/tmp`.
- Follow `## .agents Policy (Canonical)` for ownership and commit-boundary rules.

## Command-Line Tool Usage

- Paging: `git --no-pager <cmd>` or `| cat`. Never interactive input.
- **Always pass non-interactive flags to `ng test`:** `--watch=false --browsers=ChromeHeadless`
- **Never multiline code via `-c` flags** — zsh triggers `dquote>` heredoc mode, corrupts session silently.
- **Never shell heredocs** (`<< 'MARKER'`) — same corruption risk.
- Fix for both: write to file, run the file:
  ```shell
  python3 .agents/tmp/run.py | cat    # one-off
  ```
- If terminal stuck (no output / garbled): run the heredoc end-marker (`EOF`, `PYEOF`, etc.) as a standalone command to escape.

## Python Utility Scripts

- Check project utility-script dir first (`scripts/README.md`) before writing ad-hoc helpers.
- No utility dir → write to `.agents/tmp/run.py`.

## Git Commits

- Never amend. Never force-push. Never push to `main`.
- When preparing or discussing commits in this repository, reason only from the current tracked/staged file set (`git status` / `git diff --staged`). Do not ask to commit `.agents/` files when they are not trackable/staged.
- Do not make speculative commit suggestions. Only suggest commit actions grounded in the current tracked/staged set.
- **Never `git commit -m "..."` for multiline** — write to `.agents/tmp/commit-msg.txt`, then `git commit -F .agents/tmp/commit-msg.txt | cat`.
- Single-line exception: `git commit -m "chore: one line" | cat`.

## Pull Request Summaries

- Write to `.agents/pr-summary.md` (not tracked in project git). Structure: `## Title`, `### Summary`, `### Changes`, `### Notes`. Delete after use.

## Markdown Tables

Data rows define required column width. Pad header and separator to match widest data cell.

## Response Hygiene

- Distinguish verified facts from assumptions. If something is not verified, label it explicitly.
- Do not suggest next steps that conflict with repository rules.
- If task metadata is clearly stale or inconsistent, fix it proactively and report the change. Do not ask for permission first when the correction is clear and non-destructive.
- After editing each TypeScript file, run `get_errors` on that file and fix any issues before moving on.

# Agent Rules — boxrunner

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

- `[always]` Stay within the project directory. Outside file: read only the specific file requested — no browsing.
- `[always]` **Never read `AGENT_QUIZ_ANSWERS.md`** until all quiz answers written **and** developer explicitly grants permission.
- `[always]` Create temporary files in `.agents/tmp/` only (for example `.agents/tmp/run.py`, `.agents/tmp/commit-msg.txt`) — never system `/tmp`.
- `[always]` Follow `## .agents Policy (Canonical)` for ownership and commit-boundary rules.

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

- `[when-committing]` Never amend. Never force-push. Never push to `main`.
- `[when-committing]` When preparing or discussing commits in this repository, reason only from the current tracked/staged file set (`git status` / `git diff --staged`). Do not ask to commit `.agents/` files when they are not trackable/staged here.
- `[when-committing]` Do not make speculative commit suggestions. Only suggest commit actions grounded in the current tracked/staged set.
- `[when-committing]` **Never `git commit -m "..."` for multiline** — write to `.agents/tmp/commit-msg.txt`, then `git commit -F .agents/tmp/commit-msg.txt | cat`.
- `[when-committing]` If project has `scripts/commit.py` or `dotpy/commit.py`, use that instead.
- `[when-committing]` Single-line exception: `git commit -m "chore: one line" | cat`.

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
- If task metadata is clearly stale or inconsistent (for example `tasks/README.md` summary/status drift, or `STATUS.md` not matching `TODO.md`), fix it proactively and report the change. Do not ask for permission first when the correction is clear and non-destructive.

## Session State (`tasks/ARC-nnn/STATUS.md`)

Apply this section whenever the current task needs `.agents/` bookkeeping; these files are long-term memory for future agents, not application code.

At session start: (1) identify ticket from branch name by extracting a key matching `ARC-\d+` (e.g. `ARC-42/my-feature` -> `ARC-42`), (2) if the branch name does not contain an `ARC-\d+` key, list open tickets from `.agents/tasks/README.md` and ask the developer which ticket to focus on, (3) if `tasks/ARC-nnn/` does not exist yet for the selected ticket, create `TODO.md`, `STATUS.md`, and `plans/` plus a row in `tasks/README.md`, (4) read `tasks/ARC-nnn/STATUS.md` in full, (5) cross-check open subtasks against `TODO.md` — `TODO.md` is authoritative.

During session: update `STATUS.md` when a subtask completes, a plan changes, or a key decision is made.

End of session: update Last Updated, Recent Activity, Next Steps. `.agents` files are maintained separately and should be edited in place; Git staging/commit/archival for `.agents` is handled manually by the developer unless explicitly requested.

- `Open Tasks` in `STATUS.md` must mirror unchecked subtasks in `TODO.md` exactly at session end.
- Add a `Verification Evidence` subsection in `STATUS.md` with commands run, outcomes, and explicit blockers.
- If verification is blocked, report: blocker, exact command attempted, observed output/error, and what remains unverified.

| Section               | Contents                                                               |
|-----------------------|------------------------------------------------------------------------|
| Last Updated    | ISO date + one-line session summary                                    |
| Current Branch  | Active git branch name; brief note on other local branches if relevant |
| Open Tasks      | Copy of unchecked subtasks from `TODO.md`; key files for each task     |
| Open Plans      | Table of files in `tasks/ARC-nnn/plans/` with purpose and status       |
| Recent Activity | Bullet list of meaningful changes made in the most recent session      |
| Key Context     | Decisions, design notes, or gotchas the next agent needs to understand |
| Next Steps      | Ordered list of what to do next, specific enough to act on immediately |
| Verification Evidence | Commands run, key results, blockers, and unverified scope         |

## Task Tracking (`tasks/ARC-nnn/TODO.md` / `tasks/ARC-nnn/DONE.md`)

Apply this section whenever the current task needs `.agents/` task bookkeeping; these files are long-term memory for future agents, not application code.

Primary location: `.agents/tasks/ARC-nnn/` (TODO.md, DONE.md, STATUS.md, plans/).

Fallback location when `.agents` is unavailable: `AGENTS_ROOT/guidelines/projects/boxrunner/tasks/ARC-nnn/`.

New ticket: `mkdir -p .agents/tasks/ARC-nnn/plans` + create TODO.md + STATUS.md + row in `.agents/tasks/README.md`.

- Record plan in `TODO.md` before executing. Check off (`- [x]`) as completed.
- Every task ends with `- [ ] Verify with the developer that the task is complete`.
- Task lifecycle: `In Progress` -> `Developer Verified` -> `Merged` -> `Archived`.
- All done → create `tasks/ARC-nnn/DONE.md` with timestamp + summary + checklist.
- If PR review requests follow-up after a task was marked complete, reopen the same ticket: add new unchecked subtasks to `TODO.md`, update `STATUS.md` (`Open Tasks`, `Recent Activity`, `Next Steps`), and keep the task under `.agents/tasks/ARC-nnn/` until it is re-verified.
- After the related PR merges, archive with `git mv .agents/tasks/ARC-nnn .agents/archive/ARC-nnn` (create `.agents/archive/` if missing).
- Ticket archival and any `.agents`-side Git operations are handled outside normal app-code work in the separate agent-framework project; the agent should not assume it needs to manage `.agents` commits as part of the current project task here.
- Reorder subtasks with Python only — never string-replace.

## Ruby on Rails Conventions

- **All application commands run inside the Docker container.** Never against system Ruby/Node.
- Start stack: `docker compose up` (starts all services: `app`, `redis`, `resque`, `resque-web`, `solr`, `zookeeper`).
- After first `docker compose up`, initialize Solr collection: `/bin/bash ./solr/dev-init.sh`
- **RuboCop before committing Ruby files**:
  - Auto-fix: `docker compose exec app bundle exec rubocop -a | cat`
  - Check: `docker compose exec app bundle exec rubocop | cat`
- **Tests**: `docker compose exec app bundle exec rails test | cat`
- **Rails console**: `docker compose exec app bundle exec rails console`
- **Ruby version**: 3.4.9 (see `.ruby-version` and `Dockerfile ARG RUBY_VERSION`).
- **Rails version**: ~> 8.1.3 (see `Gemfile`).
- **Database**: SQLite 3 (see `Gemfile`; `db:prepare` runs automatically in `docker-entrypoint`).
- **Solr**: version 9.7, SolrCloud mode with ZooKeeper. Collection name: `blacklight-collection`. Config dir: `solr/conf/`.
- `SOLR_URL` env var: `http://solr:8983/solr/blacklight-collection` (set in `compose.yml`).


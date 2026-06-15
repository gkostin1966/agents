# Agent Rules — boxrunner

## File Access

- Stay within the project directory. Outside file: read only the specific file requested — no browsing.
- **Never read `AGENT_QUIZ_ANSWERS.md`** until all quiz answers written **and** developer explicitly grants permission.
- Create temporary files in `.agents/tmp/` only (for example `.agents/tmp/run.py`, `.agents/tmp/commit-msg.txt`) — never system `/tmp`.

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

## Session State (`tasks/ARC-nnn/STATUS.md`)

At session start: (1) identify ticket from branch name (e.g. `ARC-42/my-feature` → `ARC-42`), (2) if `tasks/ARC-nnn/` does not exist yet, create `TODO.md`, `STATUS.md`, and `plans/` plus a row in `tasks/README.md`, (3) read `tasks/ARC-nnn/STATUS.md` in full, (4) cross-check open subtasks against `TODO.md` — `TODO.md` is authoritative.

During session: update `STATUS.md` when a subtask completes, a plan changes, or a key decision is made.

End of session: update Last Updated, Recent Activity, Next Steps. `.agents` files are maintained separately and should be edited in place; Git staging/commit/archival for `.agents` is handled manually by the developer unless explicitly requested.

| Section         | Contents                                                               |
|-----------------|------------------------------------------------------------------------|
| Last Updated    | ISO date + one-line session summary                                    |
| Current Branch  | Active git branch name; brief note on other local branches if relevant |
| Open Tasks      | Copy of unchecked subtasks from `TODO.md`; key files for each task     |
| Open Plans      | Table of files in `tasks/ARC-nnn/plans/` with purpose and status       |
| Recent Activity | Bullet list of meaningful changes made in the most recent session      |
| Key Context     | Decisions, design notes, or gotchas the next agent needs to understand |
| Next Steps      | Ordered list of what to do next, specific enough to act on immediately |

## Task Tracking (`tasks/ARC-nnn/TODO.md` / `tasks/ARC-nnn/DONE.md`)

Primary location: `.agents/tasks/ARC-nnn/` (TODO.md, DONE.md, STATUS.md, plans/).

Fallback location when `.agents` is unavailable: `AGENTS_ROOT/guidelines/projects/boxrunner/tasks/ARC-nnn/`.

New ticket: `mkdir -p .agents/tasks/ARC-nnn/plans` + create TODO.md + STATUS.md + row in `.agents/tasks/README.md`.

- Record plan in `TODO.md` before executing. Check off (`- [x]`) as completed.
- Every task ends with `- [ ] Verify with the developer that the task is complete`.
- All done → create `tasks/ARC-nnn/DONE.md` with timestamp + summary + checklist.
- After the related PR merges, archive with `git mv .agents/tasks/ARC-nnn .agents/archive/ARC-nnn` (create `.agents/archive/` if missing).
- Ticket archival and any `.agents`-side Git operations are handled manually by the developer; the agent should not assume it needs to commit `.agents` changes.
- Reorder subtasks with Python only — never string-replace.

## Ruby on Rails Conventions

- **All application commands run inside the Docker container.** Never against system Ruby/Node.
- Start stack: `docker compose up` (starts `app`, `solr`, `zookeeper`).
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


# Agent Rules — dor-depot

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
- `[when-committing]` Base commit suggestions on tracked/staged files only (`git status`, `git diff --staged`).
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
- If task metadata is clearly stale or inconsistent (for example ticket index summary/status drift, or `STATUS.md` not matching `TODO.md`), fix it proactively and report the change. Do not ask for permission first when the correction is clear and non-destructive.

## Session State (`tasks/DOR-nnn/STATUS.md`)

At session start: (1) identify ticket from branch name (e.g. `DOR-142/ingest-validation` → `DOR-142`), (2) read `tasks/DOR-nnn/STATUS.md` in full, (3) cross-check open subtasks against `TODO.md` — `TODO.md` is authoritative.

During session: update `STATUS.md` when a subtask completes, a plan changes, or a key decision is made.

End of session: update Last Updated, Recent Activity, Next Steps. Commit `STATUS.md` in final commit.

| Section         | Contents                                                               |
|-----------------|------------------------------------------------------------------------|
| Last Updated    | ISO date + one-line session summary                                    |
| Current Branch  | Active git branch name; brief note on other local branches if relevant |
| Open Tasks      | Copy of unchecked subtasks from `TODO.md`; key files for each task     |
| Open Plans      | Table of files in `tasks/DOR-nnn/plans/` with purpose and status       |
| Recent Activity | Bullet list of meaningful changes made in the most recent session      |
| Key Context     | Decisions, design notes, or gotchas the next agent needs to understand |
| Next Steps      | Ordered list of what to do next, specific enough to act on immediately |

## Task Tracking (`tasks/DOR-nnn/TODO.md` / `tasks/DOR-nnn/DONE.md`)

Files live at `guidelines/projects/dor-depot/tasks/DOR-nnn/` (TODO.md, DONE.md, STATUS.md, plans/).

New ticket: `mkdir -p guidelines/projects/dor-depot/tasks/DOR-nnn/plans` + create TODO.md + STATUS.md + row in `tasks/README.md`.

- Record plan in `TODO.md` before executing. Check off (`- [x]`) as completed.
- Every task ends with `- [ ] Verify with the developer that the task is complete`.
- All done → create `tasks/DOR-nnn/DONE.md` with timestamp + summary + checklist.
- Complete ticket (after PR merges): `git mv guidelines/projects/dor-depot/tasks/DOR-nnn guidelines/projects/dor-depot/archive/DOR-nnn`
- Reorder subtasks with Python only — never string-replace.

## Java / Gradle Conventions

- Build: `./gradlew` wrapper only. Never system `gradle`. Requires **JDK 26**.
- Style: Spotless (Palantir/AOSP). Before committing: `./gradlew spotlessApply | cat` then `./gradlew spotlessCheck | cat`
- Tests: `./gradlew test`. Requires Docker running (PostgreSQL + RabbitMQ via Testcontainers).
- Run app: `./gradlew bootRun` (Docker must be running first via `compose.yaml`).
- **Spring Modulith**: cross-module communication via published application events only — never call another module's internal service classes directly. Modules: `preservation`, `console`, `config`.
  - `UuidTypeHandler` in `config`; `JsonTypeHandler<T>` in `preservation`.
- **AMQP**: `@Externalized` events use routing constants from `AmqpIntegrationConfiguration`. Exchanges: `intake.exchange`, `integrity.exchange`, `publication.exchange`. `IngestValidation*` events are internal-only (not externalized).
- Spring profiles: `dev` = HTTP Basic; `demo` = OIDC. Activate: `--spring.profiles.active=dev`.
- Reset local env: delete `data/ocfl/root` contents, `docker compose down`, `docker volume rm dor-depot_postgres-data`.


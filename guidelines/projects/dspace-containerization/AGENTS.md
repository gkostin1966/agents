# Agent Rules — dspace-containerization (project-specific additions)

> **Base guidelines apply first**: `guidelines/base/AGENTS.md`
> Sections in this file **override** any base section with the same `## Heading`.
> Additional sections here are appended after the base.
>
> **Task tracking files for this project live at:**
> `guidelines/projects/dspace-containerization/`

## Task Tracking (TODO.md / DONE.md)

Task tracking for this project lives in the agents framework repository at
`guidelines/projects/dspace-containerization/TODO.md` and `DONE.md`.

- **TODO.md** is the active task list. Organise work as **tasks** with **subtasks**:
  ```
  ## Task Title
  Short description of the overall goal.

  - [ ] Subtask one
  - [ ] Subtask two
  - [ ] Verify the current state of the project achieves the task goal
  - [ ] Verify with the developer that the task is complete
  ```
- **Check off subtasks** (`- [x]`) as they are completed. Keep the task in `TODO.md` until
  **all** subtasks — including the final developer-verification step — are checked off.
- **Every task must end with a developer-verification subtask** as its final item:
  `- [ ] Verify with the developer that the task is complete`
  When this subtask is reached, ask: *"Are there any additional subtasks needed before this
  task is complete?"* Add any new subtasks before the verification step.
- **Only when all subtasks are done**, move the whole task to `DONE.md`:
  1. **Remove** the task block from `TODO.md`.
  2. **Prepend** it to `DONE.md` (insert after the `# DONE` heading, before any existing
     entries) with a timestamp and brief summary. This keeps `DONE.md` in **reverse
     chronological order** (newest entry first).
- Example entry in `DONE.md`:
  ```
  ## 2026-04-21T14:32:00 — Added AGENTS.md paging rule
  Added the first rule to AGENTS.md requiring all CLI commands to suppress
  interactive paging so output is captured without waiting for user input.
  ```
- Never leave a completed task in `TODO.md`; always archive it to `DONE.md`.

## Docker / Make Conventions

- **Primary workflow** is through `make` targets. Run `make help` (or read the `Makefile`)
  to see available targets. Key targets: `make build`, `make up`, `make up-all`, `make down`,
  `make clean`, `make rebuild`, `make test`.
- **Multiple Dockerfiles** exist for different services: `frontend.dockerfile`,
  `backend.dockerfile`, `db.dockerfile`, `solr.dockerfile`. Always build through
  `docker compose build` or `make build` — never invoke `docker build` directly.
- **Smoke tests**: `bash tests/smoke.sh` verifies basic service availability. Always run
  after a build before committing.
- **Environment variables**: Copy `.env.example` to `.env` and fill in required values
  before running `make up`. Never commit `.env`.
- **CI**: GitHub Actions workflows live in `.github/workflows/`. Verify CI passes before
  declaring work complete.


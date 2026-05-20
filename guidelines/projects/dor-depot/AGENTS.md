# Agent Rules — dor-depot (project-specific additions)

> **Base guidelines apply first**: `guidelines/base/AGENTS.md`
> Sections in this file **override** any base section with the same `## Heading`.
> Additional sections here are appended after the base.
>
> **Task tracking files for this project live at:**
> `guidelines/projects/dor-depot/tasks/`

## Session State (`tasks/DOR-nnn/STATUS.md`)

Each Jira ticket has its own `tasks/DOR-nnn/STATUS.md` — the **living state snapshot** for
that ticket's branch. It records the current branch, open subtasks, open plans, recent
activity, and key context so any agent can pick up exactly where the previous one left off.

**At the start of every session** (after reading `AGENTS.md`):
1. Identify the active ticket from the branch name (e.g., `DOR-142/ingest-validation` → `DOR-142`).
2. Read `tasks/DOR-nnn/STATUS.md` in full before touching any other file.
3. Cross-check the open subtasks listed there against `tasks/DOR-nnn/TODO.md` — if they
   differ, update `STATUS.md` to match `TODO.md` (the task file is authoritative).

**During a session**, update `tasks/DOR-nnn/STATUS.md` whenever:
- A subtask is completed (update Open Tasks).
- A plan file is created or significantly changed (update Open Plans).
- A significant decision or discovery is made that the next agent needs to know.

**At the end of every session** (before yielding back to the developer):
- Update the **Last Updated** timestamp and write a one-line summary.
- Update **Recent Activity** with a bullet list of key changes.
- Update **Next Steps** so the next agent knows exactly where to resume.
- Commit `tasks/DOR-nnn/STATUS.md` as part of the final commit of the session.

**What to keep in each section:**

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

Each Jira ticket has its own `tasks/DOR-nnn/` directory (stored in this agents repository
at `guidelines/projects/dor-depot/tasks/DOR-nnn/`) containing:
- `TODO.md` — the active subtask checklist for that ticket
- `DONE.md` — created when all subtasks complete; moved to `archive/` with the ticket
- `STATUS.md` — living session snapshot (see § Session State above)
- `plans/` — design docs, summaries, and plan files for this ticket

**Starting a new ticket:**
```
mkdir -p guidelines/projects/dor-depot/tasks/DOR-nnn/plans
```
Create `tasks/DOR-nnn/TODO.md` and `tasks/DOR-nnn/STATUS.md`, then add a row to
`tasks/README.md`. Work entirely within `tasks/DOR-nnn/` — never touch another ticket's
directory.

**`TODO.md` format** — organise work as **tasks** with **subtasks**:
```
## Task Title
Short description of the overall goal.

- [ ] Subtask one
- [ ] Subtask two
- [ ] Verify the current state of the project achieves the task goal
- [ ] Verify with the developer that the task is complete
```

- **Before executing any multi-step plan**, record it in `TODO.md` first. Do not begin
  execution until the plan is recorded so work is always resumable.
- **Check off subtasks** (`- [x]`) as they are completed.
- **Every task must end with a developer-verification subtask** as its final item.
  When reached, ask: *"Are there any additional subtasks needed before this task is complete?"*
- **Only when all subtasks are done**, create `tasks/DOR-nnn/DONE.md` with a timestamp,
  summary, and the completed checklist.

**Completing a ticket** (after PR merges, on the `agents` branch):
```shell
git mv guidelines/projects/dor-depot/tasks/DOR-nnn guidelines/projects/dor-depot/archive/DOR-nnn
```
Update `tasks/README.md` to mark the ticket archived. Commit on `agents`.

### Reordering Subtasks in `tasks/DOR-nnn/TODO.md`

**Never use string-search-and-replace to reorder tasks.** Use Python instead:

```python
import re
content = open('tasks/DOR-nnn/TODO.md').read()
parts = re.split(r'(?=^## )', content, flags=re.MULTILINE)
header, tasks = parts[0], parts[1:]
tasks.append(tasks.pop(2))  # example: move index 2 to end
open('tasks/DOR-nnn/TODO.md', 'w').write(header + ''.join(tasks))
```

## Java / Gradle Conventions

- **Build tool**: Gradle with the Gradle wrapper (`./gradlew`). Never install or invoke a
  system `gradle` directly. Requires **JDK 26** (e.g.,
  [Eclipse Temurin 26](https://adoptium.net/temurin/releases?version=26&mode=filter&os=any&arch=any)).
- **Imports**: Always use import statements for annotations and types in method parameters
  and signatures, rather than fully qualified class names. Prefer imports throughout the code.
- **Code style**: Spotless is configured with Palantir Java Format (AOSP style). Before
  committing Java files, run:
  ```shell
  ./gradlew spotlessApply | cat
  ./gradlew spotlessCheck | cat
  ```
  Spotless uses `ratchetFrom 'origin/main'`, so only files changed since `origin/main` are
  checked.
- **Tests**: Use JUnit 5 with `./gradlew test`. Tests require Docker to be running
  (PostgreSQL and RabbitMQ are managed via Testcontainers).
- **Running the app**: `./gradlew bootRun` starts the application. Docker must be running
  first (PostgreSQL + RabbitMQ via `compose.yaml`).
- **Module boundaries**: This project uses Spring Modulith. Each top-level package under
  `edu.umich.lib.dor.depot` is a module. Cross-module communication must go through
  published application events — never call internal service classes from another module
  directly. Modules: `preservation` (core domain), `console` (web UI + admin REST), `config`
  (infrastructure support — no Spring beans).
  - **MyBatis type handlers**: `UuidTypeHandler` lives in `config`; `JsonTypeHandler<T>`
    lives in `preservation`. Both packages are scanned via `mybatis.type-handlers-package`.
- **AMQP event externalization**: Domain events published to RabbitMQ use `@Externalized`
  with a routing constant from `AmqpIntegrationConfiguration`. Three exchanges:
  `intake.exchange`, `integrity.exchange`, `publication.exchange`.
  **Not all events are externalized**: `IngestValidation*` events are internal-only.
  All `IntegrityCheck*` events are externalized to `integrity.exchange`.
- **Resource types**: The `ResourceType` enum defines `Curio`, `Glam`, and `Fileset`.
  The `dor-info.txt` label specifies type via `Resource-Type:`.
- **Spring profiles**: `dev` — HTTP Basic auth; `demo` — OIDC via U-M Weblogin.
  Activate with `--spring.profiles.active=dev`.
- **Application properties** in `src/main/resources/application.properties`:
  - `dor.inbox.path`, `dor.workingStorage.path`, `dor.ocfl.path`
- **Debugging the OCFL repository**: `compose.yaml` includes an `ocfl-webui` service at
  `http://localhost:8283` that mounts `data/ocfl/root` read-only.
- **Resetting the local environment**:
  1. Delete the contents of `data/ocfl/root` (keep the directory itself).
  2. `docker compose down`
  3. `docker volume rm dor-depot_postgres-data`


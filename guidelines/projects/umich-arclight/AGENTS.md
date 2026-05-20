# Agent Rules — umich-arclight (project-specific additions)

> **Base guidelines apply first**: `guidelines/base/AGENTS.md`
> Sections in this file **override** any base section with the same `## Heading`.
> Additional sections here are appended after the base.
>
> **Task tracking files for this project live at:**
> `guidelines/projects/umich-arclight/tasks/`

## Session State (`tasks/ARC-nnn/STATUS.md`)

Each Jira ticket has its own `tasks/ARC-nnn/STATUS.md` — the **living state snapshot** for
that ticket's branch. It records the current branch, open subtasks, open plans, recent
activity, and key context so any agent can pick up exactly where the previous one left off.

**At the start of every session** (after reading `AGENTS.md`):
1. Identify the active ticket from the branch name (e.g., `ARC-123/my-feature` → `ARC-123`).
2. Read `tasks/ARC-nnn/STATUS.md` in full before touching any other file.
3. Cross-check the open subtasks listed there against `tasks/ARC-nnn/TODO.md` — if they
   differ, update `STATUS.md` to match `TODO.md` (the task file is authoritative).

**During a session**, update `tasks/ARC-nnn/STATUS.md` whenever:
- A subtask is completed (update Open Tasks).
- A plan file is created or significantly changed (update Open Plans).
- A significant decision or discovery is made that the next agent needs to know.

**At the end of every session** (before yielding back to the developer):
- Update the **Last Updated** timestamp and write a one-line summary.
- Update **Recent Activity** with a bullet list of key changes.
- Update **Next Steps** so the next agent knows exactly where to resume.
- Commit `tasks/ARC-nnn/STATUS.md` as part of the final commit of the session.

**What to keep in each section:**

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

Each Jira ticket has its own `tasks/ARC-nnn/` directory (stored in this agents repository
at `guidelines/projects/umich-arclight/tasks/ARC-nnn/`) containing:
- `TODO.md` — the active subtask checklist for that ticket
- `DONE.md` — created when all subtasks complete; moved to `archive/` with the ticket
- `STATUS.md` — living session snapshot (see § Session State above)
- `plans/` — design docs, summaries, and plan files for this ticket

**Starting a new ticket:**
```
mkdir -p guidelines/projects/umich-arclight/tasks/ARC-nnn/plans
```
Create `tasks/ARC-nnn/TODO.md` and `tasks/ARC-nnn/STATUS.md`, then add a row to
`tasks/README.md`. Work entirely within `tasks/ARC-nnn/`.

**`TODO.md` format:**
```
## Task Title
Short description of the overall goal.

- [ ] Subtask one
- [ ] Subtask two
- [ ] Verify the current state of the project achieves the task goal
- [ ] Verify with the developer that the task is complete
```

- **Before executing any multi-step plan**, record it in `TODO.md` first.
- **Check off subtasks** (`- [x]`) as they are completed.
- **Every task must end with a developer-verification subtask** as its final item.
- **Only when all subtasks are done**, create `tasks/ARC-nnn/DONE.md` with a timestamp,
  summary, and the completed checklist.

**Completing a ticket** (after PR merges, on the `agents` branch):
```shell
git mv guidelines/projects/umich-arclight/tasks/ARC-nnn guidelines/projects/umich-arclight/archive/ARC-nnn
```
Update `tasks/README.md` to mark the ticket archived. Commit on `agents`.

### Reordering Subtasks in `tasks/ARC-nnn/TODO.md`

**Never use string-search-and-replace to reorder tasks.** Use Python instead:

```python
import re
content = open('tasks/ARC-nnn/TODO.md').read()
parts = re.split(r'(?=^## )', content, flags=re.MULTILINE)
header, tasks = parts[0], parts[1:]
tasks.append(tasks.pop(2))  # example: move index 2 to end
open('tasks/ARC-nnn/TODO.md', 'w').write(header + ''.join(tasks))
```

## Ruby on Rails Conventions

- **Runtime environment**: All application commands must be run inside the Docker container
  — never against a system Ruby or Node installation. Use
  `docker-compose exec -- app <command>` as the prefix.
- **Code style**: RuboCop is configured with Standard, rubocop-rails, rubocop-rspec, and
  rubocop-rake. Before committing Ruby files, run:
  ```shell
  docker-compose exec -- app bundle exec rubocop | cat
  ```
  Auto-fix safe offences with:
  ```shell
  docker-compose exec -- app bundle exec rubocop -a | cat
  ```
- **JavaScript linting**: Uses Yarn with the `lint` script:
  ```shell
  docker-compose exec -- app yarn lint | cat
  ```
- **Tests**: Two suites — MiniTest (`rake test`) and RSpec (`rspec`). Run inside the
  container:
  ```shell
  docker-compose exec -- app bundle exec rake test | cat
  docker-compose exec -- app bundle exec rspec | cat
  ```
  The default CI rake task runs both: `bundle exec rake` (equivalent to
  `rake rubocop test spec`).
- **Running the app**: Bring up all services with `docker-compose up -d`, then:
  ```shell
  docker-compose exec -- app bundle exec rails s -b 0.0.0.0
  ```
  Available at `http://localhost:3000/`
- **Background jobs**: Resque workers process indexing jobs. Monitor via Resque-Web at
  `http://localhost:8080/overview`. Start workers with `docker-compose restart resque`.
- **Configuration files**:
  - `config/repositories.yml` — repository slugs, names, and metadata per institution
  - `config/blacklight.yml` — Solr connection URL per environment
  - `config/database.yml` — PostgreSQL connection config (overridden by `DATABASE_URL`)
  - `lib/dul_arclight.rb` — declares `DulArclight.finding_aid_data` (default `/data`,
    overridden by `FINDING_AID_DATA`)


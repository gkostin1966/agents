# Agent Rules — dor-react-app (project-specific additions)

> **Base guidelines apply first**: `guidelines/base/AGENTS.md`
> Sections in this file **override** any base section with the same `## Heading`.
> Additional sections here are appended after the base.
>
> **Task tracking files for this project live at:**
> `guidelines/projects/dor-react-app/tasks/`

## Environment Check (New Session)

At the start of every new session, run the following command to confirm whether you are
inside a devcontainer and identify its type:

```shell
printenv | grep -i "container\|remote\|codespace" | cat
```

**What to look for:**

| Signal                                 | Meaning                                                            |
|----------------------------------------|--------------------------------------------------------------------|
| `DEVCONTAINER_CONFIG_PATH` is set      | You are inside a devcontainer (most definitive indicator)          |
| Value contains `/.jbdevcontainer`      | It is a **JetBrains** remote dev devcontainer                      |
| `REMOTE_CONTAINERS=true`               | It is a **VS Code** devcontainer (this variable absent here)       |
| `CODESPACES=true`                      | It is a **GitHub Codespace** (this variable absent here)           |
| `REMOTE_DEV_*` variables present       | JetBrains remote dev server is managing the session                |
| Working directory under `/workspaces/` | Standard devcontainer mount point                                  |
| Hostname is a 12-char hex hash         | Typical Docker container ID — corroborates containerised execution |

**In this repository** the environment is a JetBrains devcontainer:
`DEVCONTAINER_CONFIG_PATH=/.jbdevcontainer/config/JetBrains/host-config.json`

This matters because ports, file paths, and the dev server URL (`http://localhost:5173`)
are all relative to the container — the JetBrains IDE handles port-forwarding to the host
automatically.

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
at `guidelines/projects/dor-react-app/tasks/DOR-nnn/`) containing:
- `TODO.md` — the active subtask checklist for that ticket
- `DONE.md` — created when all subtasks complete; moved to `archive/` with the ticket
- `STATUS.md` — living session snapshot (see § Session State above)
- `plans/` — design docs, summaries, and plan files for this ticket

**Starting a new ticket:**
```
mkdir -p guidelines/projects/dor-react-app/tasks/DOR-nnn/plans
```
Create `tasks/DOR-nnn/TODO.md` and `tasks/DOR-nnn/STATUS.md`, then add a row to
`tasks/README.md`. Work entirely within `tasks/DOR-nnn/`.

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
- **After recording a plan**, ask the developer to review it before starting any work.
  Wait for explicit approval before proceeding with implementation.
- **Check off subtasks** (`- [x]`) as they are completed.
- **Every task must end with a developer-verification subtask** as its final item.
- **Only when all subtasks are done**, create `tasks/DOR-nnn/DONE.md` with a timestamp,
  summary, and the completed checklist.

**Completing a ticket** (after PR merges, on the `agents` branch):
```shell
git mv guidelines/projects/dor-react-app/tasks/DOR-nnn guidelines/projects/dor-react-app/archive/DOR-nnn
```
Update `tasks/README.md` to mark the ticket archived. Commit on `agents`.

### Reordering Subtasks in `tasks/DOR-nnn/TODO.md`

**Never use string-search-and-replace to reorder tasks.** Use Python instead:

```python
import re
content = open('tasks/DOR-nnn/TODO.md').read()
parts = re.split(r'(?=^## )', content, flags=re.MULTILINE)
header, tasks = parts[0], parts[1:]
tasks.append(tasks.pop(2))
open('tasks/DOR-nnn/TODO.md', 'w').write(header + ''.join(tasks))
```

## Test-Driven Development (TDD)

- **Write tests before implementation**: When developing new features or fixing bugs, write
  tests first that define the expected behavior, then implement the code to make the tests pass.
- **Task order**: Structure work as **Test → Implementation → Documentation**:
  1. **Test**: Write unit tests, integration tests, or test cases that specify what the code
     should do.
  2. **Implementation**: Write the actual code to make the tests pass.
  3. **Documentation**: Update README, inline comments, and other docs to reflect the
     implementation.
- **Test frameworks**:
  - JavaScript/React: Vitest, React Testing Library
  - Python: pytest, unittest

## React / Node.js / Vite Conventions

- **Package manager**: Use `npm` for all dependency management. Never use `yarn` or `pnpm`
  unless the developer explicitly requests it.
- **Imports**: Always use ES6 import syntax. Use named imports for utilities and components;
  default imports for React components that are the primary export of a file.
- **Code style**: ESLint is configured for React. Before committing, run:
  ```shell
  npm run lint | cat
  ```
- **Development server**: `npm run dev` starts the Vite development server (typically on
  `http://localhost:5173`).
- **Building**: `npm run build` creates a production build in the `dist/` directory.
- **Project structure**:
  - `src/` — all source code
  - `src/apps/` — application modules/pages (e.g., `OsDorDcApp`, `RsDorDcApp`)
  - `src/apps/*/components/` — React components specific to an app
  - `src/apps/*/services/` — API clients and data services
  - `src/apps/*/utils/` — utility functions and constants
  - `src/assets/` — static assets
  - `public/` — public static files served at root
- **Key dependencies**:
  - `react` + `react-dom` — React framework
  - `react-router-dom` — client-side routing
  - `antd` — Ant Design UI component library
  - `@appbaseio/reactivesearch` — Elasticsearch/OpenSearch search UI components
  - `dompurify` — HTML sanitization
  - `vite` — build tool and dev server


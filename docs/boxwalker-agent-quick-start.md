# Boxwalker Agent Quick Start

Use this guide when everything is already configured and you want to start a new boxwalker task for an agent.

## Assumptions

- `mounted-projects/boxwalker` already exists and points to the real boxwalker repo.
- `mounted-projects/boxwalker/.agents` already points to `guidelines/projects/boxwalker`.
- Docker, git, and the framework CLI are already working on your machine.
- You can edit `.agents/tasks/` from your current environment (host or devcontainer).

## What to prepare before starting an agent

1. Pick a ticket id (`BW-###`) and create a matching branch in boxwalker.
2. Create task tracking files under `.agents/tasks/BW-###/`.
3. Update the boxwalker task index (`.agents/tasks/README.md`).
4. Start a fresh agent chat in the mounted project.
5. Use `.agents` files as startup/task sources.

## Storybook Example: Starting `BW-101`

### 1) Create the implementation branch in boxwalker

```shell
cd /Users/gkostin/GitHub/gkostin1966/agents/mounted-projects/boxwalker
git checkout -b BW-101/add-facet-chip
```

### 2) Create task files from the mounted project

```shell
cd /Users/gkostin/GitHub/gkostin1966/agents/mounted-projects/boxwalker
mkdir -p .agents/tasks/BW-101/plans
touch .agents/tasks/BW-101/TODO.md
touch .agents/tasks/BW-101/STATUS.md
```

Suggested `TODO.md` starter:

```markdown
# BW-101 TODO

- [ ] Confirm current behavior in `app/` and add notes
- [ ] Implement facet-chip behavior changes in target files
- [ ] Add/update tests
- [ ] Run test and lint commands in Docker
- [ ] Verify with the developer that the task is complete
```

Suggested `STATUS.md` starter:

```markdown
# BW-101 STATUS

## Last Updated
- 2026-06-09 — Created task shell and branch

## Current Branch
- `BW-101/add-facet-chip`

## Open Tasks
- Track unchecked items from `TODO.md`

## Open Plans
- None yet

## Recent Activity
- Created task folder and tracking files

## Key Context
- Add key decisions and constraints here

## Next Steps
1. Capture baseline behavior
2. Draft implementation plan
3. Hand off to agent
```

### 3) Add the ticket to the task index

Edit `.agents/tasks/README.md` and add a row for the active ticket.

Example row:

```markdown
| `BW-101` | `BW-101/add-facet-chip` | In Progress | Add facet chip behavior |
```

### 4) Verify `.agents` startup files are present

```shell
cd /Users/gkostin/GitHub/gkostin1966/agents/mounted-projects/boxwalker
ls -la .agents/AGENT_PROMPT.md .agents/AGENTS.md .agents/tasks/README.md | cat
```

Optional (host-side) refresh before session:

```shell
cd /Users/gkostin/GitHub/gkostin1966/agents
PYTHONPATH=src python3 -m agents_framework.cli bootstrap boxwalker
```

Use this optional step only when the framework repo is available in your current environment.

### 5) Start a fresh agent chat in boxwalker

- Open a new agent chat with working directory set to `mounted-projects/boxwalker`.
- Start with: `Read .agents/AGENT_PROMPT.md and follow the instructions there.`
- Confirm the agent identifies `BW-101` from branch name and reads:
  - `.agents/tasks/README.md`
  - `.agents/tasks/BW-101/STATUS.md`
  - `.agents/tasks/BW-101/TODO.md`
- Only if `.agents` is unavailable, provide `AGENTS_ROOT` fallback path.

At this point, prerequisites are complete and the agent can start implementation work.

## Quick command block

```shell
cd /Users/gkostin/GitHub/gkostin1966/agents/mounted-projects/boxwalker
git checkout -b BW-101/add-facet-chip

mkdir -p .agents/tasks/BW-101/plans
touch .agents/tasks/BW-101/TODO.md
touch .agents/tasks/BW-101/STATUS.md
ls -la .agents/AGENT_PROMPT.md .agents/AGENTS.md .agents/tasks/README.md | cat
```


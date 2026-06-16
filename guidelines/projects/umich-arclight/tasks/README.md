# Task Index

Reference for the `tasks/` directory layout. For the full agent workflow and
rules, see `.agents/AGENTS.md`.

---

## Active Tasks

| Ticket       | Branch | Summary |
|--------------|--------|---------|
| *(none yet)* |        |         |

---

## Archived Tasks

| Ticket       | Archive path | Summary |
|--------------|--------------|---------|
| *(none yet)* |              |         |

---

## Directory Convention

Each Jira ticket gets a subdirectory under `tasks/`:

```
tasks/
  ARC-nnn/
    TODO.md      <- subtask checklist (follow AGENTS.md section Task Tracking format)
    STATUS.md    <- living session snapshot (follow AGENTS.md section Session State format)
    DONE.md      <- created when all subtasks complete; retained when archived
    plans/
      *.md       <- design docs, summaries, and plan files for this ticket
```

**Starting a new ticket:**
1. `mkdir -p guidelines/projects/umich-arclight/tasks/ARC-nnn/plans`
2. Create `TODO.md` and `STATUS.md` under that directory.
3. Add a row to the Active Tasks table above.
4. Work entirely within `tasks/ARC-nnn/` for all agent state and plans.

**Completing a ticket (after PR merges):**
1. `git mv guidelines/projects/umich-arclight/tasks/ARC-nnn guidelines/projects/umich-arclight/archive/ARC-nnn`
2. Move the row from Active to Archived in this file.
3. Commit in the `agents` repository.


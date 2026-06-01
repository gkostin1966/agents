# Agent Rules — dor-react-app (project-specific additions)

> Base: `guidelines/base/AGENTS.md`. Matching `## Heading` here replaces base section.
> Task tracking: `guidelines/projects/dor-react-app/tasks/`

## Environment Check (New Session)

Run at session start to confirm devcontainer type:
```shell
printenv | grep -i "container\|remote\|codespace" | cat
```
Key signal: `DEVCONTAINER_CONFIG_PATH=/.jbdevcontainer/...` = JetBrains devcontainer. Ports/paths are container-relative; IDE handles port-forwarding automatically.

## Session State (`tasks/DOR-nnn/STATUS.md`)

At session start: (1) identify ticket from branch name, (2) read `tasks/DOR-nnn/STATUS.md` in full, (3) cross-check against `TODO.md` — `TODO.md` is authoritative.

During session: update `STATUS.md` when a subtask completes, plan changes, or key decision made.

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

Files live at `guidelines/projects/dor-react-app/tasks/DOR-nnn/` (TODO.md, DONE.md, STATUS.md, plans/).

New ticket: `mkdir -p guidelines/projects/dor-react-app/tasks/DOR-nnn/plans` + create TODO.md + STATUS.md + row in `tasks/README.md`.

- **Record plan in `TODO.md` first, then ask developer to review. Wait for explicit approval before implementing.**
- Check off (`- [x]`) as completed. Every task ends with `- [ ] Verify with the developer that the task is complete`.
- All done → create `tasks/DOR-nnn/DONE.md` with timestamp + summary + checklist.
- Complete ticket: `git mv guidelines/projects/dor-react-app/tasks/DOR-nnn guidelines/projects/dor-react-app/archive/DOR-nnn`
- Reorder subtasks with Python only — never string-replace.

## Test-Driven Development (TDD)

Write tests before implementation. Order: Test → Implementation → Documentation. Frameworks: Vitest + React Testing Library (JS), pytest/unittest (Python).

## React / Node.js / Vite Conventions

- **Package manager**: `npm` only. Never `yarn` or `pnpm`.
- **Lint before commit**: `npm run lint | cat`
- Key deps (don't swap without reason): `antd` (UI), `@appbaseio/reactivesearch` (search), `dompurify` (sanitization), `react-router-dom` (routing).


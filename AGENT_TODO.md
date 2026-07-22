# AGENT_TODO

## Resuming a session

1. Check working state: `git branch --show-current | cat` and `git --no-pager status | cat`
2. Read [`AGENTS.md`](AGENTS.md) (meta-rules and conventions for this project).
3. Read the top entry of [`AGENT_DONE.md`](AGENT_DONE.md) for recent completion context.
4. Read this file — the first unchecked subtask in the first task below is where to pick up.

---

<!-- Add new tasks below this line. Keep the most urgent task first. -->

## Migrate dspace-angular agent files from project root to .agents/

- [x] Copy `AGENTS.md`, `TODO.md`, `DONE.md`, `PLAN_DSPACE_ANGULAR_PASSWORD_LOGIN.md`, `PULL_REQUEST.md` from project root to `.agents/` with framework naming (`AGENT_TODO.md`, `AGENT_DONE.md`, etc.)
- [x] Update `.agents/AGENTS.md` to be project-specific (add Project Context, Task Files, Branch Naming, Test Commands sections)
- [x] `git rm` the five files from `mlibrary/dspace-angular` and commit removal (commit `2a3fd7b18`)
- [ ] Verify with the developer that migration is complete and project root is clean




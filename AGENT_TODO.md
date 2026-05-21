# AGENT_TODO

## Resuming a session

1. Check working state: `git branch --show-current | cat` and `git --no-pager status | cat`
2. Read [`AGENTS.md`](AGENTS.md) (meta-rules and conventions for this project).
3. Read the top entry of [`AGENT_DONE.md`](AGENT_DONE.md) for recent completion context.
4. Read this file — the first unchecked subtask in the first task below is where to pick up.

---

<!-- Add new tasks below this line. Keep the most urgent task first. -->

## Sync agent files and refresh PR summary
Bring project agent artifacts in line with the current framework state and update `pr-summary.md` accordingly.

- [x] Review changed agent/framework files and align wording/state with current behavior
- [x] Update `pr-summary.md` to reflect the latest cumulative branch changes
- [x] Verify the current state of the project achieves the task goal
- [ ] Verify with the developer that the task is complete

## Fix stale config schema reference in quiz answer A24
Ensure onboarding quiz content matches the current `config/projects.json` schema (no `guidelines_path` field).

- [x] Update `AGENT_QUIZ_ANSWERS.md` A24 to remove `guidelines_path`
- [x] Update `AGENT_QUIZ.md` Q24 wording if needed to emphasize current schema
- [x] Verify the current state of the project achieves the task goal
- [ ] Verify with the developer that the task is complete

## Prevent `all + --output` overwrite in generate commands
Ensure `agentsfw guidelines|prompt generate all --output ...` cannot silently overwrite one file repeatedly.

- [x] Update CLI generation logic to reject `--output` when project target is `all`
- [x] Add tests covering rejected `all + --output` behavior
- [x] Fix `validate_projects` filtering so `project_names=[]` validates none (not all)
- [x] Add tests covering empty-list validation behavior
- [x] Verify tests pass
- [x] Verify the current state of the project achieves the task goal
- [ ] Verify with the developer that the task is complete

## Make init-mounts source path follow relative_path
Ensure mount source lookup remains correct when `relative_path` differs from project `name`.

- [x] Update `init_mounts` source-path derivation to use `relative_path`
- [x] Ensure destination parent directories are created for nested `relative_path` values
- [x] Add tests for differing/nested `relative_path` mount behavior
- [x] Verify tests pass
- [x] Verify the current state of the project achieves the task goal
- [ ] Verify with the developer that the task is complete

# AGENT_TODO

## Resuming a session

1. Check working state: `git branch --show-current | cat` and `git --no-pager status | cat`
2. Read [`AGENTS.md`](AGENTS.md) (meta-rules and conventions for this project).
3. Read the top entry of [`AGENT_DONE.md`](AGENT_DONE.md) for recent completion context.
4. Read this file — the first unchecked subtask in the first task below is where to pick up.

---

<!-- Add new tasks below this line. Keep the most urgent task first. -->

## Make merged provenance paths repo-relative
Avoid absolute-path leakage and non-determinism in merged guideline/prompt headers.

- [x] Use stable repo-relative project path text in merged provenance headers
- [x] Add tests that fail if absolute project paths appear in merged output
- [x] Verify tests pass
- [x] Verify the current state of the project achieves the task goal
- [ ] Verify with the developer that the task is complete

## Make CLI repo-root resolution install-safe
Ensure `agentsfw` does not rely on `__file__` paths that break in non-editable installs.

- [x] Resolve repo root from `--repo-root` or current working directory
- [x] Add clear error when resolved root does not contain `config/projects.json`
- [x] Add tests for repo-root resolution behavior
- [x] Verify tests pass
- [x] Verify the current state of the project achieves the task goal
- [ ] Verify with the developer that the task is complete

## Improve smoke script shell portability
Switch `scripts/smoke_run.sh` to a portable shebang and align docs.

- [x] Change `scripts/smoke_run.sh` shebang from zsh to bash
- [x] Update `scripts/README.md` invocation example to bash
- [x] Run `bash scripts/smoke_run.sh` to verify behavior
- [x] Verify the current state of the project achieves the task goal
- [ ] Verify with the developer that the task is complete

## Review reviewer changes and respond to comments
Review code-reviewer edits for correctness, apply any needed follow-up fixes, and prepare responses to all reviewer comments.

- [x] Review each reviewer-provided change for correctness and project-rule compliance
- [x] Address any remaining reviewer comments with code or documentation updates
- [x] Prepare concise response notes for each reviewer comment (resolved/updated/explanation)
- [x] Verify the current state of the project achieves the task goal
- [ ] Verify with the developer that the task is complete

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

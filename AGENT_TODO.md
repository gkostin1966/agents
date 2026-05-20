# AGENT_TODO

## Resuming a session

1. Check working state: `git branch --show-current | cat` and `git --no-pager status | cat`
2. Read [`AGENTS.md`](AGENTS.md) (meta-rules and conventions for this project).
3. Read the top entry of [`AGENT_DONE.md`](AGENT_DONE.md) for recent completion context.
4. Read this file — the first unchecked subtask in the first task below is where to pick up.

---

<!-- Add new tasks below this line. Keep the most urgent task first. -->

## Refactor and feature additions from review
Ten-item improvement plan: DRY refactor, dead code removal, new CLI features, housekeeping, quiz content, and expanded tests.

- [x] Extract shared `merge.py` module; update `guidelines.py` and `prompts.py` to use it
- [x] Remove dead `guidelines_path` field from `config/projects.json`; remove unused `marker_path` property from `ProjectConfig`
- [x] Add `all` support to `guidelines generate` and `prompt generate` CLI commands
- [x] Add `.idea*/` and `pr-summary.md` to `.gitignore`
- [x] Add `agentsfw validate` subcommand for per-project agent-file completeness check
- [x] Fix `dotpy/` vs `/tmp/` commit instruction contradiction between `guidelines/base/AGENTS.md` and `AGENTS.md`
- [x] Create `dspace-containerization` `AGENT_QUIZ.md` and `AGENT_QUIZ_ANSWERS.md`
- [x] Update root `AGENT_QUIZ.md` and `AGENT_QUIZ_ANSWERS.md` to cover `prompts.py` and `prompt generate`
- [x] Extend test coverage: `init_mounts`, `run_task` dry-run, `load_config`, file-write paths for generate functions
- [x] Verify the current state of the project achieves the task goal
- [ ] Verify with the developer that the task is complete

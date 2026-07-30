# AGENT_TODO

## Resuming a session

1. Check working state: `git branch --show-current | cat` and `git --no-pager status | cat`
2. Read [`AGENTS.md`](AGENTS.md) (meta-rules and conventions for this project).
3. Read the top entry of [`AGENT_DONE.md`](AGENT_DONE.md) for recent completion context.
4. Read this file — the first unchecked subtask in the first task below is where to pick up.

---

<!-- Add new tasks below this line. Keep the most urgent task first. -->

## 2026-07-30T00:00:00Z — Add and mount project: deepblue

- [x] Add `deepblue` entry in `config/projects.json` with required fields
- [x] Initialize the mounted symlink under `mounted-projects/`
- [x] Seed project guideline defaults for `guidelines/projects/deepblue/`
- [x] Validate with framework tests: `PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py'`
- [ ] Verify with the developer that the task is complete



# AGENT_TODO

## Resuming a session

1. Check working state: `git branch --show-current | cat` and `git --no-pager status | cat`
2. Read [`AGENTS.md`](AGENTS.md) (meta-rules and conventions for this project).
3. Read the top entry of [`AGENT_DONE.md`](AGENT_DONE.md) for recent completion context.
4. Read this file — the first unchecked subtask in the first task below is where to pick up.

---

<!-- Add new tasks below this line. Keep the most urgent task first. -->

## Add AGENT_PROMPT base+project merge support
Create a mergeable base prompt, refactor project prompts to shared heading blocks, add CLI support, tests, and documentation.

- [x] Create `guidelines/base/AGENT_PROMPT.md` with explicit heading blocks suitable for deterministic merges
- [x] Refactor each `guidelines/projects/<name>/AGENT_PROMPT.md` to use the same heading-block structure and project-specific overrides
- [x] Implement framework merge logic and CLI support for generating merged prompt files
- [x] Add/update tests covering prompt merge behavior and CLI integration
- [x] Update documentation to describe prompt architecture and generation workflow
- [x] Verify the current state of the project achieves the task goal
- [ ] Verify with the developer that the task is complete

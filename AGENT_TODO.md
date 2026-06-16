# AGENT_TODO

## Resuming a session

1. Check working state: `git branch --show-current | cat` and `git --no-pager status | cat`
2. Read [`AGENTS.md`](AGENTS.md) (meta-rules and conventions for this project).
3. Read the top entry of [`AGENT_DONE.md`](AGENT_DONE.md) for recent completion context.
4. Read this file — the first unchecked subtask in the first task below is where to pick up.

---

<!-- Add new tasks below this line. Keep the most urgent task first. -->


## Task: Audit dspace-containerization agent files outside vs inside .agents/

Loose files found at project root: `AGENTS.md`, `TODO.md`, `DONE.md`

- [ ] Read and compare `mounted-projects/dspace-containerization/AGENTS.md` against `mounted-projects/dspace-containerization/.agents/AGENTS.md` — note any content differences, additions, or staleness
- [ ] Read and compare `mounted-projects/dspace-containerization/TODO.md` against equivalent task tracking files under `mounted-projects/dspace-containerization/.agents/` (if any exist)
- [ ] Read and compare `mounted-projects/dspace-containerization/DONE.md` against equivalent archive files under `mounted-projects/dspace-containerization/.agents/` (if any exist)
- [ ] Produce a written comparison summary: which files are stale copies, which have unique content, and whether any data would be lost by removing the root-level files
- [ ] Recommend action: remove root-level files, migrate unique content to `.agents/`, or keep as-is with rationale
- [ ] Verify with the developer that the task is complete



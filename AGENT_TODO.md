# AGENT_TODO

## Resuming a session

1. Check working state: `git branch --show-current | cat` and `git --no-pager status | cat`
2. Read [`AGENTS.md`](AGENTS.md) (meta-rules and conventions for this project).
3. Read the top entry of [`AGENT_DONE.md`](AGENT_DONE.md) for recent completion context.
4. Read this file — the first unchecked subtask in the first task below is where to pick up.

---

<!-- Add new tasks below this line. Keep the most urgent task first. -->

## Task: Audit dor-react-app agent files outside vs inside .agents/

Loose files found at project root: `AGENTS.md`, `AGENT_PROMPT.md`, `AGENT_QUIZ.md`, `AGENT_QUIZ_ANSWERS.md`, `tasks/`

- [x] Read and compare `mounted-projects/dor-react-app/AGENTS.md` against `mounted-projects/dor-react-app/.agents/AGENTS.md` — note any content differences, additions, or staleness
- [x] Read and compare `mounted-projects/dor-react-app/AGENT_PROMPT.md` against `mounted-projects/dor-react-app/.agents/AGENT_PROMPT.md`
- [x] Read and compare `mounted-projects/dor-react-app/AGENT_QUIZ.md` against `mounted-projects/dor-react-app/.agents/AGENT_QUIZ.md`
- [x] Read and compare `mounted-projects/dor-react-app/AGENT_QUIZ_ANSWERS.md` against `mounted-projects/dor-react-app/.agents/AGENT_QUIZ_ANSWERS.md`
- [x] Inspect `mounted-projects/dor-react-app/tasks/` — determine if task files have equivalents under `.agents/tasks/` or are orphaned
- [x] Produce a written comparison summary: which files are stale copies, which have unique content, and whether any data would be lost by removing the root-level files
- [x] Recommend action: remove root-level files, migrate unique content to `.agents/`, or keep as-is with rationale
- [ ] Verify with the developer that the task is complete

## Task: dor-react-app — fix Email Drafts convention in .agents/AGENTS.md

Root uses RTF files under `emails/`. Framework currently says `.md` files under `communications/`. Root convention is project-specific and correct for this project.

- [x] Replace the `## Email Drafts for Third Parties` section in `guidelines/projects/dor-react-app/AGENTS.md` with the RTF/`emails/` convention from the root `AGENTS.md`
- [x] Regenerate `PYTHONPATH=src python3 -m agents_framework.cli guidelines generate dor-react-app`
- [ ] Verify with the developer that the task is complete

## Task: dor-react-app — add Markdown table tools to .agents/AGENTS.md

Root version references `dotpy/format_table.py`, `dotpy/calc_widths.py`, `dotpy/check_tables.py`. The `.agents/` version has only the generic padding rule. Project-specific tooling must be captured.

- [x] Expand the `## Markdown Tables` section in `guidelines/projects/dor-react-app/AGENTS.md` with the three `dotpy/` table commands and their usage
- [x] Regenerate `PYTHONPATH=src python3 -m agents_framework.cli guidelines generate dor-react-app`
- [ ] Verify with the developer that the task is complete

## Task: dor-react-app — elevate dotpy/commit.py to primary multiline commit path in .agents/AGENTS.md

Root version makes `dotpy/commit.py` the required multiline commit method (write to `dotpy/commit_msg.txt`, run `python3 dotpy/commit.py | cat`). The `.agents/` version treats it as an optional fallback. The project-specific convention must be primary.

- [x] Update `## Git Commits` in `guidelines/projects/dor-react-app/AGENTS.md` to make `dotpy/commit.py` the required multiline path rather than a fallback
- [x] Regenerate `PYTHONPATH=src python3 -m agents_framework.cli guidelines generate dor-react-app`
- [ ] Verify with the developer that the task is complete

## Task: dor-react-app — expand React conventions and Task Tracking in .agents/AGENTS.md

Root version has full project structure tree, all key dependencies, and explicit "ask developer to review plan before implementing" requirement. `.agents/` version is condensed.

- [x] Expand `## React / Node.js / Vite Conventions` in `guidelines/projects/dor-react-app/AGENTS.md` with full project structure and key deps
- [x] Strengthen `## Task Tracking` to include explicit developer-approval-before-implementing requirement (already present — confirmed)
- [x] Regenerate `PYTHONPATH=src python3 -m agents_framework.cli guidelines generate dor-react-app`
- [ ] Verify with the developer that the task is complete

## Task: dor-react-app — populate .agents/tasks/README.md with archive index

The `.agents/tasks/README.md` is currently empty. The root `tasks/README.md` has the full task index including three archived tickets (DOR-158, DOR-159, DOR-160) and directory conventions.

- [x] Copy content from root `tasks/README.md` into `guidelines/projects/dor-react-app/tasks/README.md`, updating any path references to be framework-relative
- [ ] Verify with the developer that the task is complete

## Task: dor-react-app — remove root-level agent files from mounted project (developer action)

Once all preceding tasks are complete, root-level agent files in `dor-react-app` are redundant. These files must be removed by the developer directly in the project repository.

- [ ] Confirm all preceding dor-react-app migration tasks are developer-verified complete
- [ ] Developer removes `AGENT_QUIZ.md` from `dor-react-app/` root (safe immediately — identical to `.agents/`)
- [ ] Developer removes `AGENT_QUIZ_ANSWERS.md` from `dor-react-app/` root (safe immediately — identical to `.agents/`)
- [ ] Developer removes `AGENTS.md` from `dor-react-app/` root (safe after migration tasks complete)
- [ ] Developer removes `AGENT_PROMPT.md` from `dor-react-app/` root (safe after migration tasks complete)
- [ ] Developer removes `tasks/README.md` from `dor-react-app/` root and the empty `tasks/` directory if no ticket dirs remain (safe after tasks/README.md populated in `.agents/`)
- [ ] Verify with the developer that the task is complete

## Task: Audit dspace-containerization agent files outside vs inside .agents/

Loose files found at project root: `AGENTS.md`, `TODO.md`, `DONE.md`

- [ ] Read and compare `mounted-projects/dspace-containerization/AGENTS.md` against `mounted-projects/dspace-containerization/.agents/AGENTS.md` — note any content differences, additions, or staleness
- [ ] Read and compare `mounted-projects/dspace-containerization/TODO.md` against equivalent task tracking files under `mounted-projects/dspace-containerization/.agents/` (if any exist)
- [ ] Read and compare `mounted-projects/dspace-containerization/DONE.md` against equivalent archive files under `mounted-projects/dspace-containerization/.agents/` (if any exist)
- [ ] Produce a written comparison summary: which files are stale copies, which have unique content, and whether any data would be lost by removing the root-level files
- [ ] Recommend action: remove root-level files, migrate unique content to `.agents/`, or keep as-is with rationale
- [ ] Verify with the developer that the task is complete

## Task: Audit umich-arclight agent files outside vs inside .agents/

Loose files found at project root: `AGENTS.md`, `AGENT_PROMPT.md`, `AGENT_QUIZ.md`, `AGENT_QUIZ_ANSWERS.md`, `tasks/`

- [ ] Read and compare `mounted-projects/umich-arclight/AGENTS.md` against `mounted-projects/umich-arclight/.agents/AGENTS.md` — note any content differences, additions, or staleness
- [ ] Read and compare `mounted-projects/umich-arclight/AGENT_PROMPT.md` against `mounted-projects/umich-arclight/.agents/AGENT_PROMPT.md`
- [ ] Read and compare `mounted-projects/umich-arclight/AGENT_QUIZ.md` against `mounted-projects/umich-arclight/.agents/AGENT_QUIZ.md`
- [ ] Read and compare `mounted-projects/umich-arclight/AGENT_QUIZ_ANSWERS.md` against `mounted-projects/umich-arclight/.agents/AGENT_QUIZ_ANSWERS.md`
- [ ] Inspect `mounted-projects/umich-arclight/tasks/` — determine if task files have equivalents under `.agents/tasks/` or are orphaned
- [ ] Produce a written comparison summary: which files are stale copies, which have unique content, and whether any data would be lost by removing the root-level files
- [ ] Recommend action: remove root-level files, migrate unique content to `.agents/`, or keep as-is with rationale
- [ ] Verify with the developer that the task is complete


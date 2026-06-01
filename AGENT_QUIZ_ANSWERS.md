# AGENT_QUIZ_ANSWERS — agents (meta-framework)

> **Do not read this file until you have answered all questions in `AGENT_QUIZ.md`
> and the developer has told you to compare.**

---

## Section 1 — Framework Scope and Layout

**A1.** The repository has two primary roles:
1. Guidelines repository for agent rules, prompts, quizzes, and task tracking metadata.
2. Operational framework (`agentsfw`) for mounts, scans, task execution, and merged-file generation.

**A2.** Package path: `src/agents_framework/`. Package name: `agents_framework`.

**A3.** Modules in `src/agents_framework/`:
- `__init__.py` — package metadata/version.
- `cli.py` — parser wiring and command dispatch.
- `config.py` — `FrameworkConfig`/`ProjectConfig` dataclasses and config loading.
- `framework.py` — mount path resolution, mount init, scan, and task execution.
- `guidelines.py` — guidelines merge and merged-file generation.
- `merge.py` — shared heading-based Markdown merge primitives.
- `prompts.py` — prompt merge and merged-file generation.
- `validate.py` — required/recommended per-project file validation.

**A4.** Catalog file: `config/projects.json`. Per project entry (current schema):
- `name`
- `stack`
- `relative_path`
- `commands`

**A5.** `mounted-projects/` contains symlink mounts to external source repos.
It is read-only from this framework perspective: do not create, edit, or delete mounted project source files there.

---

## Section 2 — Config and Registration Rules

**A6.** A first-time mounted project must be added to `config/projects.json` so the framework can discover and operate on it.

**A7.** `relative_path` is the project path under both source root and mount root.
It is used by mount/path logic in `src/agents_framework/framework.py` (`resolve_project_path`, `init_mounts`).

**A8.** Update `STACK_MARKERS` in `src/agents_framework/framework.py`.

**A9.** `name` is the logical identifier used for selection/output in CLI commands; `relative_path` is the filesystem path segment used to locate and mount the repository.

---

## Section 3 — Merge Architecture

**A10.** Guidelines merge files:
- Base source: `guidelines/base/AGENTS.md`
- Project source: `guidelines/projects/<name>/AGENTS.md`
- Generated output: `guidelines/projects/<name>/AGENTS_MERGED.md`

**A11.** Prompt merge files:
- Base source: `guidelines/base/AGENT_PROMPT.md`
- Project source: `guidelines/projects/<name>/AGENT_PROMPT.md`
- Generated output: `guidelines/projects/<name>/AGENT_PROMPT_MERGED.md`

**A12.** If the same `## Heading` appears in both files, the project section replaces the base section entirely.

**A13.** Shared module: `src/agents_framework/merge.py`.
Public functions: `split_sections`, `merge_sections`, `read_and_merge`.

**A14.** `src/agents_framework/guidelines.py` and `src/agents_framework/prompts.py`.

---

## Section 4 — CLI Behavior

**A15.** `agents_framework.cli:main`.

**A16.** `agentsfw scan` reports mounted/missing status for each configured project plus stack marker detection.

**A17.** `agentsfw validate` checks `guidelines/projects/<name>/` files.
- Required: `AGENTS.md`, `AGENT_PROMPT.md`
- Recommended: `AGENT_QUIZ.md`, `AGENT_QUIZ_ANSWERS.md`

**A18.** `--output` is rejected when target is `all` (for both guidelines and prompt generate), to prevent repeatedly overwriting one output file.

**A19.**
```shell
PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py'
```

---

## Section 5 — Task Tracking and Workflow

**A20.** Framework task tracking lives at repo root in `AGENT_TODO.md` (active) and `AGENT_DONE.md` (archive).
The required final subtask is: `- [ ] Verify with the developer that the task is complete`.

**A21.** Before a multi-step plan is executed, record it in `AGENT_TODO.md` first.

**A22.** Once all subtasks are complete: remove the task block from `AGENT_TODO.md`, then prepend it (timestamped summary) to `AGENT_DONE.md` immediately after the heading.

**A23.** `AGENT_QUIZ_ANSWERS.md` may be read only after answering all quiz questions and receiving explicit developer permission to compare.

---

## Section 6 — Operational Checks

**A24.** Startup orientation commands:
```shell
git branch --show-current | cat
git --no-pager status | cat
git --no-pager log --oneline -5 | cat
```

**A25.** Stop and notify the developer before proceeding.

**A26.** Regenerate merged outputs across configured projects, e.g.:
```shell
PYTHONPATH=src python3 -m agents_framework.cli guidelines generate all
```

**A27.** `agentsfw prompt generate all` merges base+project prompts for every configured project and writes each result to `guidelines/projects/<name>/AGENT_PROMPT_MERGED.md`.

**A28.** Verify the exact latest commit message with:
```shell
git --no-pager log --oneline -1 | cat
```


# AGENT_QUIZ — agents (meta-framework)

> Answer every question below by looking up the answer in the actual project files.
> Do **not** read `AGENT_QUIZ_ANSWERS.md` until you have answered all questions and the
> developer has told you to compare.
>
> This quiz is scoped to the `agents` framework itself.
> Treat mounted projects as abstract configured entries (not stack-specific trivia targets).
>
> Write your answers inline under each question before moving on.

---

## Section 1 — Framework Scope and Layout

**Q1.** What are the two primary roles of this repository, as described in root `AGENTS.md`?

- (1) Guidelines/prompt/task-tracking store for mounted projects.
- (2) `agentsfw` Python CLI framework.

**Q2.** What is the Python package path for the framework code, and what is the package name?

- Path: `src/agents_framework/`
- Package: `agents_framework`

**Q3.** List every module in `src/agents_framework/` and give a one-line purpose for each.

- `__init__.py` - package metadata (`__version__`) and package docstring.
- `cli.py` - argparse command wiring and command dispatch for `agentsfw`.
- `config.py` - config dataclasses plus load/add helpers for `config/projects.json`.
- `framework.py` - project scanning, marker detection, mount setup, and task execution.
- `guidelines.py` - base/project guidelines merge and merged file generation.
- `merge.py` - shared section split/merge engine used by guidelines/prompt merging.
- `prompts.py` - base/project prompt merge and merged prompt generation.
- `sync_base.py` - diff/sync utilities to propagate base sections into project files.
- `validate.py` - per-project required/recommended agent-file completeness checks.

**Q4.** What file defines the mounted-project catalog, and which fields are required per project entry in the current schema?

- Catalog file: `config/projects.json`
- Required per-project fields (from `load_config`): `name`, `stack`, `relative_path`, `source_path`

**Q5.** In this framework, what does `mounted-projects/` represent, and what are the read/write restrictions for that directory?

- It is the configured mounts root for linked project working trees (default `projects_root`).
- Restriction: treat `mounted-projects/` as read-only in this meta-framework; never create/edit/delete files there manually.

---

## Section 2 — Config and Registration Rules

**Q6.** When a project is mounted for the first time, what must be updated first so the framework recognizes it?

- Add/register the project in `config/projects.json` first.

**Q7.** In `config/projects.json`, what is the purpose of `relative_path`, and where in the code is it used to resolve mount paths?

- `relative_path` is the path under `projects_root` (usually `mounted-projects/`) where the mount/symlink lives.
- Used in `framework.py` via `resolve_project_path()` (`repo_root / config.projects_root / project.relative_path`) and in `init_mounts()` for destination `dst`.

**Q8.** If a project uses a stack value not currently listed in `STACK_MARKERS`, what code file and symbol must be updated?

- Update `src/agents_framework/framework.py`, symbol `STACK_MARKERS`.

**Q9.** What is the difference between `name` and `relative_path` in practical CLI behavior?

- `name` is the project identifier used by CLI selectors/arguments (for example `--project`, `--projects`, and config lookup keys).
- `relative_path` is filesystem placement for the mount under `projects_root`; it controls where links are created/resolved, independent of the CLI key.

---

## Section 3 — Merge Architecture

**Q10.** What are the source and generated files for guidelines merging?

- Sources: `guidelines/base/AGENTS.md` + `guidelines/projects/<name>/AGENTS.md`
- Generated output: `guidelines/projects/<name>/AGENTS_MERGED.md` (or a custom `--output` path)

**Q11.** What are the source and generated files for prompt merging?

- Sources: `guidelines/base/AGENT_PROMPT.md` + `guidelines/projects/<name>/AGENT_PROMPT.md`
- Generated output: `guidelines/projects/<name>/AGENT_PROMPT_MERGED.md` (or a custom `--output` path)

**Q12.** What happens when a `## Heading` exists in both base and project files during merge?

- The project section replaces the base section entirely for that heading.

**Q13.** Which shared module implements section splitting/merging, and what are its three public functions?

- Module: `src/agents_framework/merge.py`
- Public functions: `split_sections`, `merge_sections`, `read_and_merge`

**Q14.** Which two modules import that shared merge helper?

- `src/agents_framework/guidelines.py`
- `src/agents_framework/prompts.py`

---

## Section 4 — CLI Behavior

**Q15.** What is the console entry point (`module:function`) for `agentsfw`?

- `agents_framework.cli:main`

**Q16.** What does `agentsfw scan` report at a high level?

- For each configured project: mount state (`mounted`/`missing`), configured stack, and detected stack markers.

**Q17.** What does `agentsfw validate` check, and which files are required vs recommended?

- It validates per-project agent-file completeness under `guidelines/projects/<name>/`.
- Required: `AGENTS.md`, `AGENT_PROMPT.md`
- Recommended: `AGENT_QUIZ.md`, `AGENT_QUIZ_ANSWERS.md`

**Q18.** What safety rule applies to `guidelines generate all --output ...` and `prompt generate all --output ...`?

- Safety rule: `--output` cannot be used when `project` is `all`; command returns an error.

**Q19.** What command should be used to run the full test suite without installing the package?

- `PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py'`

---

## Section 5 — Task Tracking and Workflow

**Q20.** Where does task tracking for framework work live, and what is the required final subtask in every task?

- Task tracking lives in `AGENT_TODO.md` (active) and `AGENT_DONE.md` (archived).
- Required final subtask: `- [ ] Verify with the developer that the task is complete`

**Q21.** Before executing any multi-step plan, what must be done in `AGENT_TODO.md`?

- Add the task to `AGENT_TODO.md` before executing the plan.

**Q22.** When a framework task is fully complete, how is it archived from `AGENT_TODO.md` to `AGENT_DONE.md`?

- Only when all subtasks are done: remove it from `AGENT_TODO.md` and prepend it to `AGENT_DONE.md` with a timestamp.

**Q23.** What is the rule about reading `AGENT_QUIZ_ANSWERS.md`?

- Do not read it until all quiz answers are written and the developer explicitly says to compare/self-grade.

---

## Section 6 — Operational Checks

**Q24.** What startup git-orientation commands must be run at the beginning of a new session?

- `git branch --show-current | cat`
- `git --no-pager status | cat`
- `git --no-pager log --oneline -5 | cat`

**Q25.** If branch or working state is unexpected during startup checks, what should the agent do next?

- Stop and tell the developer.

**Q26.** You update `guidelines/base/AGENTS.md`. What is the next framework step to validate merged outputs across all configured projects?

- Regenerate all guidelines merges:
  `PYTHONPATH=src python3 -m agents_framework.cli guidelines generate all`

**Q27.** What does `agentsfw prompt generate all` do, and where are outputs written?

- It generates merged prompt files for every configured project.
- Outputs are written to each project's `guidelines/projects/<name>/AGENT_PROMPT_MERGED.md` (unless printing/custom output is used).

**Q28.** Looking at current git history, what is the most recent commit message?

- `chore: commit modified deepblue guideline files`



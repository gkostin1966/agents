# Agent Rules — agents (meta-framework project)

> **Read this file at the start of every new agent session, before taking any action.**
> These rules apply to all AI coding agents (GitHub Copilot, Claude, Cursor, etc.) working
> in the `agents` project.
>
> **Important:** This project is a *meta-framework*. It manages agent guidelines and task
> tracking for multiple mounted sub-projects. The rules here govern work on the framework
> itself — not on the mounted projects.

## Project Purpose and Scope

The `agents` project serves two roles:

1. **Guidelines repository** — canonical home for all agent rules (`AGENTS.md`), onboarding
   quizzes, session prompts, and task tracking for the six mounted projects.
2. **Operational framework** — Python CLI (`agentsfw`) for mounting projects, scanning
   status, running tasks, and generating merged agent guidelines and startup prompts.

**Every file in this repository falls into one of these categories:**

| Category              | Paths                                          | Purpose                                     |
|-----------------------|------------------------------------------------|---------------------------------------------|
| Meta-agent files      | `AGENTS.md`, `AGENT_*.md` (project root)       | Rules for working on the agents project     |
| Base guidelines       | `guidelines/base/AGENTS.md`                    | Shared rules for all mounted projects       |
| Base startup prompt   | `guidelines/base/AGENT_PROMPT.md`              | Shared startup blocks for all projects      |
| Project guidelines    | `guidelines/projects/<name>/AGENTS.md`         | Per-project overrides and additions         |
| Project startup prompt| `guidelines/projects/<name>/AGENT_PROMPT.md`   | Per-project startup prompt overrides        |
| Project task tracking | `guidelines/projects/<name>/AGENT_TODO.md` etc | Task/session state for each mounted project |
| Framework source      | `src/agents_framework/`                        | Python CLI and merge engine                 |
| Tests                 | `tests/`                                       | Framework unit tests                        |
| Config                | `config/projects.json`                         | Project catalog and metadata                |
| Mount root            | `mounted-projects/`                            | Symlinks to source repos (gitignored)       |

## File Access

- **Stay within this project directory.** Do not read, write, or search files in the
  mounted sub-projects unless the developer **explicitly** requests it.
  - When a developer requests access to a mounted project file, read **only that specific
    file** — do not browse or list the surrounding directory.
  - Never speculatively explore paths outside this repository root.

- **The mounted-projects directory is read-only.** Never create, edit, or delete files
  under `mounted-projects/`. Changes to mounted project source code must be done in the
  upstream repositories directly.

- **Never read `AGENT_QUIZ_ANSWERS.md` before completing the quiz.** When taking the
  `AGENT_QUIZ.md` onboarding quiz, do not open or read `AGENT_QUIZ_ANSWERS.md` until you
  have written out answers to all questions **and** the developer has explicitly told you
  to compare.

## Guidelines and Prompt Architecture — Know Before You Edit

### Three files, three roles

| File                                           | Role                           | Edit when…                                            |
|------------------------------------------------|--------------------------------|-------------------------------------------------------|
| `guidelines/base/AGENTS.md`                    | Shared rules for all projects  | A rule should apply to every mounted project          |
| `guidelines/projects/<name>/AGENTS.md`         | Per-project overrides          | A rule is specific to one project or overrides base   |
| `AGENTS.md` (this file)                        | Meta-rules for this repo       | Rules for working on the framework itself change      |

### Merge semantics

When `agentsfw guidelines generate <project>` is run, the base and project files are merged:
- A section in the project file whose `## Heading` **matches** a base heading **replaces**
  the base section entirely.
- Sections present only in the project file are **appended** after the merged base.
- Sections present only in the base are **kept as-is**.

The merged output is written to
`guidelines/projects/<name>/AGENTS_MERGED.md` (gitignored — never commit it).

### Prompt files and merge semantics

Startup prompts use the same section-merge model with explicit heading blocks:

- Base file: `guidelines/base/AGENT_PROMPT.md`
- Project file: `guidelines/projects/<name>/AGENT_PROMPT.md`
- Generated file: `guidelines/projects/<name>/AGENT_PROMPT_MERGED.md` (gitignored)

When `agentsfw prompt generate <project>` is run:
- A section in the project prompt whose `## Heading` matches a base heading replaces the
  base section entirely.
- Sections present only in the project prompt are appended after merged base sections.
- Sections present only in the base prompt are kept as-is.

### Which file to edit

- Rules about CLI paging, zsh quoting, commit message patterns, Markdown formatting → **base**
- Rules about a specific stack (Rails, Spring, Tanka/k8s), task tracking style, or cluster
  topology → **project-specific**
- Rules about how the framework itself is structured, tested, or extended → **this file**

## Task Tracking (AGENT_TODO.md / AGENT_DONE.md)

Task tracking for work on this project lives at the project root:
`AGENT_TODO.md` (active) and `AGENT_DONE.md` (archive).

- **AGENT_TODO.md** is the active task list. Organise work as **tasks** with **subtasks**:
  ```
  ## Task Title
  Short description of the overall goal.

  - [ ] Subtask one
  - [ ] Subtask two
  - [ ] Verify the current state of the project achieves the task goal
  - [ ] Verify with the developer that the task is complete
  ```
- **Before executing any multi-step plan**, add it to `AGENT_TODO.md` first. Do not begin
  execution until the plan is recorded.
- **Check off subtasks** (`- [x]`) as they are completed. Keep the task in `AGENT_TODO.md`
  until **all** subtasks — including the final developer-verification step — are done.
- **Every task must end with a developer-verification subtask** as its final item:
  `- [ ] Verify with the developer that the task is complete`
- **Only when all subtasks are done**, move the whole task to `AGENT_DONE.md`:
  1. **Remove** the task block from `AGENT_TODO.md`.
  2. **Prepend** it to `AGENT_DONE.md` (insert after the `# AGENT_DONE` heading) with a
     timestamp and brief summary. This keeps `AGENT_DONE.md` in **reverse chronological
     order** (newest entry first).
- Never leave a completed task in `AGENT_TODO.md`; always archive it to `AGENT_DONE.md`.

### Reordering Tasks in `AGENT_TODO.md`

**Never use string-search-and-replace to reorder tasks.** Always use Python:

```python
import re
content = open('AGENT_TODO.md').read()
parts = re.split(r'(?=^## )', content, flags=re.MULTILINE)
header, tasks = parts[0], parts[1:]
tasks.append(tasks.pop(2))  # example: move index 2 to end
open('AGENT_TODO.md', 'w').write(header + ''.join(tasks))
```

## Command-Line Tool Usage

- **Disable interactive paging**: When running commands that may invoke a pager, always
  suppress paging:
  - `git --no-pager <command>` for git commands
  - Append `| cat` to commands that might page output
  - Never rely on interactive input

- **Never pass multi-line code via `-c` flags.** zsh mangles multi-line quoted strings —
  unclosed inner quotes trigger `dquote>` heredoc mode, corrupting the terminal session.

  **The universal fix — write to a file, run the file:**

  1. Use `create_file` or `insert_edit_into_file` to write the code to a temp file.
  2. Run: `python3 /tmp/run.py | cat`

- **Never use shell heredocs (`<< 'MARKER'`).** Write Python files instead.

- **Always run with `PYTHONPATH=src`** when invoking framework code without installing it:
  ```shell
  PYTHONPATH=src python3 -m agents_framework.cli <subcommand>
  ```

## Python Framework Conventions

- **Package layout**: `src/agents_framework/` (src layout). All modules live here.
  - `cli.py` — CLI entry point and subcommand wiring
  - `config.py` — `FrameworkConfig` / `ProjectConfig` dataclasses; loads `config/projects.json`
  - `framework.py` — mount detection, `scan_projects`, `init_mounts`, `run_task`
  - `merge.py` — shared `split_sections`, `merge_sections`, `read_and_merge` used by guidelines and prompts
  - `guidelines.py` — `merge_guidelines`, `generate_merged_file`
  - `prompts.py` — `merge_prompts`, `generate_merged_prompt`
  - `validate.py` — `validate_projects`, `ProjectValidation`
- **Tests**: Plain `unittest` in `tests/`. Run with:
  ```shell
  PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py'
  ```
  **Always run tests after modifying framework code** before committing.
- **No external dependencies**: The framework uses only the Python standard library. Do not
  add third-party packages without explicit developer approval.
- **Adding a new module**: Add the file under `src/agents_framework/`, import it in `cli.py`
  as needed, and add a corresponding `tests/test_<module>.py`.
- **Adding a new CLI subcommand**: Add a `sub.add_parser(...)` block in `build_parser()` in
  `cli.py`, wire the `which` key in `main()`, and add tests.
- **Python version**: Targets Python 3.10+. Use built-in generics (`list[str]`,
  `dict[str, str]`) rather than `typing.List`/`typing.Dict`.

## Adding or Modifying Guidelines

### Editing base guidelines

1. Edit `guidelines/base/AGENTS.md`.
2. Regenerate all project merged files to check for layout issues:
   ```shell
   for p in deepblue-documents-kube dor-depot dor-react-app dspace-containerization findingaids-argocd umich-arclight; do
     PYTHONPATH=src python3 -m agents_framework.cli guidelines generate $p
   done
   ```
3. Review the generated `AGENTS_MERGED.md` for any project where the change is non-trivial.
4. Commit only the source files (`guidelines/base/AGENTS.md`). The merged files are
   gitignored and are produced on demand.

### Editing project-specific guidelines

1. Edit `guidelines/projects/<name>/AGENTS.md`.
2. Regenerate just that project's merged file:
   ```shell
   PYTHONPATH=src python3 -m agents_framework.cli guidelines generate <name>
   ```
3. Review `guidelines/projects/<name>/AGENTS_MERGED.md` to confirm the override is correct.
4. Commit only `guidelines/projects/<name>/AGENTS.md`.

### Editing base startup prompts

1. Edit `guidelines/base/AGENT_PROMPT.md` using explicit `## Heading` blocks.
2. Regenerate all project merged prompts:
   ```shell
   for p in deepblue-documents-kube dor-depot dor-react-app dspace-containerization findingaids-argocd umich-arclight; do
     PYTHONPATH=src python3 -m agents_framework.cli prompt generate $p
   done
   ```
3. Review relevant `AGENT_PROMPT_MERGED.md` output files.
4. Commit only source files (`guidelines/base/AGENT_PROMPT.md`). Merged files are gitignored.

### Editing project-specific startup prompts

1. Edit `guidelines/projects/<name>/AGENT_PROMPT.md` with the standard heading blocks.
2. Regenerate that project's merged prompt:
   ```shell
   PYTHONPATH=src python3 -m agents_framework.cli prompt generate <name>
   ```
3. Review `guidelines/projects/<name>/AGENT_PROMPT_MERGED.md`.
4. Commit only `guidelines/projects/<name>/AGENT_PROMPT.md`.

### Adding a new mounted project

1. Add an entry to `config/projects.json` with `name`, `stack`, `relative_path`,
   `guidelines_path`, and `commands`.
2. Create `guidelines/projects/<name>/AGENTS.md` with the project-specific sections.
3. Copy or create `AGENT_PROMPT.md`, `AGENT_QUIZ.md`, `AGENT_QUIZ_ANSWERS.md` as needed.
4. Create any task tracking files or directories (`AGENT_TODO.md`, `AGENT_DONE.md`, or
   `tasks/` depending on the project's tracking style).
5. Add a stack marker entry in `framework.py` under `STACK_MARKERS` if the stack is new.
6. Run `PYTHONPATH=src python3 -m agents_framework.cli guidelines generate <name>` and
   review the output.
7. Run `PYTHONPATH=src python3 -m agents_framework.cli scan` (after mounting) to confirm
   detection.

## Git Commits

- **Never amend existing commits.** Always create a new commit on top of HEAD.
- **Do not force-push** or rewrite history unless the developer explicitly instructs it.
- **Never push to `main`.** The developer handles all pushes.

### Writing commit messages — write to a file, not `-m`

**Never use `git commit -m "..."` for multi-line messages.** Use a temp file:

1. Write the commit message to `/tmp/commit-msg.txt`:
   ```
   subject line here

   Body paragraph here.
   ```
2. Run:
   ```shell
   git commit -F /tmp/commit-msg.txt | cat
   ```

Single-line subject-only commits are the **one exception** where `-m` is safe:
```shell
git commit -m "chore: single line message" | cat
```

## Pull Request Summaries

- **When the developer asks for a PR summary**, write it to `pr-summary.md` and open the
  file so they can select-all and copy. `pr-summary.md` is gitignored.
- Structure:
  1. **`## <Title>`** — one-line description.
  2. **`### Summary`** — 2–4 sentences.
  3. **`### Changes`** — one bold entry per changed file/dir with bullet sub-points.
  4. **`### Notes`** *(optional)* — follow-up items or known limitations.
- Delete `pr-summary.md` after use; do not commit it.

## Markdown Formatting

- **Format tables correctly**: Every column must be padded so all cells in that column are
  the same width. Mismatched widths cause IDE warnings.
  - Pad every shorter cell with trailing spaces.
  - Separator row dashes must match the widest cell width.
  - **Data rows define the required column width** — not the header.


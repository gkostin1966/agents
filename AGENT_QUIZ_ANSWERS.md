# AGENT_QUIZ_ANSWERS — agents (meta-framework)

> **Do not read this file until you have answered all questions in `AGENT_QUIZ.md`
> and the developer has told you to compare.**

---

## Section 1 — Project Structure

**A1.** The source package lives at `src/agents_framework/`. The Python package name is
`agents_framework`.

**A2.** Modules inside `src/agents_framework/`:

| Module           | Purpose                                                                   |
|------------------|---------------------------------------------------------------------------|
| `__init__.py`    | Package marker; exports `__version__ = "0.1.0"`                          |
| `cli.py`         | CLI entry point (`main()`); defines and dispatches all subcommands        |
| `config.py`      | `ProjectConfig` and `FrameworkConfig` dataclasses; `load_config()` parses `config/projects.json` |
| `framework.py`   | Mount detection (`STACK_MARKERS`), `scan_projects`, `init_mounts`, `run_task` |
| `guidelines.py`  | `merge_guidelines` (section-level merge); `generate_merged_file` (writes/prints merged AGENTS.md) |
| `merge.py`       | Additional package module in `src/agents_framework/`; include in the module inventory |
| `prompts.py`     | Additional package module in `src/agents_framework/`; include in the module inventory |
| `validate.py`    | Additional package module in `src/agents_framework/`; include in the module inventory |

**A3.** `config/projects.json`. The six project names are:
1. `deepblue-documents-kube`
2. `dor-depot`
3. `dor-react-app`
4. `dspace-containerization`
5. `findingaids-argocd`
6. `umich-arclight`

**A4.** Via symlinks — the `agentsfw init-mounts` subcommand (`framework.init_mounts`)
creates `os.symlink` entries under `mounted-projects/` pointing at source repos elsewhere
on disk. The `mounted-projects/` directory is gitignored and is not committed to the
repository by default.

**A5.** Task tracking for the `agents` project lives at the repository root:
`AGENT_TODO.md` (active) and `AGENT_DONE.md` (archive). These are flat files with no
per-ticket subdirectory structure. This differs from mounted projects like `dor-depot` and
`umich-arclight`, whose task tracking lives under
`guidelines/projects/<name>/tasks/<ticket-id>/`.

---

## Section 2 — Guidelines Architecture

**A6.** Path: `guidelines/base/AGENTS.md`. Current top-level `## ` sections:
1. `## File Access`
2. `## Command-Line Tool Usage`
3. `## Python Utility Scripts`
4. `## Git Commits`
5. `## Pull Request Summaries`
6. `## Email Drafts for Third Parties`
7. `## Markdown Formatting`

**A7.** The project section **replaces** the base section entirely. The merge logic in
`merge.py` normalises headings for comparison; if a project heading matches a base heading,
only the project's chunk is included in the merged output — the base chunk is discarded for
that heading.

**A8.** The base guidelines for `## Email Drafts for Third Parties` now specify
**Markdown** under `communications/`. `deepblue-documents-kube` is therefore not an
exception using Markdown while other projects use RTF; the old answer describing base RTF
is out of date.

**A9.**
- **Flat `AGENT_TODO.md` / `AGENT_DONE.md`** (project-level, no per-ticket dirs):
  `deepblue-documents-kube`, `findingaids-argocd`, `dspace-containerization`
- **Per-ticket `tasks/<ticket>/` directories**:
  `dor-depot` (DOR-nnn), `dor-react-app` (DOR-nnn), `umich-arclight` (ARC-nnn)

**A10.**
```shell
PYTHONPATH=src python3 -m agents_framework.cli guidelines generate dor-react-app
```
The merged file is written to
`guidelines/projects/dor-react-app/AGENTS_MERGED.md`.

---

## Section 3 — Framework Code

**A11.** The function `load_config(repo_root: Path)` in `src/agents_framework/config.py`
loads the catalog. It returns a `FrameworkConfig` (containing `projects_root: Path` and
`projects: tuple[ProjectConfig, ...]`), which is composed of `ProjectConfig` instances
(each with `name`, `stack`, `relative_path`, `commands`).

**A12.** `STACK_MARKERS` is a `dict[str, tuple[str, ...]]` in `framework.py` that maps
a stack name to the file/folder names used as presence indicators when scanning a mounted
project. For `rails-arclight` the markers are `("Gemfile", "docker-compose.yml")`.

**A13.**
```shell
PYTHONPATH=src python3 -m agents_framework.cli run <task> --projects dor-depot,umich-arclight
```

**A14.** The base `## Git Commits` section is **discarded** and the project's `## Git
Commits` section is used instead. The merge logic (`merge_guidelines` in `guidelines.py`)
looks up each base heading in the project index; if found, it substitutes the project chunk.

**A15.** The function is `generate_merged_file(repo_root, project_name, output_path, *,
print_only)` in `src/agents_framework/guidelines.py`. The default output path is
`guidelines/projects/<project_name>/AGENTS_MERGED.md`. That file is listed in `.gitignore`
as `guidelines/projects/**/AGENTS_MERGED.md` and is **never committed**.

---

## Section 4 — Testing

**A16.**
```shell
PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py'
```

**A17.** 7 tests across 2 classes:

`FrameworkTests` (`tests/test_framework.py`):
- `test_detect_markers_for_react_stack`
- `test_scan_projects_marks_missing_mounts`
- `test_resolve_project_path`

`GuidelinesMergeTests` (`tests/test_guidelines.py`):
- `test_base_sections_kept_when_no_override`
- `test_project_section_overrides_base`
- `test_section_order_base_first_then_project_only`
- `test_real_base_and_project_files_exist_and_merge`

**A18.** The test asserts that `"## File Access"` and `"## Kubernetes Cluster Topology"`
are both present in the merged output for `deepblue-documents-kube`.

---

## Section 5 — Guidelines Content

**A19.** The heredoc rule (`Never use shell heredocs`) was introduced in
`dor-react-app/AGENTS.md` — it was the only source project to document this failure mode
explicitly. It belongs in the base because the zsh heredoc corruption risk is universal to
all tool-driven terminal sessions, regardless of which project an agent is working on.

**A20.** The section heading is `## ConfigMap Key Encoding`. The two encoding tokens are:
- **`__P__`** — encodes a **dot** (`.`) in the DSpace property name
- **`__D__`** — encodes a **hyphen** (`-`) in the DSpace property name
(A single `_` is preserved literally — no encoding needed.)

**A21.** Spring Modulith requires that cross-module communication go through **published
application events** — never by calling internal service classes from another module
directly. The web UI lives in the `console` package
(`edu.umich.lib.dor.depot.console`).

**A22.** `findingaids-argocd` uses **three** separate Kubernetes clusters. Their kubectl
context names are:
- `findingaids-production` (namespaces: `production`, `preview`, `argocd`)
- `findingaids-staging` (namespaces: `staging`, `argocd`)
- `findingaids-workshop` (namespaces: `testing`, `admin`, `argocd`)

**A23.** The ticket prefix is `ARC-nnn`. A new ARC-050 ticket's files should be created
at `guidelines/projects/umich-arclight/tasks/ARC-050/`.

---

## Section 6 — Operational Knowledge

**A24.** To register a seventh project `new-project` with stack `ruby-rails`, you must
create or modify:

1. **`config/projects.json`** — add a new JSON entry with `name`, `stack`,
   `relative_path`, and `commands`.
2. **`guidelines/projects/new-project/AGENTS.md`** — project-specific guidelines.
3. **`guidelines/projects/new-project/AGENT_PROMPT.md`** — session startup prompt.
4. **`guidelines/projects/new-project/AGENT_QUIZ.md`** — onboarding quiz.
5. **`guidelines/projects/new-project/AGENT_QUIZ_ANSWERS.md`** — quiz answers.
6. **Task tracking files** — e.g. `AGENT_TODO.md` / `AGENT_DONE.md` (flat) or
   `tasks/` directory (per-ticket), depending on the project's chosen pattern.
7. **`src/agents_framework/framework.py`** — add `"ruby-rails": (...)` to `STACK_MARKERS`
   if the stack is new.

**A25.** No, it is not allowed without explicit developer approval. The rule is in
`guidelines/projects/deepblue-documents-kube/AGENTS.md` under the subsection
`### Destructive \`kubectl\` and \`tk apply\` commands` (within `## Kubernetes Cluster
Topology`): `tk apply <env>` is listed as a command that **requires explicit developer
approval before running**.

**A26.** From `guidelines/base/AGENTS.md` § `## File Access`: an agent may read
`AGENT_QUIZ_ANSWERS.md` only after having **written out answers to all questions** *and*
the **developer has explicitly told you to compare**. Both conditions must be met.

**A27.** After modifying `guidelines/base/AGENTS.md`, regenerate the merged files for all
six projects and review them for correctness:

```shell
for p in deepblue-documents-kube dor-depot dor-react-app dspace-containerization findingaids-argocd umich-arclight; do
  PYTHONPATH=src python3 -m agents_framework.cli guidelines generate $p
done
```

Then commit only `guidelines/base/AGENTS.md` (the merged files are gitignored).

**A28.** The entry point lives in `src/agents_framework/cli.py`, function `main()`. It is
registered as a console script in `pyproject.toml`:
```
agentsfw = "agents_framework.cli:main"
```

**A29.** The shared merge module is `src/agents_framework/merge.py`. Its three public
functions are:
- `split_sections(text)` — splits a Markdown document into `(header, [(key, chunk), ...])`.
- `merge_sections(base_text, project_text)` — returns `(base_header, project_header, merged_chunks)`.
- `read_and_merge(base_path, project_path)` — reads both files and calls `merge_sections`.

`guidelines.py` and `prompts.py` both import from `merge.py` via `from .merge import read_and_merge`.

**A30.** `agentsfw validate` checks every registered project's `guidelines/projects/<name>/`
directory against two lists:
- **Required**: `AGENTS.md`, `AGENT_PROMPT.md` — project fails validation if either is missing.
- **Recommended**: `AGENT_QUIZ.md`, `AGENT_QUIZ_ANSWERS.md` — warnings only; project still passes.

**A31.** `agentsfw prompt generate all` merges `guidelines/base/AGENT_PROMPT.md` with each
project's `guidelines/projects/<name>/AGENT_PROMPT.md` in turn and writes the result to
`guidelines/projects/<name>/AGENT_PROMPT_MERGED.md` (gitignored) for all six projects.

**A32.** Verify the exact wording with:
```shell
git --no-pager log --oneline -1 | cat
```


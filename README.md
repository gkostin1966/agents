# Agents Multi-Project Development Framework

This repository now provides a lightweight framework for coordinating development tasks across multiple mounted projects under one root.

## Project catalog

`config/projects.json` is the source of truth for configured mounted projects and
stack-specific commands.

- Each project is an abstract framework entry with `name`, `stack`, `relative_path`, and
  `commands`.
- If a project is mounted for the first time, add it to `config/projects.json` before
  running framework commands that target it.
- The currently configured project names are listed in that file.

## Directory layout

```text
agents/
  config/projects.json
  guidelines/
    base/
      AGENTS.md                 # Shared rules for all projects
      AGENT_PROMPT.md           # Shared startup prompt blocks for all projects
    projects/
      deepblue-documents-kube/
        AGENTS.md               # Project-specific overrides/additions
        AGENT_PROMPT.md         # Session startup prompt
        AGENT_QUIZ.md           # Onboarding quiz
        AGENT_QUIZ_ANSWERS.md   # Quiz answers
        AGENT_TODO.md           # Active task list (flat, no per-ticket dirs)
        AGENT_DONE.md           # Completed task archive
      dor-depot/
        AGENTS.md
        AGENT_PROMPT.md / AGENT_QUIZ.md / AGENT_QUIZ_ANSWERS.md
        tasks/                  # Per-ticket DOR-nnn/ task directories
      dor-react-app/
        AGENTS.md
        AGENT_PROMPT.md / AGENT_QUIZ.md / AGENT_QUIZ_ANSWERS.md
        tasks/
      dspace-containerization/
        AGENTS.md
        AGENT_PROMPT.md / AGENT_QUIZ.md / AGENT_QUIZ_ANSWERS.md
        TODO.md / DONE.md
      findingaids-argocd/
        AGENTS.md
        AGENT_PROMPT.md / AGENT_QUIZ.md / AGENT_QUIZ_ANSWERS.md
        AGENT_TODO.md / AGENT_DONE.md
      umich-arclight/
        AGENTS.md
        AGENT_PROMPT.md / AGENT_QUIZ.md / AGENT_QUIZ_ANSWERS.md
        tasks/
  mounted-projects/             # Symlinks to source repos are created here
  src/agents_framework/
    cli.py                      # CLI entry point
    config.py                   # Loads config/projects.json
    framework.py                # Mounting, scanning, task execution
    guidelines.py               # Base + project guidelines merge engine
    prompts.py                  # Base + project startup prompt merge engine
  tests/
  scripts/
    README.md                  # Utility scripts index and conventions
    smoke_run.sh               # Non-interactive smoke run
```

## Quick start

Create mounts (symlinks) from the source root:

```bash
PYTHONPATH=src python3 -m agents_framework.cli init-mounts --source-root /path/to/source-root
```

Scan status and marker detection:

```bash
PYTHONPATH=src python3 -m agents_framework.cli scan
```

Validate that all projects have required agent files:

```bash
PYTHONPATH=src python3 -m agents_framework.cli validate
```

Dry-run a task on one or more projects:

```bash
PYTHONPATH=src python3 -m agents_framework.cli run test --projects dor-react-app,dor-depot --dry-run
```

Run a configured task for all mounted projects:

```bash
PYTHONPATH=src python3 -m agents_framework.cli run lint --projects all
```

## Install as local CLI

```bash
python3 -m pip install -e .
agentsfw scan
agentsfw validate
```

## Tests and smoke run

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py'
zsh scripts/smoke_run.sh
```

## Agent guidelines

All agent files (`AGENTS.md`, `AGENT_PROMPT.md`, `AGENT_QUIZ.*`, task tracking files) are
stored in this repository under `guidelines/projects/<project-name>/`, not in the mounted
project roots.

### How guidelines work

- **`guidelines/base/AGENTS.md`** — shared rules that apply to all projects: file access,
  CLI usage, git commits, pager suppression, markdown formatting, etc.
- **`guidelines/projects/<name>/AGENTS.md`** — project-specific overrides and additions.
  Any section with the same `## Heading` as the base **replaces** it; new sections are
  appended after the base.

### How startup prompts work

- **`guidelines/base/AGENT_PROMPT.md`** — shared startup workflow blocks.
- **`guidelines/projects/<name>/AGENT_PROMPT.md`** — project-specific prompt overrides.
  Prompts use the same heading-based merge semantics as guidelines.

### Generate a merged AGENTS.md

```bash
# Write merged file to guidelines/projects/<name>/AGENTS_MERGED.md
PYTHONPATH=src python3 -m agents_framework.cli guidelines generate deepblue-documents-kube

# Regenerate all configured projects at once
PYTHONPATH=src python3 -m agents_framework.cli guidelines generate all

# Print merged content to stdout (useful for review or piping)
PYTHONPATH=src python3 -m agents_framework.cli guidelines generate dor-react-app --print
```

`AGENTS_MERGED.md` is gitignored (auto-generated artefact). The two source-of-truth files
are `guidelines/base/AGENTS.md` and `guidelines/projects/<name>/AGENTS.md`.

### Generate a merged AGENT_PROMPT.md

```bash
# Write merged file to guidelines/projects/<name>/AGENT_PROMPT_MERGED.md
PYTHONPATH=src python3 -m agents_framework.cli prompt generate deepblue-documents-kube

# Regenerate all configured projects at once
PYTHONPATH=src python3 -m agents_framework.cli prompt generate all

# Print merged content to stdout (useful for review or piping)
PYTHONPATH=src python3 -m agents_framework.cli prompt generate dor-react-app --print
```

`AGENT_PROMPT_MERGED.md` is gitignored (auto-generated artefact). The two source-of-truth
files are `guidelines/base/AGENT_PROMPT.md` and
`guidelines/projects/<name>/AGENT_PROMPT.md`.

## Notes

- The framework does not modify the source projects.
- Mounted projects are expected under `mounted-projects/` via symlinks.
- Reusable framework helper scripts live in `scripts/`; mounted projects remain
  agent-unaware.
- Add or update tasks in `config/projects.json` as project workflows evolve.
- Agent meta-files for this project (`AGENTS.md`, `AGENT_PROMPT.md`, `AGENT_QUIZ.md`,
  `AGENT_QUIZ_ANSWERS.md`, `AGENT_TODO.md`, `AGENT_DONE.md`) live at the repository root.
- Agent files for each mounted project live under `guidelines/projects/<name>/`.
- `AGENTS_MERGED.md` and `AGENT_PROMPT_MERGED.md` files are gitignored auto-generated
  artefacts; regenerate on demand.

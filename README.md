# Agents Multi-Project Development Framework

This repository now provides a lightweight framework for coordinating development tasks across multiple mounted projects under one root.

## Included project catalog

`config/projects.json` contains the six requested projects and stack-specific commands:

- `deepblue-documents-kube`
- `dor-depot`
- `dor-react-app`
- `dspace-containerization`
- `findingaids-argocd`
- `umich-arclight`

## Directory layout

```text
agents/
  config/projects.json
  guidelines/
    base/
      AGENTS.md                 # Shared rules for all projects
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
  tests/
  scripts/smoke_run.sh
```

## Quick start

Create mounts (symlinks) from the source root:

```bash
cd /Users/gkostin/GitHub/gkostin1966/agents
python3 -m agents_framework.cli init-mounts --source-root /Users/gkostin/GitHub/mlibrary
```

Scan status and marker detection:

```bash
cd /Users/gkostin/GitHub/gkostin1966/agents
python3 -m agents_framework.cli scan
```

Dry-run a task on one or more projects:

```bash
cd /Users/gkostin/GitHub/gkostin1966/agents
python3 -m agents_framework.cli run test --projects dor-react-app,dor-depot --dry-run
```

Run a configured task for all mounted projects:

```bash
cd /Users/gkostin/GitHub/gkostin1966/agents
python3 -m agents_framework.cli run lint --projects all
```

## Install as local CLI

```bash
cd /Users/gkostin/GitHub/gkostin1966/agents
python3 -m pip install -e .
agentsfw scan
```

## Tests and smoke run

```bash
cd /Users/gkostin/GitHub/gkostin1966/agents
python3 -m unittest discover -s tests -p 'test_*.py'
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

### Generate a merged AGENTS.md

```bash
# Write merged file to guidelines/projects/<name>/AGENTS_MERGED.md
PYTHONPATH=src python3 -m agents_framework.cli guidelines generate deepblue-documents-kube

# Print merged content to stdout (useful for review or piping)
PYTHONPATH=src python3 -m agents_framework.cli guidelines generate dor-react-app --print
```

`AGENTS_MERGED.md` is gitignored (auto-generated artefact). The two source-of-truth files
are `guidelines/base/AGENTS.md` and `guidelines/projects/<name>/AGENTS.md`.

## Notes

- The framework does not modify the source projects.
- Mounted projects are expected under `mounted-projects/` via symlinks.
- Add or update tasks in `config/projects.json` as project workflows evolve.
- Agent meta-files for this project (`AGENTS.md`, `AGENT_PROMPT.md`, `AGENT_QUIZ.md`,
  `AGENT_QUIZ_ANSWERS.md`, `AGENT_TODO.md`, `AGENT_DONE.md`) live at the repository root.
- Agent files for each mounted project live under `guidelines/projects/<name>/`.
- `AGENTS_MERGED.md` files are gitignored auto-generated artefacts; regenerate on demand.

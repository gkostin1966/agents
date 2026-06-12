# Agents Multi-Project Development Framework

This repository now provides a lightweight framework for coordinating development tasks across multiple mounted projects under one root.

## Project catalog

`config/projects.json` is the source of truth for configured mounted projects and
stack-specific commands.

- Each project is an abstract framework entry with `name`, `stack`, `relative_path`,
  `commands`, and required `source_path`.
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
      <project-name>/
        AGENTS.md               # Project-specific rules (self-contained)
        AGENT_PROMPT.md         # Session startup prompt
        AGENT_QUIZ.md           # Optional onboarding quiz
        AGENT_QUIZ_ANSWERS.md   # Optional quiz answers
        AGENT_TODO.md           # Optional active task list
        AGENT_DONE.md           # Optional completed task archive
        tasks/                  # Optional per-ticket task directories
  mounted-projects/             # Symlinks to source repos are created here; each mount also gets `.agents`
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

Actual project names are defined in `config/projects.json`.

## Quick start

Create mounts (symlinks) from each project's configured `source_path`; each mounted
project also gets a `.agents` link to `guidelines/projects/<name>`:

```bash
PYTHONPATH=src python3 -m agents_framework.cli init-mounts
```

Add a new project and mount it immediately from any path:

```bash
PYTHONPATH=src python3 -m agents_framework.cli project add my-project --stack react-vite --source-path /absolute/path/to/my-project
```

`project add` also creates `guidelines/projects/<name>/AGENTS.md` and
`guidelines/projects/<name>/AGENT_PROMPT.md` when missing (copied from
`guidelines/base/` when available), so `.agents` is linked on first mount.

Supported `--stack` values: `rails-arclight`, `k8s-gitops`, `java-spring`,
`react-vite`, `dspace-docker`.

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

## Two-Hat Workflow

Use two IDE contexts depending on what you are doing:

- **Project hat** (`mounted-projects/<name>/`): work inside the mounted project root and `.agents/` only.
- **Framework hat** (`agents/` repo root): update framework-managed guidance, run generation commands, and run framework utilities.

### Project hat (local IDE or devcontainer)

- Start agent sessions from the mounted project root.
- Read startup/rules/tasks through `.agents/`.
- Keep project-local helper scripts under `.agents/scripts/`.

```bash
cd /Users/gkostin/GitHub/gkostin1966/agents/mounted-projects/boxwalker
ls -la .agents/AGENT_PROMPT.md .agents/AGENTS.md .agents/tasks/README.md | cat
```

### Framework hat (local IDE)

- Edit source-of-truth files under `guidelines/projects/<name>/`.
- Regenerate merged files when needed.
- Run `.agents` integrity checks for mounted projects.

```bash
cd /Users/gkostin/GitHub/gkostin1966/agents
PYTHONPATH=src python3 -m agents_framework.cli bootstrap boxwalker
python3 scripts/check_agents_link.py --project boxwalker | cat
```

## Agent guidelines

All agent files (`AGENTS.md`, `AGENT_PROMPT.md`, `AGENT_QUIZ.*`, task tracking files) are
stored in this repository under `guidelines/projects/<project-name>/`, not in the mounted
project roots. Each project file is **self-contained** — base rules are inlined and managed
through the two-hat workflow.

### How guidelines work

- **`guidelines/base/AGENTS.md`** — shared rules used as the reference for `sync-base`.
- **`guidelines/projects/<name>/AGENTS.md`** — self-contained project file with base rules
  inlined. Sections that differ from base are considered customized and protected from
  automatic sync.

### Propagate base rule changes (framework hat)

```bash
# Show which sections have drifted from base
PYTHONPATH=src python3 -m agents_framework.cli diff-base boxwalker

# Sync unchanged sections; skip project-customized sections
PYTHONPATH=src python3 -m agents_framework.cli sync-base boxwalker

# Force-replace all sections including customized ones
PYTHONPATH=src python3 -m agents_framework.cli sync-base boxwalker --force
```

### How startup prompts work

- **`guidelines/base/AGENT_PROMPT.md`** — reference prompt blocks.
- **`guidelines/projects/<name>/AGENT_PROMPT.md`** — self-contained project startup prompt.

### Get one-shot bootstrap text

Print copy/paste startup text for a project session:

```bash
PYTHONPATH=src python3 -m agents_framework.cli bootstrap dor-depot
```

Or paste this directly in a mounted-project agent chat:

```text
Read .agents/AGENT_PROMPT.md and follow it.
Then read .agents/AGENTS.md and follow those rules for all code changes.
```


No merge artifacts are generated. The agent reads `AGENTS.md` and `AGENT_PROMPT.md`
directly from `.agents/` inside the project.

## Notes

- The framework does not modify the source projects.
- Mounted projects are expected under `mounted-projects/` via symlinks.
- Reusable framework helper scripts live in `scripts/`; mounted projects remain
  agent-unaware.
- Day-to-day commands and workflows live in `docs/developer-cheatsheet.md`.
- Boxwalker onboarding walkthrough lives in `docs/boxwalker-agent-quick-start.md`.
- Add or update tasks in `config/projects.json` as project workflows evolve.
- Agent meta-files for this project (`AGENTS.md`, `AGENT_PROMPT.md`, `AGENT_QUIZ.md`,
  `AGENT_QUIZ_ANSWERS.md`, `AGENT_TODO.md`, `AGENT_DONE.md`) live at the repository root.
- Agent files for each mounted project live under `guidelines/projects/<name>/` and are
  self-contained — no merge artifacts are generated.

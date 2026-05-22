# scripts/

Reusable helper scripts for the `agents` framework repository.

## Purpose

- Keep framework-specific automation in one discoverable place.
- Avoid creating agent tooling inside `mounted-projects/`.
- Prefer these scripts over ad-hoc one-liners when a task repeats.

## Conventions

- Python scripts: `scripts/<name>.py`
- Shell scripts: `scripts/<name>.sh`
- Include a short module docstring or header comment with usage.
- Scripts should be non-interactive and safe for tool-driven execution.
- Use `| cat` when invoking commands that might page.

## Current scripts

- `scripts/smoke_run.sh` — framework smoke run:
  - runs unit tests
  - runs `agentsfw scan`
  - runs `agentsfw validate`
  - regenerates merged guidelines/prompts for all projects
  - runs one dry-run task command
- `scripts/check_token_budgets.py` — always-on context budget guardrail:
  - checks line-count and byte-size budgets for `AGENTS.md`, `guidelines/base/AGENTS.md`, and `.github/copilot-instructions.md`
  - exits non-zero when files exceed budget or are missing

## Usage

```shell
bash scripts/smoke_run.sh
python3 scripts/check_token_budgets.py | cat
```


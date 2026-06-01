---
applyTo: "guidelines/**/*.md"
---
# Guidelines editing rules

- Edit base → regenerate all: `PYTHONPATH=src python3 -m agents_framework.cli guidelines generate all`
- Edit project → regenerate one: `PYTHONPATH=src python3 -m agents_framework.cli guidelines generate <name>`
- Same pattern for prompts: `prompt generate all / <name>`
- Merged files (`AGENTS_MERGED.md`, `AGENT_PROMPT_MERGED.md`) are gitignored — never commit them.
- Matching `## Heading` in project file replaces the base section entirely.
- New project: add to `config/projects.json` first, then create `guidelines/projects/<name>/` files.


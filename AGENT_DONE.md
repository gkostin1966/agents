# AGENT_DONE

<!-- Entries are prepended (newest first). -->

## 2026-05-20T12:00:00 — Add AGENT_PROMPT base+project merge support

Added a mergeable startup-prompt architecture mirroring the existing AGENTS.md merge model:
- `guidelines/base/AGENT_PROMPT.md` — shared startup blocks with explicit `## Heading` sections.
- All six `guidelines/projects/<name>/AGENT_PROMPT.md` files refactored to the same block schema; project-specific sections override base sections on matching headings.
- New `dspace-containerization/AGENT_PROMPT.md` created (was previously missing).
- `src/agents_framework/prompts.py` — `merge_prompts()` and `generate_merged_prompt()`.
- `agentsfw prompt generate <project> [--print] [--output]` CLI subcommand added.
- `tests/test_prompts.py` — 4 new tests; total suite now 11 passing.
- `AGENT_PROMPT_MERGED.md` added to `.gitignore`.
- `AGENTS.md` and `README.md` updated with prompt architecture documentation.

Created the full project structure:
- Python framework package (`src/agents_framework/`) with CLI, config, framework, and
  guidelines merge engine.
- `config/projects.json` cataloguing six mounted projects.
- `guidelines/base/AGENTS.md` — shared agent rules for all projects.
- `guidelines/projects/<name>/AGENTS.md` for all six projects — project-specific overrides
  and additions.
- Copied all existing agent files (`AGENT_PROMPT.md`, `AGENT_QUIZ.md`,
  `AGENT_QUIZ_ANSWERS.md`, task tracking files) from source repos into
  `guidelines/projects/<name>/`.
- Meta-agent files for this project: `AGENTS.md`, `AGENT_PROMPT.md`, `AGENT_QUIZ.md`,
  `AGENT_QUIZ_ANSWERS.md`, `AGENT_TODO.md`, `AGENT_DONE.md`.
- 7 passing unit tests covering framework scanning and guidelines merge logic.

## 2026-05-20T00:00:00 — Bootstrap agents meta-framework

Created the full project structure:
- Python framework package (`src/agents_framework/`) with CLI, config, framework, and
  guidelines merge engine.
- `config/projects.json` cataloguing six mounted projects.
- `guidelines/base/AGENTS.md` — shared agent rules for all projects.
- `guidelines/projects/<name>/AGENTS.md` for all six projects — project-specific overrides
  and additions.
- Copied all existing agent files (`AGENT_PROMPT.md`, `AGENT_QUIZ.md`,
  `AGENT_QUIZ_ANSWERS.md`, task tracking files) from source repos into
  `guidelines/projects/<name>/`.
- Meta-agent files for this project: `AGENTS.md`, `AGENT_PROMPT.md`, `AGENT_QUIZ.md`,
  `AGENT_QUIZ_ANSWERS.md`, `AGENT_TODO.md`, `AGENT_DONE.md`.
- 7 passing unit tests covering framework scanning and guidelines merge logic.


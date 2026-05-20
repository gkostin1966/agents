# AGENT_DONE

<!-- Entries are prepended (newest first). -->

## 2026-05-20T17:20:00 — Standardize communication drafts as Markdown in `communications/`

Made base guidance use `communications/*.md` for email/Slack/etc drafts and removed
project-specific overrides for this section so the shared default applies consistently.

- [x] Update `guidelines/base/AGENTS.md` to define Markdown drafts in `communications/`
- [x] Remove project overrides for the communication-drafts section so base applies everywhere
- [x] Regenerate affected merged guideline files and verify output
- [x] Verify the current state of the project achieves the task goal
- [x] Verify with the developer that the task is complete

## 2026-05-20T17:00:00 — Standardize framework utility scripts on `scripts/`

Updated framework guidance and documentation so this repository uses `scripts/`
as the canonical utility-script location while keeping mounted projects agent-unaware.

- [x] Update root/framework guidance to explicitly use `scripts/` for this repository
- [x] Remove or reword remaining repo-specific `dotpy/` references where they should point to `scripts/`
- [x] Add `scripts/README.md` documenting script conventions and current utilities
- [x] Verify commands and tests still pass after documentation/tooling updates
- [x] Verify the current state of the project achieves the task goal
- [x] Verify with the developer that the task is complete

## 2026-05-20T16:45:00 — Refactor and feature additions from review

Ten-item improvement plan completed: DRY merge refactor, dead code removal, CLI feature additions,
housekeeping fixes, quiz updates, and expanded test coverage.

- [x] Extract shared `merge.py` module; update `guidelines.py` and `prompts.py` to use it
- [x] Remove dead `guidelines_path` field from `config/projects.json`; remove unused `marker_path` property from `ProjectConfig`
- [x] Add `all` support to `guidelines generate` and `prompt generate` CLI commands
- [x] Add `.idea*/` and `pr-summary.md` to `.gitignore`
- [x] Add `agentsfw validate` subcommand for per-project agent-file completeness check
- [x] Fix `dotpy/` vs `/tmp/` commit instruction contradiction between `guidelines/base/AGENTS.md` and `AGENTS.md`
- [x] Create `dspace-containerization` `AGENT_QUIZ.md` and `AGENT_QUIZ_ANSWERS.md`
- [x] Update root `AGENT_QUIZ.md` and `AGENT_QUIZ_ANSWERS.md` to cover `prompts.py` and `prompt generate`
- [x] Extend test coverage: `init_mounts`, `run_task` dry-run, `load_config`, file-write paths for generate functions
- [x] Verify the current state of the project achieves the task goal
- [x] Verify with the developer that the task is complete

## 2026-05-20T16:40:16 — Resuming a session

1. Check working state: `git branch --show-current | cat` and `git --no-pager status | cat`
2. Read [`AGENTS.md`](AGENTS.md) (meta-rules and conventions for this project).
3. Read the top entry of [`AGENT_DONE.md`](AGENT_DONE.md) for recent completion context.
4. Read this file — the first unchecked subtask in the first task below is where to pick up.

---

<!-- Add new tasks below this line. Keep the most urgent task first. -->

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


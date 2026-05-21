# AGENT_DONE

<!-- Entries are prepended (newest first). -->

## 2026-05-21T14:57:43Z — Mount dor-depot project symlink

Created the `mounted-projects/dor-depot` symlink from the provided source path and verified framework scan now detects `dor-depot` as mounted.

- [x] Resolve source root and mount only `dor-depot`
- [x] Run framework scan to verify `dor-depot` is mounted
- [x] Verify the current state of the project achieves the task goal
- [x] Verify with the developer that the task is complete

## 2026-05-21T14:52:45Z — Systematic framework-purpose alignment review

Reviewed root framework docs and onboarding artifacts for wording that overfit current mounted repositories, and updated them to emphasize the framework's generic meta-purpose and config-driven project registration.

- [x] Audit root docs/prompts for project-specific assumptions that conflict with framework-first guidance
- [x] Update root docs/prompts to treat mounted projects as configured abstract entries
- [x] Ensure first-time mount registration in `config/projects.json` is explicitly documented
- [x] Verify the current state of the project achieves the task goal
- [x] Verify with the developer that the task is complete

## 2026-05-21T14:52:44Z — Refactor root onboarding quiz to framework-only scope

Updated `AGENT_QUIZ.md` and `AGENT_QUIZ_ANSWERS.md` to focus on the `agents` framework itself, treat mounted projects as abstract entries, and codify first-time registration in `config/projects.json`.

- [x] Redraft `AGENT_QUIZ.md` to remove concrete mounted-project trivia and use framework-scoped questions
- [x] Redraft `AGENT_QUIZ_ANSWERS.md` to match the new framework-scoped quiz
- [x] Verify the new quiz explicitly states that first-time mounted projects must be added to `config/projects.json`
- [x] Verify the current state of the project achieves the task goal
- [x] Verify with the developer that the task is complete

## 2026-05-21T10:26:50 — Make merged provenance paths repo-relative

Avoid absolute-path leakage and non-determinism in merged guideline/prompt headers.

- [x] Use stable repo-relative project path text in merged provenance headers
- [x] Add tests that fail if absolute project paths appear in merged output
- [x] Verify tests pass
- [x] Verify the current state of the project achieves the task goal
- [x] Verify with the developer that the task is complete

## 2026-05-21T10:26:51 — Make CLI repo-root resolution install-safe

Ensure `agentsfw` does not rely on `__file__` paths that break in non-editable installs.

- [x] Resolve repo root from `--repo-root` or current working directory
- [x] Add clear error when resolved root does not contain `config/projects.json`
- [x] Add tests for repo-root resolution behavior
- [x] Verify tests pass
- [x] Verify the current state of the project achieves the task goal
- [x] Verify with the developer that the task is complete

## 2026-05-21T10:26:52 — Improve smoke script shell portability

Switch `scripts/smoke_run.sh` to a portable shebang and align docs.

- [x] Change `scripts/smoke_run.sh` shebang from zsh to bash
- [x] Update `scripts/README.md` invocation example to bash
- [x] Run `bash scripts/smoke_run.sh` to verify behavior
- [x] Verify the current state of the project achieves the task goal
- [x] Verify with the developer that the task is complete

## 2026-05-21T10:26:53 — Review reviewer changes and respond to comments

Review code-reviewer edits for correctness, apply any needed follow-up fixes, and prepare responses to all reviewer comments.

- [x] Review each reviewer-provided change for correctness and project-rule compliance
- [x] Address any remaining reviewer comments with code or documentation updates
- [x] Prepare concise response notes for each reviewer comment (resolved/updated/explanation)
- [x] Verify the current state of the project achieves the task goal
- [x] Verify with the developer that the task is complete

## 2026-05-21T10:26:54 — Sync agent files and refresh PR summary

Bring project agent artifacts in line with the current framework state and update `pr-summary.md` accordingly.

- [x] Review changed agent/framework files and align wording/state with current behavior
- [x] Update `pr-summary.md` to reflect the latest cumulative branch changes
- [x] Verify the current state of the project achieves the task goal
- [x] Verify with the developer that the task is complete

## 2026-05-21T10:26:55 — Fix stale config schema reference in quiz answer A24

Ensure onboarding quiz content matches the current `config/projects.json` schema (no `guidelines_path` field).

- [x] Update `AGENT_QUIZ_ANSWERS.md` A24 to remove `guidelines_path`
- [x] Update `AGENT_QUIZ.md` Q24 wording if needed to emphasize current schema
- [x] Verify the current state of the project achieves the task goal
- [x] Verify with the developer that the task is complete

## 2026-05-21T10:26:56 — Prevent `all + --output` overwrite in generate commands

Ensure `agentsfw guidelines|prompt generate all --output ...` cannot silently overwrite one file repeatedly.

- [x] Update CLI generation logic to reject `--output` when project target is `all`
- [x] Add tests covering rejected `all + --output` behavior
- [x] Fix `validate_projects` filtering so `project_names=[]` validates none (not all)
- [x] Add tests covering empty-list validation behavior
- [x] Verify tests pass
- [x] Verify the current state of the project achieves the task goal
- [x] Verify with the developer that the task is complete

## 2026-05-21T10:26:57 — Make init-mounts source path follow relative_path

Ensure mount source lookup remains correct when `relative_path` differs from project `name`.

- [x] Update `init_mounts` source-path derivation to use `relative_path`
- [x] Ensure destination parent directories are created for nested `relative_path` values
- [x] Add tests for differing/nested `relative_path` mount behavior
- [x] Verify tests pass
- [x] Verify the current state of the project achieves the task goal
- [x] Verify with the developer that the task is complete

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


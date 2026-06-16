# AGENT_DONE

<!-- Entries are prepended (newest first). -->

## 2026-06-16T15:51:17Z — Audit umich-arclight agent files outside vs inside .agents/

Compared root-level umich-arclight agent files against `.agents/` equivalents and identified migration requirements before root cleanup.

- [x] Read and compare `mounted-projects/umich-arclight/AGENTS.md` against `mounted-projects/umich-arclight/.agents/AGENTS.md` — note any content differences, additions, or staleness
- [x] Read and compare `mounted-projects/umich-arclight/AGENT_PROMPT.md` against `mounted-projects/umich-arclight/.agents/AGENT_PROMPT.md`
- [x] Read and compare `mounted-projects/umich-arclight/AGENT_QUIZ.md` against `mounted-projects/umich-arclight/.agents/AGENT_QUIZ.md`
- [x] Read and compare `mounted-projects/umich-arclight/AGENT_QUIZ_ANSWERS.md` against `mounted-projects/umich-arclight/.agents/AGENT_QUIZ_ANSWERS.md`
- [x] Inspect `mounted-projects/umich-arclight/tasks/` — determine if task files have equivalents under `.agents/tasks/` or are orphaned
- [x] Produce a written comparison summary: which files are stale copies, which have unique content, and whether any data would be lost by removing the root-level files
- [x] Recommend action: remove root-level files, migrate unique content to `.agents/`, or keep as-is with rationale
- [x] Verify with the developer that the task is complete

## 2026-06-16T15:51:17Z — umich-arclight — migrate essential AGENTS behavior into .agents/AGENTS.md

Merged essential root-level behaviors into framework-managed umich-arclight guidance before deleting root agent files.

- [x] Merge unique root-level behaviors into `guidelines/projects/umich-arclight/AGENTS.md` (dotpy/email conventions, markdown tooling commands, richer command-line safety, detailed task/session workflow where still missing)
- [x] Regenerate `PYTHONPATH=src python3 -m agents_framework.cli guidelines generate umich-arclight`
- [x] Verify with the developer that the task is complete

## 2026-06-16T15:51:17Z — umich-arclight — migrate root dotpy scripts and emails directory into .agents/

Copied root utility script and email-draft scaffolding into framework-managed `.agents` locations and updated references.

- [x] Create `guidelines/projects/umich-arclight/dotpy/` and copy root `dotpy/` scripts there, updating paths to `.agents/dotpy/` where needed
- [x] Create `guidelines/projects/umich-arclight/emails/` with `.keep`
- [x] Update `guidelines/projects/umich-arclight/AGENTS.md` to reference `.agents/dotpy/` and `.agents/emails/`
- [x] Regenerate `PYTHONPATH=src python3 -m agents_framework.cli guidelines generate umich-arclight`
- [x] Verify with the developer that the task is complete

## 2026-06-16T15:51:17Z — umich-arclight — populate .agents/tasks/README.md from root tasks index

Copied the root task index into framework-managed `.agents/tasks/README.md` so root task index removal is safe.

- [x] Copy content from `mounted-projects/umich-arclight/tasks/README.md` into `guidelines/projects/umich-arclight/tasks/README.md` with framework-relative path wording
- [x] Verify with the developer that the task is complete

## 2026-06-16T15:51:17Z — umich-arclight — remove root-level agent infrastructure files from mounted project (developer action)

Developer removed root-level umich-arclight agent infrastructure after migration to `.agents/`-backed framework files.

- [x] Confirm all preceding umich-arclight migration tasks are developer-verified complete
- [x] Developer removes `AGENT_QUIZ.md` and `AGENT_QUIZ_ANSWERS.md` from `umich-arclight/` root (safe immediately — identical to `.agents/`)
- [x] Developer removes `AGENTS.md` and `AGENT_PROMPT.md` from `umich-arclight/` root (safe after migration)
- [x] Developer removes `tasks/README.md` and root `tasks/` directory if no ticket files remain
- [x] Developer removes root `dotpy/` and `emails/` directories after `.agents/` migration is complete
- [x] Verify with the developer that the task is complete

## 2026-06-16T15:41:10Z — Audit dor-react-app agent files outside vs inside .agents/

Compared root-level agent files against `.agents/` equivalents and identified migration gaps before cleanup.

- [x] Read and compare `mounted-projects/dor-react-app/AGENTS.md` against `mounted-projects/dor-react-app/.agents/AGENTS.md` — note any content differences, additions, or staleness
- [x] Read and compare `mounted-projects/dor-react-app/AGENT_PROMPT.md` against `mounted-projects/dor-react-app/.agents/AGENT_PROMPT.md`
- [x] Read and compare `mounted-projects/dor-react-app/AGENT_QUIZ.md` against `mounted-projects/dor-react-app/.agents/AGENT_QUIZ.md`
- [x] Read and compare `mounted-projects/dor-react-app/AGENT_QUIZ_ANSWERS.md` against `mounted-projects/dor-react-app/.agents/AGENT_QUIZ_ANSWERS.md`
- [x] Inspect `mounted-projects/dor-react-app/tasks/` — determine if task files have equivalents under `.agents/tasks/` or are orphaned
- [x] Produce a written comparison summary: which files are stale copies, which have unique content, and whether any data would be lost by removing the root-level files
- [x] Recommend action: remove root-level files, migrate unique content to `.agents/`, or keep as-is with rationale
- [x] Verify with the developer that the task is complete

## 2026-06-16T15:41:10Z — dor-react-app — fix Email Drafts convention in .agents/AGENTS.md

Updated dor-react-app guidance to keep project-specific RTF email drafting behavior.

- [x] Replace the `## Email Drafts for Third Parties` section in `guidelines/projects/dor-react-app/AGENTS.md` with the RTF/`emails/` convention from the root `AGENTS.md`
- [x] Regenerate `PYTHONPATH=src python3 -m agents_framework.cli guidelines generate dor-react-app`
- [x] Verify with the developer that the task is complete

## 2026-06-16T15:41:10Z — dor-react-app — add Markdown table tools to .agents/AGENTS.md

Added project-specific table utility command guidance under dor-react-app `.agents` rules.

- [x] Expand the `## Markdown Tables` section in `guidelines/projects/dor-react-app/AGENTS.md` with the three `dotpy/` table commands and their usage
- [x] Regenerate `PYTHONPATH=src python3 -m agents_framework.cli guidelines generate dor-react-app`
- [x] Verify with the developer that the task is complete

## 2026-06-16T15:41:10Z — dor-react-app — elevate dotpy/commit.py to primary multiline commit path in .agents/AGENTS.md

Made the project-specific multiline commit workflow use the dotpy helper as the primary path.

- [x] Update `## Git Commits` in `guidelines/projects/dor-react-app/AGENTS.md` to make `dotpy/commit.py` the required multiline path rather than a fallback
- [x] Regenerate `PYTHONPATH=src python3 -m agents_framework.cli guidelines generate dor-react-app`
- [x] Verify with the developer that the task is complete

## 2026-06-16T15:41:10Z — dor-react-app — expand React conventions and Task Tracking in .agents/AGENTS.md

Expanded dor-react-app framework guidance to preserve essential project-specific behavior before root-file cleanup.

- [x] Expand `## React / Node.js / Vite Conventions` in `guidelines/projects/dor-react-app/AGENTS.md` with full project structure and key deps
- [x] Strengthen `## Task Tracking` to include explicit developer-approval-before-implementing requirement (already present — confirmed)
- [x] Regenerate `PYTHONPATH=src python3 -m agents_framework.cli guidelines generate dor-react-app`
- [x] Verify with the developer that the task is complete

## 2026-06-16T15:41:10Z — dor-react-app — populate .agents/tasks/README.md with archive index

Copied task index/archive metadata into `.agents` so root task index can be safely removed.

- [x] Copy content from root `tasks/README.md` into `guidelines/projects/dor-react-app/tasks/README.md`, updating any path references to be framework-relative
- [x] Verify with the developer that the task is complete

## 2026-06-16T15:41:10Z — dor-react-app — remove root-level agent files from mounted project (developer action)

Developer removed redundant root-level agent infrastructure from dor-react-app after migration to `.agents/`.

- [x] Confirm all preceding dor-react-app migration tasks are developer-verified complete
- [x] Developer removes `AGENT_QUIZ.md` from `dor-react-app/` root (safe immediately — identical to `.agents/`)
- [x] Developer removes `AGENT_QUIZ_ANSWERS.md` from `dor-react-app/` root (safe immediately — identical to `.agents/`)
- [x] Developer removes `AGENTS.md` from `dor-react-app/` root (safe after migration tasks complete)
- [x] Developer removes `AGENT_PROMPT.md` from `dor-react-app/` root (safe after migration tasks complete)
- [x] Developer removes `tasks/README.md` from `dor-react-app/` root and the empty `tasks/` directory if no ticket dirs remain (safe after tasks/README.md populated in `.agents/`)
- [x] Verify with the developer that the task is complete

## 2026-06-16T15:03:46Z — Implement guideline usability improvements from critique

Added shared usability structure and scanning aids to base guidance files.

- [x] Add a concise `Quick Session Checklist` section to `guidelines/base/AGENTS.md` for fast startup scanning
- [x] Add context tagging guidance (`always`, `when-bookkeeping`, `when-committing`) in `guidelines/base/AGENTS.md`
- [x] Add a canonical `.agents` policy section in `guidelines/base/AGENTS.md` and reduce duplication where practical
- [x] Add a compact startup checklist to `guidelines/base/AGENT_PROMPT.md`
- [x] Update `guidelines/projects/boxrunner/AGENTS.md` to align with the improved structure while preserving project-specific rules
- [x] Regenerate merged outputs after edits (`guidelines generate all`, `prompt generate all`)
- [x] Verify with the developer that the task is complete

## 2026-06-16T15:03:46Z — Propagate guideline usability improvements to all projects

Applied and harmonized new shared sections and tag conventions across configured projects.

- [x] Run `PYTHONPATH=src python3 -m agents_framework.cli diff-base <project> --file AGENTS.md` across configured projects to map drift
- [x] Apply non-force `sync-base` for `AGENTS.md` across all projects to insert new shared sections
- [x] Apply non-force `sync-base` for `AGENT_PROMPT.md` across all projects to insert any new shared sections
- [x] Manually patch project files where customized sections require explicit adoption of new structure/tags
- [x] Re-run `PYTHONPATH=src python3 -m agents_framework.cli guidelines generate all`
- [x] Re-run `PYTHONPATH=src python3 -m agents_framework.cli prompt generate all`
- [x] Validate with `PYTHONPATH=src python3 -m agents_framework.cli validate --projects all`
- [x] Verify with the developer that the task is complete

## 2026-06-16T15:03:46Z — Propagate boxrunner guideline overhaul to boxwalker

Ported boxrunner improvements into boxwalker project guidance and validated merged outputs.

- [x] Diff `guidelines/projects/boxrunner/AGENTS.md` against `guidelines/projects/boxwalker/AGENTS.md` to isolate candidate changes
- [x] Port boxrunner improvements that are boxwalker-compatible into `guidelines/projects/boxwalker/AGENTS.md`
- [x] If startup flow changes are implicated, port matching updates from `guidelines/projects/boxrunner/AGENT_PROMPT.md` to `guidelines/projects/boxwalker/AGENT_PROMPT.md`
- [x] Run `PYTHONPATH=src python3 -m agents_framework.cli guidelines generate boxwalker`
- [x] If prompt was edited, run `PYTHONPATH=src python3 -m agents_framework.cli prompt generate boxwalker`
- [x] Review resulting `guidelines/projects/boxwalker/AGENTS_MERGED.md` (and prompt merged file if generated) for correctness
- [x] Verify with the developer that the task is complete

## 2026-06-16T15:03:46Z — Extract shared rules from boxrunner into base guidelines

Moved cross-project-safe rules to base guidelines while retaining boxrunner-specific guidance in project files.

- [x] Review finalized boxrunner guideline changes and classify each rule as shared vs project-specific
- [x] Move shared rules into `guidelines/base/AGENTS.md` without pulling in boxrunner-only constraints
- [x] Keep project-specific rules in `guidelines/projects/boxrunner/AGENTS.md`
- [x] If shared startup/prompt guidance also changed, update `guidelines/base/AGENT_PROMPT.md`
- [x] Run `PYTHONPATH=src python3 -m agents_framework.cli guidelines generate all`
- [x] If base prompt changed, run `PYTHONPATH=src python3 -m agents_framework.cli prompt generate all`
- [x] Spot-check merged outputs for at least `boxrunner` and `boxwalker` for replacement semantics correctness
- [x] Verify with the developer that the task is complete

## 2026-06-16T15:03:46Z — Propagate updated base guidance across all project guideline files

Used `diff-base`/`sync-base` flow to apply base updates safely across all configured projects and revalidated.

- [x] Run `PYTHONPATH=src python3 -m agents_framework.cli diff-base boxrunner --file AGENTS.md` and capture baseline drift pattern
- [x] For each configured project, run `diff-base` for `AGENTS.md` to identify SAME/CUSTOMIZED/MISSING sections
- [x] Apply `sync-base` project-by-project for `AGENTS.md` (non-force first; force only where explicitly approved)
- [x] If base prompt changed, repeat diff/sync workflow for `AGENT_PROMPT.md`
- [x] Re-run `PYTHONPATH=src python3 -m agents_framework.cli guidelines generate all`
- [x] If prompt changes were applied, re-run `PYTHONPATH=src python3 -m agents_framework.cli prompt generate all`
- [x] Validate framework state with `PYTHONPATH=src python3 -m agents_framework.cli validate --projects all`
- [x] Verify with the developer that the task is complete

## 2026-06-12T05:02:01Z — Make README directory layout generic

Replaced hard-coded per-project examples with a stable template layout and added a note that actual project names come from `config/projects.json`.

- [x] Replace hard-coded project list in README directory layout with a stable template
- [x] Keep examples clear while avoiding per-project churn
- [x] Verify with the developer that the task is complete

## 2026-06-12T05:02:01Z — Remove `init-mounts --source-root` fallback

Removed the legacy shared-parent source-root path from mount logic and CLI so mount resolution is fully config-driven via required per-project `source_path`.

- [x] Make mount resolution config-driven only via project `source_path`
- [x] Remove `--source-root` from CLI and docs
- [x] Update tests for config-driven init-mounts behavior
- [x] Run framework test suite and fix regressions
- [x] Verify with the developer that the task is complete

## 2026-06-12T05:02:01Z — Require `source_path` in project config

Added `source_path` for existing projects and enforced it as a required key in `config/projects.json` loading.

- [x] Add `source_path` for all existing entries in `config/projects.json`
- [x] Enforce `source_path` as required in config loading
- [x] Update docs/tests for required `source_path`
- [x] Run framework test suite and fix regressions
- [x] Verify with the developer that the task is complete

## 2026-06-12T05:02:01Z — Validate `project add --stack`

Added stack validation for `project add` in argparse and command handling, with tests and docs updates.

- [x] Enforce known stack values for `project add`
- [x] Add tests for accepted/rejected stack values
- [x] Update docs to list supported stack identifiers
- [x] Run framework test suite and fix regressions
- [x] Verify with the developer that the task is complete

## 2026-06-12T05:02:01Z — Auto-create guidelines on project add

Updated `project add` to create project guideline files by default (copying from base when available) without overwriting existing files.

- [x] Update `project add` to create `guidelines/projects/<name>/` and required files when missing
- [x] Ensure generated starter files do not overwrite existing project guidelines
- [x] Update docs/tests for the new default behavior
- [x] Run framework test suite and fix regressions
- [x] Verify with the developer that the task is complete

## 2026-06-12T05:02:01Z — Add per-project source paths and project-add CLI

Implemented per-project mount source configuration, added project registration CLI support, and updated docs/tests for the new workflow.

- [x] Extend config model/loading to support optional per-project source path
- [x] Update mount logic/CLI to allow mounting from explicit project source path and single-project mount runs
- [x] Add CLI command to add a project entry and optionally mount it immediately
- [x] Update README quick-start/docs for new workflow
- [x] Run framework test suite and fix regressions
- [x] Verify with the developer that the task is complete

## 2026-06-10T01:29:31Z — Abandon merge model — flatten project files and add sync-base/diff-base

Replaced the base+override merge model with self-contained per-project files. Added `sync-base` and `diff-base` CLI commands for two-hat propagation. Simplified `bootstrap` to no longer generate artifacts. Removed `*_MERGED.md` patterns from `.gitignore` and deleted all existing artifacts.

- [x] Flatten all project AGENTS.md and AGENT_PROMPT.md to self-contained (base rules inlined)
- [x] Add `sync-base` CLI command to propagate base section changes into a project file
- [x] Add `diff-base` CLI command to show drift between base and a project file
- [x] Simplify `bootstrap` to validate files present and print startup text without a merge step
- [x] Remove `*_MERGED.md` from `.gitignore`, delete any existing merged artifacts
- [x] Update tests
- [x] Update docs and cheatsheet
- [x] Verify tests pass
- [x] Verify the current state of the project achieves the task goal
- [x] Verify with the developer that the task is complete

## 2026-06-10T00:58:18Z — Harden two-hat workflow for mounted projects

Documented a formal two-hat workflow, added a mounted-project `.agents` integrity checker, and introduced boxwalker `.agents/scripts` conventions for reusable vs local helper scripts.

- [x] Add a Two-Hat Workflow section to `README.md`
- [x] Add a `.agents` integrity checker script for mounted projects
- [x] Add `.agents/scripts/README.md` conventions for boxwalker
- [x] Verify tests pass
- [x] Verify the current state of the project achieves the task goal
- [x] Verify with the developer that the task is complete

## 2026-06-10T00:30:05Z — Implement `.agents`-first boxwalker startup for devcontainers

Refactored boxwalker startup guidance so agents use `.agents` paths inside the mounted project first, with `AGENTS_ROOT` only as fallback when `.agents` is unavailable.

- [x] Update boxwalker prompt/rules to use `.agents` paths first with `AGENTS_ROOT` fallback only when `.agents` is unavailable
- [x] Update `docs/boxwalker-agent-quick-start.md` after implementation to reflect `.agents`-first workflow
- [x] Verify the current state of the project achieves the task goal
- [x] Verify with the developer that the task is complete

## 2026-06-10T00:30:05Z — Create boxwalker developer quick start guide

Added a story-style quick start walkthrough showing how to prepare task files and start a new boxwalker agent session with practical commands.

- [x] Outline startup flow and required pre-task steps for boxwalker
- [x] Add a new docs guide with boxwalker-specific commands and a storybook walkthrough
- [x] Link the guide from existing docs index/location
- [x] Verify the current state of the project achieves the task goal
- [x] Verify with the developer that the task is complete

## 2026-06-09T20:03:56Z — Consistency audit and developer cheatsheet

Audited the core docs/scripts for stale guidance, aligned the smoke-run target with an actually mounted project, added a daily developer cheatsheet, and refreshed stale summary wording.

- [x] Audit core docs/scripts for contradictory or outdated guidance
- [x] Apply consistency fixes where needed
- [x] Add `docs/developer-cheatsheet.md` with practical daily commands/workflows
- [x] Verify tests pass
- [x] Verify the current state of the project achieves the task goal
- [x] Verify with the developer that the task is complete

## 2026-06-09T20:00:58Z — Link mounted project `.agents` to project guidelines

Refactored the mount flow so each mounted project gets a `.agents` symlink to its `guidelines/projects/<mounted-project>` directory and added tests plus docs coverage.

- [x] Audit mount, scan, and guideline-resolution code paths
- [x] Implement `.agents` link creation/maintenance for mounted projects
- [x] Add or update tests for the new link behavior
- [x] Verify tests pass
- [x] Verify the current state of the project achieves the task goal
- [x] Verify with the developer that the task is complete

## 2026-05-22T21:24:17Z — Create recent changes summary document

Created a single markdown handoff summary covering recent framework changes and key usage commands.

- [x] Add `docs/recent-changes-summary.md` with recent commits and practical impact
- [x] Verify the current state of the project achieves the task goal
- [x] Verify with the developer that the task is complete

## 2026-05-22T21:19:48Z — Add prompt_from_git helper script

Created a local utility that builds a compact AI-ready prompt from staged git changes (summary + file list + capped diff) to reduce token-heavy context setup.

- [x] Add `scripts/prompt_from_git.py`
- [x] Add tests for prompt generation behavior
- [x] Document usage in `scripts/README.md` and `docs/low-token-playbook.md`
- [x] Verify tests pass
- [x] Verify the current state of the project achieves the task goal
- [x] Verify with the developer that the task is complete

## 2026-05-22T21:14:49Z — Add local Ollama helper scripts

Implemented local scripts that use the Ollama HTTP API for prompt compression and PR draft generation so repetitive drafting can be done off-cloud.

- [x] Add `scripts/ollama_prompt_compress.py` and `scripts/ollama_pr_draft.py`
- [x] Add tests covering script core behavior without real network calls
- [x] Document script usage in `scripts/README.md` and `docs/low-token-playbook.md`
- [x] Verify tests pass
- [x] Verify the current state of the project achieves the task goal
- [x] Verify with the developer that the task is complete

## 2026-05-22T21:14:48Z — Create low-token session playbook document

Created a reusable markdown guide that captures the daily low-token workflow for starting and running agent sessions efficiently.

- [x] Add `docs/low-token-playbook.md` with startup commands, prompting rules, and weekly maintenance checks
- [x] Verify the current state of the project achieves the task goal
- [x] Verify with the developer that the task is complete

## 2026-05-22T21:05:43Z — Add token guardrails and terse-default regression checks

Implemented guardrails to keep always-on instruction files within budget and added tests to prevent drift in terse Copilot defaults.

- [x] Add `scripts/check_token_budgets.py` to validate line-count and byte-size budgets for always-on files
- [x] Add tests for budget checker behavior and required terse defaults in `.github/copilot-instructions.md`
- [x] Document usage in `scripts/README.md`
- [x] Verify tests pass
- [x] Verify the current state of the project achieves the task goal
- [x] Verify with the developer that the task is complete

## 2026-05-22T21:00:10Z — Token optimization for agents framework

Applied token-optimization guidance from `github-copilot-token-optimization/` to reduce always-on context cost across the agents framework and all project guideline files.

- [x] T1 — Add `.github/copilot-instructions.md` with output-control defaults (code-only, terse, no explanations unless asked)
- [x] T2 — Compress root `AGENTS.md` to landmines-only: remove discoverable facts, keep only non-obvious rules that cause silent mistakes when missed
- [x] T3 — Compress `guidelines/base/AGENTS.md` with same filter
- [x] T4 — Create scoped `.github/instructions/` files using `applyTo:` for project-specific guideline sections so they load only when relevant files are open (instead of always-on)
- [x] T5 — Compress the root `AGENT_PROMPT.md` and `guidelines/base/AGENT_PROMPT.md` to remove prose that agents don't need pre-loaded
- [x] Verify the current state of the project achieves the task goal
- [x] Verify with the developer that the task is complete

## 2026-05-21T16:27:06Z — Add mounted-project bootstrap prompt command

Implemented a framework command that regenerates merged project files and prints a one-shot bootstrap prompt suitable for starting an agent session in a mounted project.

- [x] Design CLI UX for bootstrap setup output
- [x] Implement command to regenerate merged prompt/guidelines for a project and print one-shot bootstrap text
- [x] Add or update tests for parser wiring and command behavior
- [x] Verify tests pass
- [x] Verify the current state of the project achieves the task goal
- [x] Verify with the developer that the task is complete

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


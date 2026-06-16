# Boxrunner Guidelines Propagation and Critique (2026-06-16)

## Scope Completed

- Propagated the recent `boxrunner` guideline overhaul into `boxwalker` project files.
- Extracted shared, cross-project-safe rules into base files.
- Propagated updated base guidance back into all configured project guideline files.
- Regenerated merged artifacts and validated project guideline completeness.

## Work Completed

- Updated `guidelines/projects/boxwalker/AGENTS.md` with:
  - `.agents/tmp` temp-file conventions (no system `/tmp`)
  - explicit `.agents/` metadata handling boundaries
  - stronger commit-suggestion constraints tied to tracked/staged files
  - expanded session/task-tracking expectations
  - `Response Hygiene` section
- Updated `guidelines/projects/boxwalker/AGENT_PROMPT.md` with:
  - explicit `.agents/` long-term-memory handling notes
  - richer startup defaults
  - branch/ticket fallback behavior when no `BW-\d+` key is present
- Updated `guidelines/base/AGENTS.md` with shared rules from the boxrunner model:
  - `.agents/tmp` usage policy
  - commit-suggestion guardrails
  - new `Response Hygiene` section
- Updated `guidelines/base/AGENT_PROMPT.md` with shared startup guidance:
  - `.agents/` treatment expectations
  - session-default behavior before implementation
- Synced base AGENTS changes into all configured projects via non-force `sync-base`.
- Synced base prompt changes across all projects via non-force `sync-base`.
- Regenerated merged files for all projects (`guidelines generate all`, `prompt generate all`).

## Validation and Commands Run

- `PYTHONPATH=src python3 -m agents_framework.cli guidelines generate boxwalker`
- `PYTHONPATH=src python3 -m agents_framework.cli prompt generate boxwalker`
- `PYTHONPATH=src python3 -m agents_framework.cli guidelines generate all`
- `PYTHONPATH=src python3 -m agents_framework.cli prompt generate all`
- `PYTHONPATH=src python3 -m agents_framework.cli diff-base <project> --file AGENTS.md` (all configured projects)
- `PYTHONPATH=src python3 -m agents_framework.cli sync-base <project> --file AGENTS.md` (all configured projects, non-force)
- `PYTHONPATH=src python3 -m agents_framework.cli diff-base <project> --file AGENT_PROMPT.md` (all configured projects)
- `PYTHONPATH=src python3 -m agents_framework.cli sync-base <project> --file AGENT_PROMPT.md` (all configured projects, non-force)
- `PYTHONPATH=src python3 -m agents_framework.cli validate --projects all`
- Outcome: all configured projects reported `OK`.

## Critique of Boxrunner Guidelines

## What I Like

- Strong operational safety:
  - clear anti-heredoc and anti-multiline-`-c` shell rules reduce session corruption risk.
- Excellent `.agents/` boundary clarity:
  - distinguishes app-code work from framework-memory maintenance.
- Good workflow traceability:
  - `STATUS.md` and `TODO.md` consistency requirements are explicit and practical.
- High verification quality:
  - requires evidence and blocker reporting, reducing ambiguous completion claims.
- Reopen/archival lifecycle is mature:
  - handles post-review follow-up without creating duplicate ticket histories.

## What I Dislike (or See as Risk)

- Density and cognitive load:
  - the file is long and mixes universal rules with project-specific workflow details.
- Repetition across sections:
  - `.agents/` ownership and commit-boundary rules appear in multiple places.
- Some rules are framework-concept-heavy for app-focused tasks:
  - can slow simple coding sessions that do not need deep bookkeeping.
- Table formatting strictness can distract from intent:
  - highly specific markdown-table padding rules are useful but low-value during implementation.
- Potential for section-order churn after sync:
  - moving shared sections (for example `Response Hygiene`) can create noisy diffs.

## Suggested Improvements

- Split into two layers in project guidelines:
  - short "must-follow now" section
  - detailed "operational reference" section
- Deduplicate repeated `.agents/` policy lines and link to one canonical wording block.
- Tag rules by context (`always`, `when-bookkeeping`, `when-committing`) for faster scanning.
- Keep project-specific sections focused on ticket keys, runtime stack, and repo conventions.
- Consider a short per-session checklist at top with links to detailed sections.


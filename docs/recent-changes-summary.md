# Recent Changes Summary

Quick handoff summary of recent `agents` framework updates on branch `dor-depot`.

## Latest Commits (newest first)

| Commit | Message |
|--------|---------|
| `d8cc52d` | `feat: add prompt_from_git helper and docs` |
| `0b75a75` | `feat: add local Ollama drafting helpers and playbook` |
| `fa92145` | `chore: add token guardrails and terse-default tests` |
| `658da17` | `chore: apply broad guideline/token optimization updates` |
| `a9c5815` | `docs: update dor-depot quiz content` |
| `d9af90d` | `feat: add project bootstrap command for agent startup` |

## What Changed

- Added `agentsfw bootstrap <project>` flow to regenerate merged prompt/guideline files and print one-shot startup text.
- Compressed always-on instruction files (`AGENTS.md`, `guidelines/base/AGENTS.md`, prompts) to reduce token overhead.
- Added scoped instruction files under `.github/instructions/` with `applyTo` globs.
- Added token budget guardrails (`scripts/check_token_budgets.py`) + tests.
- Added local Ollama helpers:
  - `scripts/ollama_prompt_compress.py`
  - `scripts/ollama_pr_draft.py`
- Added staged-diff prompt builder:
  - `scripts/prompt_from_git.py`
- Added low-token workflow doc:
  - `docs/low-token-playbook.md`

## Daily Commands

```shell
cd /Users/gkostin/GitHub/gkostin1966/agents
PYTHONPATH=src python3 -m agents_framework.cli bootstrap dor-depot
python3 scripts/check_token_budgets.py | cat
python3 scripts/prompt_from_git.py --max-diff-chars 4000 | cat
```

## Local Ollama Commands

```shell
cd /Users/gkostin/GitHub/gkostin1966/agents
python3 scripts/ollama_prompt_compress.py --input /tmp/prompt.txt | cat
git --no-pager diff --staged | python3 scripts/ollama_pr_draft.py --title "feat: short hint" | cat
```

## Notes

- `AGENTS_MERGED.md` and `AGENT_PROMPT_MERGED.md` remain generated artifacts (gitignored).
- Mounted project source code under `mounted-projects/` remains read-only from this framework repo.


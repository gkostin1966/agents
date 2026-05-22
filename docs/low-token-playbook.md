# Low-Token Session Playbook

Use this playbook to keep Copilot/agent token usage low while preserving delivery speed.

## Daily Workflow (5 Steps)

1. Verify local git state.
2. Regenerate merged guidance for the mounted project.
3. Start a fresh chat and paste one-shot bootstrap text.
4. Run local checks first (format/lint/tests), then ask AI only for deltas.
5. Start a new chat when topic changes.

## Commands

### 1) Check working state

```shell
git branch --show-current | cat
git --no-pager status | cat
```

### 2) Regenerate one-shot bootstrap text

```shell
cd /Users/gkostin/GitHub/gkostin1966/agents
PYTHONPATH=src python3 -m agents_framework.cli bootstrap dor-depot
```

### 3) Run local quality checks before AI help (dor-depot example)

```shell
cd /path/to/dor-depot
./gradlew spotlessApply | cat
./gradlew spotlessCheck | cat
./gradlew test | cat
```

## Prompting Rules (copy/paste)

```text
Code only, no explanation.
3 bullets max.
Touch only <file> and <symbol>.
Do not scan unrelated files.
If unsure, ask 1 question max.
```

## Ask vs Agent Mode

- Use Ask mode for single-step questions.
- Use Agent mode only for multi-step workflows needing tools/files/commands.

## Start New Chat When

- New ticket.
- New subsystem/module.
- Previous issue resolved.
- Responses become verbose/slow/confused.

## Weekly Maintenance

Run instruction-file budget guardrails:

```shell
cd /Users/gkostin/GitHub/gkostin1966/agents
python3 scripts/check_token_budgets.py | cat
```

If budgets fail, shrink always-on files (`AGENTS.md`, `guidelines/base/AGENTS.md`, `.github/copilot-instructions.md`) before continuing.

## Optional: Ollama-First Local Drafting

Use local Ollama for prep tasks, then send compact output to Copilot.

```shell
python3 scripts/ollama_prompt_compress.py --input /tmp/prompt.txt | cat
git --no-pager diff --staged | python3 scripts/ollama_pr_draft.py --title "feat: short hint" | cat
```

Best use cases: prompt compression, first-pass PR summaries, rewrite-to-bullets.


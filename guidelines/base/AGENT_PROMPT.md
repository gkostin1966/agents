# New Session Startup Prompt — Base

> **These are the shared startup blocks for all mounted projects.**
> They are merged with each project's `AGENT_PROMPT.md`.
> Project sections with matching `## Heading` values replace these base sections.

## Prompt Invocation

Copy and paste the line below into a new agent session:

```text
Read AGENT_PROMPT.md and follow the instructions there.
```

## Session Context

You are starting a new session in a mounted project managed by the `agents` meta-framework.
The mounted project contains source code; guidelines, prompts, quizzes, and task tracking live
in the separate `agents` repository.

## Required Developer Input

Before reading any cross-repository file, ask for the absolute path to the `agents`
repository root on this machine. Record it as `AGENTS_ROOT` for this session.

Do not hardcode machine-specific paths.

## Startup Workflow

Before doing anything else, follow these steps in order:

1. **Orient yourself** — run:
   ```shell
   git branch --show-current | cat
   git --no-pager status | cat
   git --no-pager log --oneline -5 | cat
   ```
   If there are uncommitted changes or you are on an unexpected branch, stop and ask the developer how to proceed.

2. **Read local `AGENTS.md`** from the mounted project repository and follow it for all actions.

3. **Read framework-managed task state** under `AGENTS_ROOT/guidelines/projects/<project>/...`
   as defined in the project-specific `## Task Files` block.

4. **Take onboarding quiz** as defined in the project-specific `## Quiz Gate` block.

Do not begin implementation work until the quiz is complete and graded (or explicitly self-graded with developer approval).

## Task Files

Project file overrides this section with exact paths and ticket conventions.

## Quiz Gate

Project file overrides this section with the exact completion message and quiz details.


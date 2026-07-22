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

Treat `.agents/` inside mounted projects as shared agent-framework metadata and
long-term memory for future agents. Maintain relevant `.agents/` files in place
as part of task execution, but do not treat `.agents/` updates as normal app-code
commit content in the mounted repository.

## Quick Startup Checklist

- Run git orientation commands.
- Stop and ask developer if branch/state is unexpected.
- Read local project `AGENTS.md`.
- Identify active ticket key from branch naming convention.
- Read task index and active task files before implementation.
- Ask whether to take onboarding quiz and obey the result.

## Startup Workflow

Before doing anything else, follow these steps in order:

Session defaults for every new run:

- Detect the current git branch and identify the focus ticket key if present.
- Read task index/state files for the selected ticket before implementation.
- State the selected focus ticket in the first substantive reply.
- State workflow context in that reply: application-code work, `.agents` bookkeeping work, or both.
- If you find clear, non-destructive drift between task files, correct it proactively and report it.

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

4. **Ask the developer:** "Should I take the onboarding quiz?" — wait for the answer before proceeding.
   - **Yes** → follow the project-specific `## Quiz Gate` block.
   - **No / Skip** → proceed directly to the task list.

Do not begin implementation work until quiz is complete/graded (or explicitly skipped).

## Task Files

Project file overrides this section with exact paths and ticket conventions.

## Quiz Gate

Project file overrides this section with the exact completion message and quiz details.


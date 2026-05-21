# New Session Startup Prompt — umich-arclight

> **Base prompt applies first**: `guidelines/base/AGENT_PROMPT.md`
> Sections in this file with the same `## Heading` override base startup blocks.

## Prompt Invocation

Copy and paste the line below into a new agent session:

```text
Read AGENT_PROMPT.md and follow the instructions there.
```

## Session Context

You are starting a new session in the `umich-arclight` repository, a Ruby on Rails
application for archival finding-aid discovery built on ArcLight and Blacklight.

## Required Developer Input

Before reading framework-managed files, ask for the absolute path to the `agents`
repository root and store it as `AGENTS_ROOT` for this session.

## Startup Workflow

After completing the base startup workflow, infer the active Jira ticket from the branch
name (for example `ARC-123/my-feature`) and use it to locate ticket files under `tasks/`.

## Task Files

Read these files from `AGENTS_ROOT`:

- `guidelines/projects/umich-arclight/tasks/README.md` (task index)
- `guidelines/projects/umich-arclight/tasks/ARC-nnn/STATUS.md` (active ticket state)
- `guidelines/projects/umich-arclight/tasks/ARC-nnn/TODO.md` (active subtasks)

Replace `ARC-nnn` using the ticket from the current branch.

## Quiz Gate

Take the onboarding quiz from:

- `AGENTS_ROOT/guidelines/projects/umich-arclight/AGENT_QUIZ.md`

After answering all questions, stop and report exactly:

> "I have answered all quiz questions. Please open `AGENT_QUIZ_ANSWERS.md` to grade my answers, or let me know when I may read it to self-grade."

Do not read `AGENT_QUIZ_ANSWERS.md` until explicitly told to compare.

# New Session Startup Prompt — dor-depot

> **Base prompt applies first**: `guidelines/base/AGENT_PROMPT.md`
> Sections in this file with the same `## Heading` override base startup blocks.

## Prompt Invocation

Copy and paste the line below into a new agent session:

```text
Read AGENT_PROMPT.md and follow the instructions there.
```

## Session Context

You are starting a new session in the `dor-depot` repository, a Java Spring Boot
application for digital object preservation with Spring Modulith and OCFL.

## Required Developer Input

Before reading framework-managed files, ask for the absolute path to the `agents`
repository root and store it as `AGENTS_ROOT` for this session.

## Startup Workflow

After completing the base startup workflow, infer the active Jira ticket from the branch
name (for example `DOR-142/foo`) and use it to locate ticket files under `tasks/`.

## Task Files

Read these files from `AGENTS_ROOT`:

- `guidelines/projects/dor-depot/tasks/README.md` (task index)
- `guidelines/projects/dor-depot/tasks/DOR-nnn/STATUS.md` (active ticket state)
- `guidelines/projects/dor-depot/tasks/DOR-nnn/TODO.md` (active subtasks)

Replace `DOR-nnn` using the ticket from the current branch.

## Quiz Gate

Take the onboarding quiz from:

- `AGENTS_ROOT/guidelines/projects/dor-depot/AGENT_QUIZ.md`

After answering all questions, stop and report exactly:

> "I have answered all quiz questions. Please open `AGENT_QUIZ_ANSWERS.md` to grade my answers, or let me know when I may read it to self-grade."

Do not read `AGENT_QUIZ_ANSWERS.md` until explicitly told to compare.

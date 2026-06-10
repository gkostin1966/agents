# New Session Startup Prompt — dor-depot

## Prompt Invocation

Copy and paste the line below into a new agent session:

```text
Read AGENT_PROMPT.md and follow the instructions there.
```

## Session Context

You are starting a new session in the `dor-depot` repository, a Java Spring Boot
application for digital object preservation with Spring Modulith and OCFL.

## Required Developer Input

Use local `.agents` paths first.

- Primary: read guidance from `.agents/` in the project root.
- Fallback only if `.agents/` is missing or unreadable: ask for absolute `AGENTS_ROOT`.

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

- `.agents/AGENT_QUIZ.md`

After answering all questions, stop and report exactly:

> "I have answered all quiz questions. Please open `AGENT_QUIZ_ANSWERS.md` to grade my answers, or let me know when I may read it to self-grade."

Do not read `AGENT_QUIZ_ANSWERS.md` until explicitly told to compare.

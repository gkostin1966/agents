# New Session Startup Prompt — umich-arclight

## Prompt Invocation

Copy and paste the line below into a new agent session:

```text
Read AGENT_PROMPT.md and follow the instructions there.
```

## Session Context

You are starting a new session in the `umich-arclight` repository, a Ruby on Rails
application for archival finding-aid discovery built on ArcLight and Blacklight.

## Required Developer Input

Use local `.agents` paths first.

- Primary: read guidance from `.agents/` in the project root.
- Fallback only if `.agents/` is missing or unreadable: ask for absolute `AGENTS_ROOT`.

## Quick Startup Checklist

- Run git orientation commands.
- Stop and ask developer if branch/state is unexpected.
- Read local project `AGENTS.md`.
- Identify active ticket key from branch naming convention.
- Read task index and active task files before implementation.
- Ask whether to take onboarding quiz and obey the result.

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

- `.agents/AGENT_QUIZ.md`

After answering all questions, stop and report exactly:

> "I have answered all quiz questions. Please open `AGENT_QUIZ_ANSWERS.md` to grade my answers, or let me know when I may read it to self-grade."

Do not read `AGENT_QUIZ_ANSWERS.md` until explicitly told to compare.

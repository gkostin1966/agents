# New Session Startup Prompt — dspace-containerization

## Prompt Invocation

Copy and paste the line below into a new agent session:

```text
Read AGENT_PROMPT.md and follow the instructions there.
```

## Session Context

You are starting a new session in the `dspace-containerization` repository, a Docker,
Docker Compose, and Make based repository for running and testing DSpace services.

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

After completing the base startup workflow, read the local `README.md` and `Makefile`
for target conventions before changing Docker or Compose behavior.

## Task Files

Read these files from `AGENTS_ROOT`:

- `guidelines/projects/dspace-containerization/TODO.md` (active work)
- `guidelines/projects/dspace-containerization/DONE.md` (recent completions)

Use the first unchecked subtask in the first task in `TODO.md` as the resume point.

## Quiz Gate

Take the onboarding quiz from:

- `.agents/AGENT_QUIZ.md`

After answering all questions, stop and report exactly:

> "I have answered all quiz questions. Please open `AGENT_QUIZ_ANSWERS.md` to grade my answers, or let me know when I may read it to self-grade."

Do not read `AGENT_QUIZ_ANSWERS.md` until explicitly told to compare.


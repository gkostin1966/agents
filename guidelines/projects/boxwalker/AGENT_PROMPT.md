# New Session Startup Prompt — boxwalker

## Prompt Invocation

Copy and paste the line below into a new agent session:

```text
Read AGENT_PROMPT.md and follow the instructions there.
```

## Session Context

You are starting a new session in the `boxwalker` repository, a Ruby on Rails 8
application for archival finding-aid discovery built on ArcLight, Blacklight, and
Solr 9 SolrCloud, using SQLite and Docker Compose for local development.

## Required Developer Input

Use local `.agents` paths first.

- Primary: read guidance from `.agents/` in the project root.
- Fallback only if `.agents/` is missing or unreadable: ask for absolute `AGENTS_ROOT`.

## Startup Workflow

After completing the base startup workflow, infer the active ticket from the branch
name (for example `BW-42/my-feature`) and use it to locate ticket files under `tasks/`.

## Task Files

Read these files from `.agents/`:

- `.agents/tasks/README.md` (task index)
- `.agents/tasks/BW-nnn/STATUS.md` (active ticket state)
- `.agents/tasks/BW-nnn/TODO.md` (active subtasks)

Fallback paths when `.agents/` is unavailable:

- `AGENTS_ROOT/guidelines/projects/boxwalker/tasks/README.md`
- `AGENTS_ROOT/guidelines/projects/boxwalker/tasks/BW-nnn/STATUS.md`
- `AGENTS_ROOT/guidelines/projects/boxwalker/tasks/BW-nnn/TODO.md`

Replace `BW-nnn` using the ticket from the current branch.

## Quiz Gate

Take the onboarding quiz from:

- Primary: `.agents/AGENT_QUIZ.md`
- Fallback: `AGENTS_ROOT/guidelines/projects/boxwalker/AGENT_QUIZ.md`

After answering all questions, stop and report exactly:

> "I have answered all quiz questions. Please open `AGENT_QUIZ_ANSWERS.md` to grade my answers, or let me know when I may read it to self-grade."

Do not read `AGENT_QUIZ_ANSWERS.md` until explicitly told to compare.


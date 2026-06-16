# New Session Startup Prompt — boxrunner

## Prompt Invocation

Copy and paste the line below into a new agent session:

```text
Read AGENT_PROMPT.md and follow the instructions there.
```

## Session Context

You are starting a new session in the `boxrunner` repository, a Ruby on Rails 8
application for archival finding-aid discovery built on ArcLight, Blacklight, and
Solr 9 SolrCloud, using SQLite and Docker Compose for local development.

## Required Developer Input

Use local `.agents` paths first.

All files under `.agents/` are part of the agent-framework project and act as shared
long-term memory for future agents. Maintain them in place as part of normal task
work when they are relevant to the current task, use them to get your work done,
and remember that any `.agents/` changes are committed in the separate
agent-framework project outside this repository instead of as part of normal
app-code commits here.
Agents in this project never commit files under `.agents/`, and developers will not
request agents here to commit `.agents/` files.

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

Session defaults for every new run:

- Detect current git branch and identify the focus ticket key (`ARC-\d+` when present).
- Read `.agents/tasks/README.md`, plus `STATUS.md` and `TODO.md` for the selected ticket.
- State the selected focus ticket in the first substantive reply.
- State workflow context in that reply: application-code work, `.agents` bookkeeping work, or both.
- If you find clear, non-destructive drift between task files (for example `README.md` summary/status mismatch with ticket `STATUS.md`/`TODO.md`), correct it proactively and report it.

After completing the base startup workflow, infer the active ticket from the branch
name by extracting a key that matches `ARC-\d+` (for example `ARC-42/my-feature` ->
`ARC-42`) and use it to locate ticket files under `tasks/`.
If the branch name does not contain an `ARC-\d+` ticket key (for example `main` or
`chore/update-readme`), list currently open tickets from `.agents/tasks/README.md`
and ask the developer which ticket to focus on before proceeding.
If the selected ticket folder does not exist, create `.agents/tasks/ARC-nnn/{TODO.md,STATUS.md,plans/}`
and add a row to `.agents/tasks/README.md` before proceeding.

## Task Files

Read these files from `.agents/`:

- `.agents/tasks/README.md` (task index)
- `.agents/tasks/ARC-nnn/STATUS.md` (active ticket state)
- `.agents/tasks/ARC-nnn/TODO.md` (active subtasks)

Fallback paths when `.agents/` is unavailable:

- `AGENTS_ROOT/guidelines/projects/boxrunner/tasks/README.md`
- `AGENTS_ROOT/guidelines/projects/boxrunner/tasks/ARC-nnn/STATUS.md`
- `AGENTS_ROOT/guidelines/projects/boxrunner/tasks/ARC-nnn/TODO.md`

Replace `ARC-nnn` using the ticket from the current branch.

## Quiz Gate

Take the onboarding quiz from:

- Primary: `.agents/AGENT_QUIZ.md`
- Fallback: `AGENTS_ROOT/guidelines/projects/boxrunner/AGENT_QUIZ.md`

After answering all questions, stop and report exactly:

> "I have answered all quiz questions. Please open `AGENT_QUIZ_ANSWERS.md` to grade my answers, or let me know when I may read it to self-grade."

Do not read `AGENT_QUIZ_ANSWERS.md` until explicitly told to compare.


# New Session Startup Prompt — findingaids-argocd

> **Base prompt applies first**: `guidelines/base/AGENT_PROMPT.md`
> Sections in this file with the same `## Heading` override base startup blocks.

## Prompt Invocation

Copy and paste the line below into a new agent session:

```text
Read AGENT_PROMPT.md and follow the instructions there.
```

## Session Context

You are starting a new session in the `findingaids-argocd` repository, the Kubernetes
and Argo CD configuration repository for the Finding Aids platform.

## Required Developer Input

Before reading framework-managed files, ask for the absolute path to the `agents`
repository root and store it as `AGENTS_ROOT` for this session.

## Startup Workflow

After completing the base startup workflow, read the local `README.md` for architecture,
cluster topology, and repository structure.

## Task Files

Read these files from `AGENTS_ROOT`:

- `guidelines/projects/findingaids-argocd/AGENT_TODO.md` (active work)
- `guidelines/projects/findingaids-argocd/AGENT_DONE.md` (recent completions)

Use the first unchecked subtask in the first task in `AGENT_TODO.md` as the resume point.

## Quiz Gate

Take the onboarding quiz from:

- `AGENTS_ROOT/guidelines/projects/findingaids-argocd/AGENT_QUIZ.md`

After answering all questions, stop and report exactly:

> "I have answered all quiz questions. Please open `AGENT_QUIZ_ANSWERS.md` to grade my answers, or let me know when I may read it to self-grade."

Do not read `AGENT_QUIZ_ANSWERS.md` until explicitly told to compare.

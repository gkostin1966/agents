# AGENTS.md — dspace

Project-specific guidance for `mlibrary/DSpace` mounted as `mounted-projects/dspace`.

## Project Context

| Item          | Value                    |
|---------------|--------------------------|
| Repo          | `mlibrary/DSpace`        |
| Stack         | Java / Maven + Docker    |
| Default branch| verify in git orientation|
| Ticket style  | confirm with developer   |

## Task Files

Use these files for per-project state:

- `.agents/AGENT_TODO.md` (active work)
- `.agents/AGENT_DONE.md` (completed work)
- `.agents/AGENT_QUIZ.md` and `.agents/AGENT_QUIZ_ANSWERS.md` (onboarding gate)

## Quick Session Checklist

- Run startup git orientation commands in `mounted-projects/dspace`.
- Confirm branch and ticket key with the developer before code edits.
- Read `.agents/AGENT_TODO.md` and top entry of `.agents/AGENT_DONE.md`.

## Test Commands

Prefer non-interactive commands:

```shell
./mvnw -q -DskipTests compile | cat
./mvnw -q test | cat
docker compose config | cat
```

## DSpace-Specific Notes

- Keep communication drafts in `communications/` at project root.
- Keep framework memory files in `.agents/` only.
- If introducing slower integration test commands, record exact invocation in `.agents/AGENT_TODO.md` first.


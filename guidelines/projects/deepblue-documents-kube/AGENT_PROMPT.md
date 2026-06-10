# New Session Startup Prompt — deepblue-documents-kube

## Prompt Invocation

Copy and paste the line below into a new agent session:

```text
Read AGENT_PROMPT.md and follow the instructions there.
```

## Session Context

You are starting a new session in the `deepblue-documents-kube` repository, a Kubernetes
GitOps configuration repository for Deep Blue Documents. It uses Tanka (Jsonnet) and Argo CD
to manage DSpace deployment state.

## Required Developer Input

Use local `.agents` paths first.

- Primary: read guidance from `.agents/` in the project root.
- Fallback only if `.agents/` is missing or unreadable: ask for absolute `AGENTS_ROOT`.

## Startup Workflow

After completing the base startup workflow, also read `README.md` in this repository for
cluster topology and operational context before changing files.

## Task Files

Read these files from `AGENTS_ROOT`:

- `guidelines/projects/deepblue-documents-kube/AGENT_TODO.md` (active work)
- `guidelines/projects/deepblue-documents-kube/AGENT_DONE.md` (recent completions)

Use the first unchecked subtask in the first task in `AGENT_TODO.md` as the resume point.

## Quiz Gate

Take the onboarding quiz from:

- `.agents/AGENT_QUIZ.md`

After answering all questions, stop and report exactly:

> "I have answered all quiz questions. Please open `AGENT_QUIZ_ANSWERS.md` to grade my answers, or let me know when I may read it to self-grade."

Do not read `AGENT_QUIZ_ANSWERS.md` until explicitly told to compare.

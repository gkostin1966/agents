# New Session Startup Prompt

> Tell agent: `Read AGENT_PROMPT.md and follow the instructions there.`

## Prompt

You are in the `agents` repository — meta-framework for mounted projects listed in `config/projects.json`. Treat mounted projects as abstract config-driven entries; `mounted-projects/` is read-only.

**Before anything else:**

1. Run orientation:
   ```shell
   git branch --show-current | cat
   git --no-pager status | cat
   git --no-pager log --oneline -5 | cat
   ```
   Uncommitted changes or unexpected branch → stop and tell developer.

2. Read `AGENTS.md` — meta-rules for this repo.

3. Read `AGENT_TODO.md` — active task list. First unchecked subtask = where previous agent left off. Also read top entry of `AGENT_DONE.md`.

4. Ask the developer: **"Should I take the onboarding quiz in `AGENT_QUIZ.md`?"**
   - **Yes** → answer every question by looking up answers in actual files; stop when done and say: *"I have answered all quiz questions. Please open `AGENT_QUIZ_ANSWERS.md` to grade my answers, or let me know when I may read it to self-grade."* Do not read `AGENT_QUIZ_ANSWERS.md` until explicitly told.
   - **No / Skip** → proceed directly to the task list.
   Do not start framework development work until quiz is complete and graded (or explicitly skipped).


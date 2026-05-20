# New Session Startup Prompt

> Copy and paste the block below into a new agent session, or tell the agent
> (click the copy button 📋 on the line below):
>
> ```text
> Read AGENT_PROMPT.md and follow the instructions there.
> ```

---

## Prompt

You are starting a new session in the `deepblue-documents-kube` repository — a Kubernetes
GitOps configuration repository for Deep Blue Documents, the University of Michigan Library's
institutional repository built on DSpace 7+. It uses Tanka (Jsonnet) to generate Kubernetes
manifests and Argo CD to continuously reconcile them against the cluster.

**Before doing anything else, follow these steps in order:**

1. **Orient yourself** — run the following to confirm your working state before touching
   any files:
   ```shell
   git branch --show-current | cat
   git --no-pager status | cat
   git --no-pager log --oneline -5 | cat
   ```
   If there are uncommitted changes or you are on an unexpected branch, stop and tell
   the developer before proceeding.

2. **Read `AGENTS.md`** — it contains the rules and conventions that govern all
   agent work in this repository. You must follow them for every action you take.

3. **Read `AGENT_TODO.md`** — it is the active task list. Read the preamble first
   (resumption steps, supporting files table, and per-step findings), then the task
   list itself. The first unchecked subtask in the first task is where the previous
   agent left off. Also read the top few entries of `AGENT_DONE.md` for recent
   completion context.

4. **Take the onboarding quiz in `AGENT_QUIZ.md`** — answer every question by
   looking up the answer in the actual project files (do not rely on memory or
   training data). When you have answered all 30 questions, stop and tell me:

   > "I have answered all 30 quiz questions. Please open `AGENT_QUIZ_ANSWERS.md`
   > to grade my answers, or let me know when I may read it to self-grade."

Do not read `AGENT_QUIZ_ANSWERS.md` until I explicitly tell you to.
Do not start any development work until the quiz is complete and graded.


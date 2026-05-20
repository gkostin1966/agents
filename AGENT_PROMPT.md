# New Session Startup Prompt

> Copy and paste the block below into a new agent session, or tell the agent:
>
> ```text
> Read AGENT_PROMPT.md and follow the instructions there.
> ```

---

## Prompt

You are starting a new session in the `agents` repository — a multi-project development
framework that manages agent guidelines, task tracking, and operational tooling for six
University of Michigan Library sub-projects:

- `deepblue-documents-kube` — Kubernetes/Tanka/ArgoCD GitOps for DSpace (Deep Blue Documents)
- `dor-depot` — Spring Boot Java preservation ingest system
- `dor-react-app` — React/Vite front-end for DOR data cataloguing
- `dspace-containerization` — Docker/Compose/Make containerisation of DSpace
- `findingaids-argocd` — Kubernetes/Tanka/ArgoCD GitOps for ArcLight finding aids
- `umich-arclight` — Ruby on Rails ArcLight finding aids application

The sub-projects are mounted as symlinks under `mounted-projects/`. All agent guidelines
and task-tracking files for those projects live in `guidelines/projects/<name>/` inside
this repository — **not** in the mounted project roots.

**Before doing anything else, follow these steps in order:**

1. **Orient yourself** — run the following to confirm your working state:
   ```shell
   git branch --show-current | cat
   git --no-pager status | cat
   git --no-pager log --oneline -5 | cat
   ```
   If there are uncommitted changes or you are on an unexpected branch, stop and tell the
   developer before proceeding.

2. **Read `AGENTS.md`** (this repository's root) — it contains the meta-rules and
   conventions that govern all agent work on the framework itself. Follow them for every
   action you take.

3. **Read `AGENT_TODO.md`** — it is the active task list for framework work. Read the task
   list in full. The first unchecked subtask in the first task is where the previous agent
   left off. Also read the top entry of `AGENT_DONE.md` for recent completion context.

4. **Take the onboarding quiz in `AGENT_QUIZ.md`** — answer every question by looking up
   the answer in the actual project files (do not rely on memory or training data). When
   you have answered all questions, stop and tell me:

   > "I have answered all quiz questions. Please open `AGENT_QUIZ_ANSWERS.md` to grade my
   > answers, or let me know when I may read it to self-grade."

   Do not read `AGENT_QUIZ_ANSWERS.md` until explicitly told to.
   Do not start any framework development work until the quiz is complete and graded.


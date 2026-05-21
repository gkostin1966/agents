# Agent Onboarding Quiz — deepblue-documents-kube

> 🚫 **DO NOT read `AGENT_QUIZ_ANSWERS.md`** until you have written out answers to all
> 30 questions below and the developer has told you to compare. Reading the answer file
> first defeats the purpose of the quiz.
>
> **Instructions for the quiz-taker (agent):**
> Answer every question by looking it up in the actual project files — do not rely on
> memory or training data. Each question includes a hint pointing to the authoritative
> source. Write your answers in your response, then stop and prompt the developer
> (see the instruction after Q30).
>
> **Instructions for the quiz-giver (developer):**
> Run this quiz at the start of a new agent session to confirm the agent has read and
> understood the project state before it begins work. When the agent prompts you after
> Q30, open `AGENT_QUIZ_ANSWERS.md` and grade the answers yourself, or ask the agent
> to read that file and self-grade at that point.

---

## Section 1 — Ground Rules (AGENTS.md)

**Q1.** You are about to start a multi-step task. What must you do *before* executing
the first step?

*(Hint: `AGENTS.md` § Task Tracking)*

---

**Q2.** You need to reorder two tasks in `AGENT_TODO.md`. What tool must you use, and what
tool must you **never** use for this operation?

*(Hint: `AGENTS.md` § Reordering Tasks)*

---

**Q3.** You have made a commit locally. ArgoCD is not reflecting your change.
What should you check first before concluding the cluster is out of date?
Also: you want to apply a Tanka change immediately without waiting for a push — what
command would do that, and are you allowed to run it without explicit developer approval?
Name two `kubectl` sub-commands that are always safe to run without approval and two that
require explicit developer approval before running.

*(Hint: `AGENTS.md` § ArgoCD and the Remote `main` Branch; § Destructive `kubectl` and `tk apply` commands)*

---

**Q4.** The developer asks you to amend the most recent commit to include a small fix.
What should you do instead? Also describe the branch strategy for this project: what branch
does the developer typically work on, when (if ever) should you create a feature branch,
and what must you never do regarding `git push`?

*(Hint: `AGENTS.md` § Branch Strategy and § Git Commits)*

---

## Section 2 — Configuration Model

**Q5.** Name all active configuration layers for the backend pod in all three
environments, in priority order (lowest to highest). Include any special-purpose
file-injection mechanisms that operate outside the env-var override chain.

*(Hint: `environments/deepblue-documents/configuration/README.md` § Configuration Layers
and § Current Deployment State; `CLASSIFY.md` § Layer 3c)*

---

**Q6.** A developer asks you to change `mail.from.address`. Which file should you
edit, and which now-retired mechanism would have been the *wrong* answer before April 2026?

*(Hint: `environments/deepblue-documents/configuration/README.md` § Decision guide;
`lib/deepblue-backend-cm.jsonnet` — note that Bucket A properties common to all environments
live in the shared lib, not in each environment's `backend-cm.jsonnet`)*

---

**Q7.** Where does the `dspace-secrets` Secret inject its values into the backend pod?
Name the Jsonnet field and the file that defines it.

*(Hint: `lib/deepblue-documents.libsonnet` lines ~380–392)*

---

**Q8.** The `local-cfg` Secret was retired. What investigation finding caused this retirement,
and when did it happen?

*(Hint: `environments/deepblue-documents/configuration/README.md` § Working with `local.cfg`)*

---

**Q9.** Does the **demo** environment set `handle.prefix` in its ConfigMap?
Does **production**? What is the upstream DSpace default for this property?

*(Hint: `environments/deepblue-documents/demo/backend-cm.jsonnet`;
`environments/deepblue-documents/production/backend-cm.jsonnet`;
`environments/deepblue-documents/configuration/CLASSIFY.md` Bucket E)*

---

## Section 3 — Active Work and Task Priorities

**Q10.** List all tasks currently in `AGENT_TODO.md` in order of priority, and classify each
as: (a) immediately actionable, (b) needs team confirmation, or (c) blocked on HITS.

*(Hint: `AGENT_TODO.md`)*

---

**Q11.** What is the **single most immediately actionable** coding task (no external
dependencies, no team confirmation needed, just a code edit)?
Describe the exact change in one sentence.

*(Hint: `AGENT_TODO.md` CronJob Stabilisation — Phase 2;
`environments/deepblue-documents/demo/cronjobs.jsonnet` or the production equivalent)*

---

**Q12.** For the DEEPBLUE-466 DEMO task, three files are ready to hand off to HITS.
Name all three and where they live.

*(Hint: `AGENT_TODO.md` DEEPBLUE-466 DEMO task; `environments/deepblue-documents/configuration/crosswalks/`)*

---

**Q13.** What is the production Elements service account email used for the RT2 connection,
and where is this documented?

*(Hint: `plans/PLAN466.md` Step 1 status note; `environments/deepblue-documents/configuration/DSPACE_ADMIN.md`)*

---

## Section 4 — Source of Truth Spot-Checks

**Q14.** What is the current `image_tag_app` SHA in `lib/deepblue-documents.libsonnet`?
Give the full SHA (not truncated).

*(Hint: `lib/deepblue-documents.libsonnet` — look in the `_config` block near the top of the file)*

---

**Q15.** The production `backend-cm.jsonnet` has multiple TODO comments about placeholder
values that must be replaced before certain features can be used. Name **two** such
placeholders — one that affects live production behaviour today, and one that only matters
when a currently-commented-out feature is re-enabled. For each, name the property and the
task in `AGENT_TODO.md` that tracks the fix.

*(Hint: `environments/deepblue-documents/production/backend-cm.jsonnet` — scan for TODO comments; `AGENT_TODO.md`)*

---

**Q16.** Which environments deploy an `express` service and an `oauth2-proxy`?
Does demo have them?

*(Hint: `environments/deepblue-documents/production/main.jsonnet`;
`environments/deepblue-documents/workshop/main.jsonnet`;
`environments/deepblue-documents/demo/main.jsonnet`)*

---

**Q17.** What cluster does the demo environment run on, and what namespace does it use?

*(Hint: `environments/deepblue-documents/demo/spec.json` or
`environments/deepblue-documents/configuration/README.md` § Environment Reference)*

---

**Q18.** The three `cronjob-*.libsonnet` files intentionally do **not** mount a specific
PVC that the backend Deployment does mount. Which PVC, and why was it removed?

*(Hint: `plans/PLANCRONJOBS.md` § Issue A; `lib/cronjob-production.libsonnet` comment)*

---

## Section 5 — Documentation Hygiene

**Q19.** After editing a Markdown file that contains tables, what two commands should you
run before committing, in order?

*(Hint: `AGENTS.md` § Markdown Formatting)*

---

**Q20.** A task in `AGENT_TODO.md` has all subtasks checked off including the developer-verification
subtask. What are the **two** steps required to archive it, and what file does it move to?

*(Hint: `AGENTS.md` § Task Tracking)*

---

## Section 6 — Configuration Encoding, CronJobs, and Architecture

**Q21.** In the backend ConfigMap files (`backend-cm.jsonnet`), DSpace property names are
encoded as environment variable keys using a special convention. What does `__P__` encode,
what does `__D__` encode, and how is a literal underscore (`_`) in a property name encoded?
Give one example of a property that uses **both** `__P__` and `__D__` in its key.

*(Hint: `AGENTS.md` § ConfigMap Key Encoding; `environments/deepblue-documents/production/backend-cm.jsonnet`
— look for any key with both dots and hyphens in the DSpace property name)*

---

**Q22.** CronJob email reports are currently **not delivered in any environment**, including
production. What is the root cause, and what is the preferred fix?

*(Hint: `plans/PLANCRONJOBS.md` § Issue B)*

---

**Q23.** The `cronjob-*.libsonnet` files explicitly override `JAVA_OPTS`. What is the
image's built-in default value, why is it dangerous in a CronJob pod without a container
resource limit, and what value does the **production** CronJob lib set it to?

*(Hint: `lib/cronjob-production.libsonnet` — look at the `env` block and the comment above it)*

---

**Q24.** There is a `db-backup` CronJob in workshop and production that is fundamentally
different from `index-discovery` and `index-oai`. What container image does it use,
where does it write backups, and how do the production and workshop schedules differ?

*(Hint: `environments/deepblue-documents/workshop/cronjob_db_backup.libsonnet`;
`environments/deepblue-documents/production/production_cronjob_db_backup.libsonnet`)*

---

**Q25.** `lib/deepblue-frontend-cm.jsonnet` defines almost all frontend environment
variables. What is the **only** key that each environment's `frontend-cm.jsonnet` adds?
And what is a common misconception about the `DSPACE_UI_HOST` key set in the shared lib?

*(Hint: `lib/deepblue-frontend-cm.jsonnet`; `environments/deepblue-documents/production/frontend-cm.jsonnet`)*

---

**Q26.** Workshop's `backend-cm.jsonnet` sets `filestorage__P__dir` to `/mnt/prod-assetstore`.
What does this mean architecturally — what data does workshop read from there, in what
access mode is it mounted, and is workshop's database independent of production's?

*(Hint: `environments/deepblue-documents/workshop/backend-cm.jsonnet`;
`environments/deepblue-documents/configuration/README.md` § Environment Reference note)*

---

**Q27.** `CLASSIFY.md` ends with a list of open questions about production configuration.
Name at least **two** unresolved open questions and explain why each matters operationally.

*(Hint: `environments/deepblue-documents/configuration/CLASSIFY.md` § Open Questions)*

---

**Q28.** Production is on a completely separate Kubernetes cluster from workshop and demo.
What are the two `kubectl` context names, which namespaces does each context manage, and
what is the mandatory rule before running any `kubectl` command when switching between
a production investigation and a workshop/demo investigation?

*(Hint: `AGENTS.md`  Kubernetes Cluster Topology)*

---

**Q29.** When the developer asks you to compose an email to an external party (e.g., ITS
or HITS), what file format do you use, where do you save it, is it tracked in git, and
what structural elements must the draft include?

*(Hint: `AGENTS.md` § Email Drafts for Third Parties)*

---

**Q30.** You need to run a short Python snippet to inspect some data. Your first instinct
is to write `python3 -c "..."`. What is wrong with that approach in this environment, when
does it go wrong specifically, what is the universal fix, and when (if ever) is the
single-line `-c` form safe to use?

*(Hint: `AGENTS.md` § Command-Line Tool Usage)*

---

## When You Have Answered All 30 Questions

Stop here. Do **not** open `AGENT_QUIZ_ANSWERS.md`.

Tell the developer:

> "I have answered all 30 quiz questions. Please open `AGENT_QUIZ_ANSWERS.md` to grade
> my answers, or let me know when I may read it to self-grade."

Wait for the developer's instruction before proceeding.

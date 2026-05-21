# Agent Onboarding Quiz — findingaids-argocd

> 🚫 **DO NOT read `AGENT_QUIZ_ANSWERS.md`** until you have written out answers to all
> questions below and the developer has told you to compare. Reading the answer file
> first defeats the purpose of the quiz.
>
> **Instructions for the quiz-taker (agent):**
> Answer every question by looking it up in the actual project files — do not rely on
> memory or training data. Each question includes a hint pointing to the authoritative
> source. Write your answers in your response, then stop and prompt the developer
> (see the instruction at the end).
>
> **Instructions for the quiz-giver (developer):**
> Run this quiz at the start of a new agent session to confirm the agent has read and
> understood the project state before it begins work. When the agent prompts you after
> the final question, open `AGENT_QUIZ_ANSWERS.md` and grade the answers yourself, or
> ask the agent to read that file and self-grade at that point.

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

*(Hint: `AGENTS.md` § ArgoCD and the Remote `main` Branch)*

---

**Q4.** The developer asks you to amend the most recent commit to include a small fix.
What should you do instead?

*(Hint: `AGENTS.md` § Git Commits)*

---

## Section 2 — Cluster Topology and Environments

**Q5.** This project uses three separate Kubernetes clusters. List all three kubectl
context names, the API server hostname for each, and which application namespaces
each context manages.

*(Hint: `AGENTS.md` § Kubernetes Cluster Topology; `environments/clusters/*/spec.json`;
`environments/findingaids/*/spec.json`)*

---

**Q6.** Which environments deploy an `oauth2-proxy` to gate access with U-M WebLogin?
Which one does **not** use oauth2-proxy? Where in the Jsonnet code is this defined?

*(Hint: `environments/findingaids/*/main.jsonnet`)*

---

**Q7.** What is the purpose of the `admin` environment/namespace, and what container
image does it run? Which cluster does it live on?

*(Hint: `environments/findingaids/admin/main.jsonnet`; `environments/findingaids/admin/spec.json`)*

---

**Q8.** The `preview` environment runs on the production cluster but uses an
oauth2-proxy. How does its auth-url differ from the one used in `staging` and
`testing`? Why?

*(Hint: `environments/findingaids/preview/main.jsonnet`;
`environments/findingaids/staging/main.jsonnet`)*

---

## Section 3 — Architecture and Infrastructure

**Q9.** List all Kubernetes resources of every type (Deployments, Services, CronJobs,
ConfigMaps, PersistentVolumeClaims, etc.) that `lib/arclight.libsonnet` defines for a
standard Finding Aids instance. For each, give its name, kind, and role in one sentence.

*(Hint: `lib/arclight.libsonnet` — read the whole file, not just the Deployment blocks)*

---

**Q10.** Where does EAD data live, and how is it accessed by the `app` and `resque`
containers? Give the NFS server hostname, the NFS export path, and the container
mount path.

*(Hint: `lib/arclight.libsonnet` — look for `nfs:` and `volumeMounts`)*

---

**Q11.** How does the Solr connection work? What Kubernetes resource type is used,
what is the `externalName` it points to, and which Secret provides the credentials?

*(Hint: `lib/arclight.libsonnet` — the `solr:` section; `environments/findingaids/staging/main.jsonnet`)*

---

**Q12.** What is the `haproxy-cloudflare` component, where does its configuration
come from, and why does the app Ingress route through it rather than directly to
the `app` Service?

*(Hint: `lib/arclight.libsonnet` — `haproxy:` section and `ingress:` section;
`lib/cloudflare/`)*

---

**Q13.** The `prune-searches` CronJob runs on what schedule, and what command does
it execute? Which image does it use?

*(Hint: `lib/arclight.libsonnet` — `db.prune_searches_job`)*

---

## Section 4 — Configuration and Image Tags

**Q14.** What is the current production image tag (full SHA) and where is it set?
Is this value also used by staging and testing?

*(Hint: `lib/release.libsonnet`; `environments/findingaids/staging/main.jsonnet`)*

---

**Q15.** The production environment sets custom `app_resources` limits and requests.
What are the CPU and memory limits for the `app` container in production?
How do they differ from the defaults in `lib/arclight.libsonnet`?

*(Hint: `environments/findingaids/production/main.jsonnet`;
`lib/arclight.libsonnet` — `_config`)*

---

**Q16.** Which environments set `FINDING_AID_INGEST: true`, and what is this
environment variable used for?

*(Hint: `environments/findingaids/*/main.jsonnet`)*

---

**Q17.** Production sets `db_pool: 40` and `RAILS_MAX_THREADS: 40`. What is the
default `db_pool` in `lib/arclight.libsonnet`? Why do these two values typically
need to match?

*(Hint: `environments/findingaids/production/main.jsonnet`;
`lib/arclight.libsonnet` — `_config.db_pool` and the `DATABASE_URL` construction)*

---

## Section 5 — Documentation Hygiene

**Q18.** After editing a Markdown file that contains tables, what two commands should
you run before committing, in order?

*(Hint: `AGENTS.md` § Markdown Formatting)*

---

**Q19.** A task in `AGENT_TODO.md` has all subtasks checked off including the
developer-verification subtask. What are the **two** steps required to archive it,
and what file does it move to?

*(Hint: `AGENTS.md` § Task Tracking)*

---

**Q20.** When the developer asks you to compose an email to an external party (e.g.,
ITS or a vendor), what file format do you use, where do you save it, and is it
tracked in git?

*(Hint: `AGENTS.md` § Email Drafts for Third Parties)*

---

## Section 6 — Active Work and Task State

**Q21.** What tasks are currently in `AGENT_TODO.md`? For each task, is it immediately
actionable, awaiting developer input, or blocked on a third party?

*(Hint: `AGENT_TODO.md`)*

---

**Q22.** You need to run a short Python snippet to inspect some data. Your first
instinct is to write `python3 -c "..."`. What is wrong with that approach in this
environment, when does it go wrong specifically, what is the universal fix, and
when (if ever) is the single-line `-c` form safe to use?

*(Hint: `AGENTS.md` § Command-Line Tool Usage)*

---

**Q23.** The `README.md` has an **Active Work** table. When you check off a subtask
in `AGENT_TODO.md`, what must you also update in `README.md`?

*(Hint: `AGENTS.md` § Keeping `README.md` in Sync)*

---

## When You Have Answered All Questions

Stop here. Do **not** open `AGENT_QUIZ_ANSWERS.md`.

Tell the developer:

> "I have answered all quiz questions. Please open `AGENT_QUIZ_ANSWERS.md` to grade
> my answers, or let me know when I may read it to self-grade."

Wait for the developer's instruction before proceeding.

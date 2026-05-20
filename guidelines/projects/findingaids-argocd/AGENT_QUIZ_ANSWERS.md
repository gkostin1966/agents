# Agent Onboarding Quiz — Answer Key

> ⚠️ **DO NOT READ THIS FILE** until you have answered all questions in
> `AGENT_QUIZ.md` and the developer has told you to compare your answers.
> Reading this file before completing the quiz defeats its purpose.

---

> Every answer below can be verified by reading the cited source file.
> If an answer here contradicts what you find in the source, **the source file wins**.

---

**A1.** Add the plan to `AGENT_TODO.md` as a new task with subtasks before taking any action.
Do not begin execution until the plan is recorded.
*(Source: `AGENTS.md` § Task Tracking — "Before executing any multi-step plan, add it to `AGENT_TODO.md` first")*

---

**A2.** Always use **Python** (`re.split` on `## ` headings, reorder list, rewrite file).
Never use **string-search-and-replace** — task bodies contain URLs and UUIDs that make
patterns brittle and prone to corrupting the file.
*(Source: `AGENTS.md` § Reordering Tasks in `AGENT_TODO.md`)*

---

**A3.** Check for unpushed local commits: `git --no-pager log --oneline origin/main..HEAD`.
ArgoCD only syncs from `origin/main`, not from local commits.
*(Source: `AGENTS.md` § ArgoCD and the Remote `main` Branch)*

---

**A4.** Create a **new commit** on top of HEAD with `git commit`. Never use `git commit --amend`.
The developer will squash commits manually as needed.
*(Source: `AGENTS.md` § Git Commits)*

---

**A5.** There are three clusters:

| kubectl context name     | API server hostname                            | Application namespaces  |
|--------------------------|------------------------------------------------|-------------------------|
| `findingaids-production` | `production.cluster.findingaids.lib.umich.edu` | `production`, `preview` |
| `findingaids-staging`    | `staging.cluster.findingaids.lib.umich.edu`    | `staging`               |
| `findingaids-workshop`   | `workshop.cluster.findingaids.lib.umich.edu`   | `testing`, `admin`      |

Each cluster also has an `argocd` namespace for ArgoCD itself.
*(Source: `AGENTS.md` § Kubernetes Cluster Topology; `environments/clusters/*/spec.json`;
`environments/findingaids/*/spec.json`)*

---

**A6.** `staging`, `testing`, and `preview` all deploy an `oauth2-proxy` (via
`$.oauth.proxy(...)` in their `main.jsonnet`). **`production`** does **not** use oauth2-proxy
— it is publicly accessible. **`admin`** also does not use oauth2-proxy (it is a workstation
pod, not a web-facing service).

The oauth2-proxy is defined in each environment's `main.jsonnet` as the `oauth2_proxy:` top-level
field calling `$.oauth.proxy(namespace=..., hostname=..., proxy_config=...)`.
*(Source: `environments/findingaids/staging/main.jsonnet`;
`environments/findingaids/testing/main.jsonnet`;
`environments/findingaids/preview/main.jsonnet`;
`environments/findingaids/production/main.jsonnet`)*

---

**A7.** The `admin` namespace contains a single Deployment running `ruby:3.1` with a
`sleep infinity` command and access to the NFS share at
`ulib-arclight-data.value.storage.umich.edu`. It is used for **administrative operations
on EAD data** (e.g. file management, bulk ingests) without going through the web application.
It runs on the **workshop cluster** (`workshop.cluster.findingaids.lib.umich.edu`,
kubectl context `findingaids-workshop`).
*(Source: `environments/findingaids/admin/main.jsonnet`;
`environments/findingaids/admin/spec.json`)*

---

**A8.** `staging` and `testing` use a standard path-based oauth2-proxy auth-url:
```
nginx.ingress.kubernetes.io/auth-url: 'https://$host/oauth2/auth'
nginx.ingress.kubernetes.io/auth-signin: 'https://$host/oauth2/start?rd=...'
```

`preview` uses a **vcluster-scoped service URL**:
```
nginx.ingress.kubernetes.io/auth-url: 'http://oauth2-proxy-x-preview-x-vcluster.arclight-production.svc.cluster.local:4180/oauth2/auth'
```

The reason: `preview` runs inside the production vcluster where the ingress controller
cannot follow the host-based redirect route. Instead it references the oauth2-proxy Service
directly by its cluster-internal DNS name, bypassing the public ingress for the auth check.
*(Source: `environments/findingaids/preview/main.jsonnet` vs
`environments/findingaids/staging/main.jsonnet`)*

---

**A9.** `lib/arclight.libsonnet` defines all of the following Kubernetes resources for a standard instance:

| Workload                        | Role                                                                  |
|---------------------------------|-----------------------------------------------------------------------|
| `app` Deployment                | Rails/ArcLight web server (puma), serves the public-facing web UI     |
| `app` Service                   | ClusterIP service exposing ports 3000 (HTTP) and 9394 (Prometheus)    |
| `app` Ingress                   | TLS ingress (cert-manager), routes through haproxy-cloudflare sidecar |
| `resque` Deployment             | Background job workers (EAD indexing, record deletion)                |
| `resque` Service                | ClusterIP service exposing port 9394 (Prometheus metrics)             |
| `resque-web` Deployment         | Resque monitoring UI on port 8080                                     |
| `resque-web` Service            | ClusterIP service for the Resque web UI                               |
| `db` Deployment                 | PostgreSQL 12-alpine database (per-environment, not shared)           |
| `db` Service                    | ClusterIP service exposing port 5432                                  |
| `db` PVC                        | `ReadWriteOnce` 5Gi PVC for PostgreSQL data                           |
| `redis` Deployment              | Redis job queue backend                                               |
| `redis` Service                 | ClusterIP service exposing port 6379                                  |
| `haproxy-cloudflare` Deployment | HAProxy sidecar filtering inbound traffic to Cloudflare IPs           |
| `haproxy-cloudflare` Service    | ClusterIP service on port 8080 (Ingress backend target)               |
| `haproxy-cloudflare` ConfigMap  | HAProxy config + Cloudflare IP allowlist                              |
| `prune-searches` CronJob        | Weekly job to purge old Blacklight saved searches from the DB         |
| Namespace                       | Kubernetes namespace with pod-security labels                         |
| LimitRange                      | Default container CPU/memory requests and limits                      |

*(Source: `lib/arclight.libsonnet`)*

---

**A10.** EAD data lives on an NFS share:
- **NFS server**: `ulib-arclight-data.value.storage.umich.edu`
- **NFS export path**: `/ulib-arclight-data`
- **Container mount path**: `/opt/app-data`
- **SubPath**: `volumes/<instance_name>` (so each environment has its own subdirectory
  within the shared NFS export, e.g. `volumes/production`, `volumes/staging`)

The `app` and `resque` containers both mount this NFS volume.
*(Source: `lib/arclight.libsonnet` — `app.deployment` and `resque.deployment` `volumeMounts`)*

---

**A11.** Solr connectivity:
- **Kubernetes resource type**: `Service` of type `ExternalName`
- **`externalName`**: `solr-solrcloud-common.solr.svc.cluster.local`
  (the shared SolrCloud headless service in the `solr` namespace, managed by the Solr operator)
- **Credentials**: the `solr-auth` Secret, referenced via `envFrom.secretRef` in the
  `app` and `resque` containers. It populates `SOLR_USER` and `SOLR_PASSWORD`, which are
  interpolated into the `SOLR_URL` environment variable.

*(Source: `lib/arclight.libsonnet` — `solr.service`; `app_env.envFrom`;
`environments/findingaids/staging/main.jsonnet` — `solr_creds` field)*

---

**A12.** `haproxy-cloudflare` is an HAProxy instance running as a sidecar Deployment in
each environment namespace. It only allows traffic originating from Cloudflare's published
IP ranges (loaded from `lib/cloudflare/ips-v4.txt`). The configuration is stored in a
ConfigMap (`haproxy-cloudflare`) populated from `lib/cloudflare/haproxy.cfg`.

The app Ingress routes to `haproxy-cloudflare:8080` (not `app:3000`) so that all
inbound traffic passes through the IP allowlist filter before reaching the Rails server.
This prevents direct-to-origin attacks that bypass Cloudflare's WAF and DDoS protection.
*(Source: `lib/arclight.libsonnet` — `haproxy.deployment`, `haproxy.config`, `app.ingress`)*

---

**A13.** The `prune-searches` CronJob:
- **Schedule**: `0 4 * * 0` — Sundays at 04:00
- **Command**: `bundle exec rake blacklight:delete_old_searches[7]`
  (deletes Blacklight saved searches older than 7 days)
- **Image**: same as the `app` image (the ArcLight application image for that environment)

*(Source: `lib/arclight.libsonnet` — `db.prune_searches_job`)*

---

**A14.** The current production image tag is `20eee1b1611a55181a6d39fa1a3f5e219ad8e34b`
(a full Git SHA), set in **`lib/release.libsonnet`** as `_config.app_image.tag`.

`staging` and `testing` do **not** import `release.libsonnet` — they set
`app_image.tag` directly in their own `main.jsonnet` (currently also set to
`20eee1b1611a55181a6d39fa1a3f5e219ad8e34b`, but this changes independently of the
production release).
*(Source: `lib/release.libsonnet`; `environments/findingaids/staging/main.jsonnet`)*

---

**A15.** Production `app` container resource limits:
- **CPU limit**: `3000m` (3 cores)
- **Memory limit**: `4Gi`

Defaults in `lib/arclight.libsonnet`:
- **CPU limit**: `1000m` (1 core)
- **Memory limit**: `2Gi`

Production also overrides requests: `cpu: 100m`, `memory: 500Mi` (same as defaults).
*(Source: `environments/findingaids/production/main.jsonnet` — `app_resources`;
`lib/arclight.libsonnet` — `_config.app_resources`)*

---

**A16.** `FINDING_AID_INGEST: true` is set in:
- **`staging`** (`environments/findingaids/staging/main.jsonnet`)
- **`testing`** (`environments/findingaids/testing/main.jsonnet`)
- **`preview`** (`environments/findingaids/preview/main.jsonnet`)

**`production`** does **not** set it (production EAD ingests happen differently).
The environment variable enables EAD file upload functionality in the web UI;
without it the upload endpoint is disabled.
*(Source: `environments/findingaids/*/main.jsonnet` — `env_additions` blocks)*

---

**A17.** The default `db_pool` in `lib/arclight.libsonnet` is **`20`**.
Production overrides it to **`40`** and also sets `RAILS_MAX_THREADS: 40`.

These values must match because Rails (Puma) uses one database connection per thread.
With 40 threads, each puma process needs up to 40 connections from the pool. If
`db_pool` is lower than `RAILS_MAX_THREADS`, threads will block waiting for a free
connection under load, degrading response times.
*(Source: `lib/arclight.libsonnet` — `_config.db_pool` and `DATABASE_URL` string using `config.db_pool`;
`environments/findingaids/production/main.jsonnet` — `db_pool: 40`)*

---

**A18.**
1. `python3 dotpy/format_table.py <file.md>` — rewrites the file with all tables correctly padded
2. `python3 dotpy/check_tables.py <file.md>` — exits 0 if all tables are consistent, 1 with errors

*(Source: `AGENTS.md` § Markdown Formatting)*

---

**A19.**
1. **Remove** the task block from `AGENT_TODO.md`
2. **Prepend** it to `AGENT_DONE.md` (insert after the `# DONE` heading, before existing entries)
   with an ISO 8601 timestamp and a brief summary

The archived task moves to **`AGENT_DONE.md`**.
*(Source: `AGENTS.md` § Task Tracking — "Only when all subtasks are done, move the whole task to `AGENT_DONE.md`")*

---

**A20.** Use **Rich Text Format (`.rtf`)**.
Save the file as **`emails/<short-descriptive-name>.rtf`** inside the `emails/` directory.
The `emails/` directory **is tracked in git** — files remain until the developer removes them.
*(Source: `AGENTS.md` § Email Drafts for Third Parties)*

---

**A21.** ⚠️ **This answer is inherently dynamic** — the task list changes as work
progresses and this answer key will always lag behind the live file.

**Grading instruction:** Compare the agent's answer directly against the current
`AGENT_TODO.md`, not against the snapshot below. Award full marks if the agent:
- Correctly names every task currently in `AGENT_TODO.md`
- Accurately describes each task's status (in progress, awaiting developer input,
  blocked on a third party, etc.)
- Does not invent tasks that are not in the file

**Snapshot at last answer-key update** *(for reference only — do not use to grade)*:

| Task                                            | Status                          |
|-------------------------------------------------|---------------------------------|
| Tailor Copied Agent Files to findingaids-argocd | Awaiting developer verification |
| Audit Documentation Against Source Files        | In progress                     |

*(Source: `AGENT_TODO.md` — always read the live file when grading)*

---

**A22.** `python3 -c "..."` fails in zsh whenever the code spans multiple lines or
contains inner quotes. zsh treats the unclosed double-quote as the start of a heredoc
(`dquote>` prompt), corrupts the command, and can hang the terminal session.

**The universal fix — write to a file, run the file:**
1. Use `insert_edit_into_file` or `create_file` to write the code to a file:
   - Reusable script → `dotpy/myscript.py`
   - Truly one-off → `/tmp/run.py`
2. Run it: `python3 dotpy/myscript.py | cat`

**The single-line `-c` form is safe only when:**
- The entire command fits on one line, **and**
- It contains no inner quotes (single or double), **and**
- It contains no `$` expansions or backticks

Example of a safe one-liner: `python3 -c "print(42)" | cat`
*(Source: `AGENTS.md` § Command-Line Tool Usage)*

---

**A23.** When a subtask is checked off, update the `Status` cell in the **Active Work**
table in `README.md` (e.g., change "Steps 2–10 remaining" to "Steps 3–10 remaining").
Also add a bullet to the matching "Findings from Step N" block (if one exists) summarising
what was done.
*(Source: `AGENTS.md` § Keeping `README.md` in Sync)*

---

## Scoring

| Score      | Verdict                                                                            |
|------------|------------------------------------------------------------------------------------|
| 23 / 23    | ✅ Ready to work — agent understands the current project state                      |
| 19–22 / 23 | ⚠️ Review the missed questions before starting work                                |
| < 19 / 23  | 🛑 Re-read `AGENTS.md`, `README.md`, and `lib/arclight.libsonnet` before proceeding |

# Agent Rules — deepblue-documents-kube (project-specific additions)

> **Base guidelines apply first**: `guidelines/base/AGENTS.md`
> Sections in this file **override** any base section with the same `## Heading`.
> Additional sections here are appended after the base.
>
> **Task tracking files for this project live at:**
> `guidelines/projects/deepblue-documents-kube/`

## Branch Strategy

This is an ArgoCD GitOps repository. The developer works directly on the `main` branch for
day-to-day work. **Do not create feature branches** unless the developer explicitly asks for
one (e.g., for substantial refactoring that needs developer review before merging).

- **Commit to the currently active branch** — whatever `git branch --show-current` returns.
  In normal operation this will be `main`.
- **One Jira ticket at a time.** Tasks are keyed as `DEEPBLUE-NNN`. There is no parallel
  per-ticket directory structure; all task tracking lives in `AGENT_TODO.md` and `AGENT_DONE.md`
  at `guidelines/projects/deepblue-documents-kube/`.
- **Do not create `tasks/` directories**, archive directories, or any per-ticket folder
  structure. This project does not use that pattern.

## Task Tracking (AGENT_TODO.md / AGENT_DONE.md)

Task tracking for this project lives in the agents framework repository at
`guidelines/projects/deepblue-documents-kube/AGENT_TODO.md` and `AGENT_DONE.md`.

- **AGENT_TODO.md** is the active task list. Organise work as **tasks** with **subtasks**:
  ```
  ## Task Title
  Short description of the overall goal.

  - [ ] Subtask one
  - [ ] Subtask two
  - [ ] Verify the current state of the project achieves the task goal
  - [ ] Verify with the developer that the task is complete
  ```
- **Before executing any multi-step plan**, add it to `AGENT_TODO.md` first — either as a
  new task (if it represents a distinct goal) or as additional subtasks under the current
  task (if it is part of ongoing work). Do not begin execution until the plan is recorded.
- **Check off subtasks** (`- [x]`) as they are completed. Keep the task in `AGENT_TODO.md`
  until **all** subtasks — including the final developer-verification step — are checked off.
- **Every task must end with a developer-verification subtask** as its final item:
  `- [ ] Verify with the developer that the task is complete`
  When this subtask is reached, ask: *"Are there any additional subtasks needed before this
  task is complete?"* Add any new subtasks before the verification step.
- **Only when all subtasks are done**, move the whole task to `AGENT_DONE.md`:
  1. **Remove** the task block from `AGENT_TODO.md`.
  2. **Prepend** it to `AGENT_DONE.md` (insert after the `# AGENT_DONE` heading) with a
     timestamp and brief summary. This keeps `AGENT_DONE.md` in **reverse chronological
     order** (newest entry first).
- Example entry in `AGENT_DONE.md`:
  ```
  ## 2026-04-21T14:32:00 — Added AGENTS.md paging rule
  Added the first rule to AGENTS.md requiring all CLI commands to suppress
  interactive paging so output is captured without waiting for user input.
  ```

### Reordering Tasks in `AGENT_TODO.md`

**Never use string-search-and-replace to reorder tasks.** Always use Python:

```python
import re
content = open('AGENT_TODO.md').read()
parts = re.split(r'(?=^## )', content, flags=re.MULTILINE)
header, tasks = parts[0], parts[1:]
tasks.append(tasks.pop(2))  # example: move index 2 to end
open('AGENT_TODO.md', 'w').write(header + ''.join(tasks))
```

After reordering, verify task headings are in the expected order and update the Active Work
table in `README.md` to match.

## Plans (`plans/`)

Design documents, runbooks, and step-by-step execution plans live in `plans/`.

- **Do not move, rename, archive, or delete any file in `plans/`** — the developer removes
  plan files manually when they are no longer relevant.
- When creating a new plan for a multi-step task, save it under `plans/PLAN<IDENTIFIER>.md`
  (e.g. `plans/PLAN466.md`, `plans/PLANCRONJOBS.md`).
- Reference the plan file in the corresponding task block in `AGENT_TODO.md` so the next
  agent can find full step-by-step instructions.
- Add new plan files to the repository structure block in `README.md`.

## Keeping `README.md` in Sync

The **Active Work** section of `README.md` (under `## Active Work`) contains a status
table only — one row per task with a one-line status. Keep it in sync with `AGENT_TODO.md`:

- **Task status changes** → update the `Status` cell.
- **Task completed** → remove its row from the table.
- **New task added** → add a row with status "Not started" (or "Blocked on …").
- **New supporting file created** (e.g., a new `dotpy/` script, a new plan file) → add it
  to the repository structure code block in `## Repository Structure` and to `dotpy/README.md`
  if it is a new Python script.

Detailed resumption context lives in **`AGENT_TODO.md`**, not in `README.md`.

After editing `README.md`, always run `python3 dotpy/check_tables.py README.md`.

## Git Commits

- **Never amend existing commits.** Always create a new commit using `git commit`.
- **Do not force-push** or rewrite history unless the developer explicitly instructs it.
- **Never run `git push`.** The developer handles all pushes. The agent may commit locally
  but must never run `git push` unless the developer explicitly instructs it.

### Writing commit messages — use `dotpy/commit.py`, never `git commit -m`

**Never use `git commit -m "..."` for multi-line messages.**

**Always use this two-step pattern instead:**

1. Use `create_file` to write the commit message to `dotpy/commit-msg.txt`:
   ```
   subject line here

   Body paragraph here.
   ```
2. Run:
   ```shell
   python3 dotpy/commit.py | cat
   ```

`dotpy/commit.py` reads the message from `dotpy/commit-msg.txt`, writes it to a temp file,
and calls `git commit -F`. `commit-msg.txt` is gitignored — never committed.

Single-line subject-only commits are the **one exception** where `-m` is safe:
```shell
git commit -m "chore: single line message" | cat
```

## Kubernetes Cluster Topology

This project uses **two separate Kubernetes clusters**. Always confirm which context is
active before running `kubectl` commands, and switch explicitly when moving between
environments:

| Environment         | kubectl context name            | Namespaces                   |
|---------------------|---------------------------------|------------------------------|
| `production`        | `deepblue-documents-production` | `production`, `argocd`       |
| `workshop` + `demo` | `deepblue-documents-workshop`   | `workshop`, `demo`, `argocd` |

**Production is on its own cluster** — it is never accessible via the workshop context,
and vice-versa.

### Executing scripts inside backend pods

**Always ask the developer before running any Perl or shell script inside a backend pod**
in any environment (production, workshop, or demo). This includes scripts in
`/dspace/bin/monthlies/`, `/dspace/bin/cronjobs/`, `/dspace/bin/aptrust/`, and any other
script that reads from or writes to the database, filesystem, or external services.

These scripts operate directly on live data and can have side effects that are difficult
or impossible to reverse. The developer must confirm the script, the target environment,
and the expected side effects before execution.

### Destructive `kubectl` and `tk apply` commands

**Never run `tk apply` or any state-modifying `kubectl` command without the developer's
explicit instruction.**

Commands that **require explicit developer approval before running:**

- `tk apply <env>` — applies Tanka-rendered manifests directly to the cluster
- `kubectl delete <resource>` — deletes any Kubernetes resource
- `kubectl apply -f ...` / `kubectl create ...` / `kubectl patch ...` — creates or modifies
  resources outside of ArgoCD
- `kubectl exec` commands that **modify state** — e.g. `dspace user --modify`, `psql`
  writes, any command that writes to the filesystem or database inside a pod

Commands that are **safe to run without prior approval** (read-only):

- `kubectl get`, `kubectl describe`, `kubectl logs` — inspect resources
- `tk show <env>`, `tk diff <env>` — render and diff manifests without applying
- `kubectl exec -- cat /path/to/file`, `kubectl exec -- ls` — read config or directory
  listings inside a pod
- `kubectl config current-context`, `kubectl config use-context` — context switching

### Switching contexts

```shell
# Target production
kubectl config use-context deepblue-documents-production | cat

# Target workshop or demo
kubectl config use-context deepblue-documents-workshop | cat

# Confirm the active context before running any kubectl command
kubectl config current-context | cat
```

**Rule:** Any time you move from investigating a production resource to a workshop/demo
resource (or vice versa), explicitly switch context **before** running the next `kubectl`
command. Never assume the context is already correct from a previous step.

## ArgoCD and the Remote `main` Branch

- **ArgoCD only syncs from the remote `origin/main` branch**, not from local commits.
- **Check for unpushed commits** before concluding that the cluster is out of date:
  ```shell
  git --no-pager log --oneline origin/main..HEAD
  ```
- **When a task is blocked because local commits need to reach the cluster**, ask the
  developer to push:
  > "The fix is committed locally but hasn't been pushed to `origin/main` yet. ArgoCD won't
  > sync until you push. Please push when ready and I'll continue once the cluster reflects
  > the new state."
- **Before asking the developer to push**, check whether any pending commits touch production
  resources. If so, warn explicitly:
  > "⚠️ These commits include changes to production resources. Pushing to `origin/main` will
  > trigger an automatic ArgoCD sync and restart affected production pods. Please confirm you
  > are comfortable with a production deployment before pushing."
- After a push, wait for ArgoCD to sync before verifying cluster state:
  ```shell
  kubectl -n argocd get application <app-name> -o jsonpath='{.status.sync.status}' | cat
  ```

## DSpace Configuration — Three-Layer Model and Decision Guide

All DSpace configuration is managed through a three-layer model. **Before editing any
DSpace property, look it up in
[`environments/deepblue-documents/configuration/CLASSIFY.md`](environments/deepblue-documents/configuration/CLASSIFY.md)**
to determine the correct layer and file to edit:

- **Bucket A — common UM non-secret** (mail addresses, DOI username, ClamAV flag, harvest
  flags, `textextractor.*`, `core.authorization.*`, IP ranges, browse indices shared across
  all envs): Edit **`lib/deepblue-backend-cm.jsonnet`**. One change propagates to all three
  environments. Do **not** duplicate Bucket A keys in per-env `backend-cm.jsonnet` files.

- **Bucket B — env-specific non-secret** (`dspace.server.url`, `dspace.ui.url`,
  `handle.prefix`, `nodoi.email`, browse overrides unique to one env): Edit
  **`environments/deepblue-documents/<env>/backend-cm.jsonnet`**. Commit locally and let
  the developer push to `main`. ArgoCD applies automatically; no `kubectl` needed.

- **Bucket C — credentials** (DB password, DOI password, API key,
  `google.analytics.key`): Rotate via `kubectl -n <NS> create secret generic
  dspace-secrets ...`. Never commit credentials.

- **Layer 3c — `oidc-cfg` Secret** (per-env OIDC client ID/secret + startup config
  injection): Managed entirely via `kubectl`. See `CLASSIFY.md § Layer 3c`.

- **Layer 1** (upstream image `dspace.cfg`) and **Layer 2** (`local-cfg` Secret) are both
  retired as of 2026-04-27. Do not reference or recreate either.

### Previewing config changes with Tanka

After editing any `.jsonnet` or `.libsonnet` file, always preview before committing:

```shell
tk show environments/deepblue-documents/<env>
tk diff environments/deepblue-documents/<env>
```

## ConfigMap Key Encoding

In `backend-cm.jsonnet` files, DSpace property names are encoded as Kubernetes env var keys:
- **`__P__`** encodes a **dot** (`.`)
- **`__D__`** encodes a **hyphen** (`-`)
- **`_`** (single underscore) is **preserved literally**

**This is a silent failure mode.** If a hyphen is encoded as `__P__` instead of `__D__`,
DSpace silently discards the env var and falls back to the upstream default — with no error,
no warning, and no log entry.

**Rule: after adding or modifying any `__P__`/`__D__`-encoded key in any
`backend-cm.jsonnet` file, run:**

```shell
python3 dotpy/validate_cm_keys.py
```

- **ERRORS** (exit 1) — the decoded property name is not in `upstream.dspace.cfg`, but a
  variant with different dot/hyphen/underscore placement *is* — clear encoding bug; fix
  before committing.
- **WARNINGS** — decoded property name not found in upstream at all — usually intentional
  UM-specific additions; verify against `CLASSIFY.md`.

If `upstream.dspace.cfg` is not present locally (it is gitignored), extract it:
```shell
docker run --rm ghcr.io/mlibrary/dspace-containerization/dspace-source:umich \
  cat /dspace/config/dspace.cfg \
  > environments/deepblue-documents/configuration/upstream.dspace.cfg
```

### Encoding examples — properties with hyphens

| DSpace property                              | Correct ConfigMap key                                        |
|----------------------------------------------|--------------------------------------------------------------|
| `handle.remote-resolver.enabled`             | `handle__P__remote__D__resolver__P__enabled`                 |
| `textextractor.max-chars`                    | `textextractor__P__max__D__chars`                            |
| `textextractor.use-temp-file`                | `textextractor__P__use__D__temp__D__file`                    |
| `core.authorization.collection-admin.policy` | `core__P__authorization__P__collection__D__admin__P__policy` |
| `webui.content_disposition_format`           | `webui__P__content_disposition_format`                       |

Every `-` in the DSpace name → `__D__`. Every `.` → `__P__`. Every `_` → literal `_`.


## Commit and PR Summaries

In this repository the developer typically pushes commits directly to `main`. A formal PR
summary is only needed when a branch was created for a significant piece of work.

- **When the developer asks for a PR or commit summary**, write it to `pr-summary.md` in
  the project root and open the file so they can select-all and copy from the editor.
  `pr-summary.md` is gitignored.
- Use standard GitHub-flavoured Markdown. Do not use HTML tags.
- Structure:
  1. **`## <Title>`** — one-line description matching the branch/commit purpose.
  2. **`### Summary`** — 2–4 sentences on what the work does and why.
  3. **`### Changes`** — one bold entry per changed file/directory with bullet sub-points.
  4. **`### Notes`** *(optional)* — follow-up items, known limitations.
- Delete `pr-summary.md` after it has been used; do not commit it.


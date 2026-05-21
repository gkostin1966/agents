# Agent Rules — findingaids-argocd (project-specific additions)

> **Base guidelines apply first**: `guidelines/base/AGENTS.md`
> Sections in this file **override** any base section with the same `## Heading`.
> Additional sections here are appended after the base.
>
> **Task tracking files for this project live at:**
> `guidelines/projects/findingaids-argocd/`

## Task Tracking (AGENT_TODO.md / AGENT_DONE.md)

Task tracking for this project lives in the agents framework repository at
`guidelines/projects/findingaids-argocd/AGENT_TODO.md` and `AGENT_DONE.md`.

- **AGENT_TODO.md** is the active task list. Organise work as **tasks** with **subtasks**:
  ```
  ## ARC-nnn: Task Title
  Short description of the overall goal.

  - [ ] Subtask one
  - [ ] Subtask two
  - [ ] Verify the current state of the project achieves the task goal
  - [ ] Verify with the developer that the task is complete
  ```
- **Every task heading must be prefixed with its Jira ticket number** in the form `ARC-nnn`
  (zero-padded to three digits), e.g. `## ARC-042: Upgrade Solr CRDs`. Ask the developer
  for the ticket number when starting a new task if it is not already known.
- **Before executing any multi-step plan**, add it to `AGENT_TODO.md` first. Do not begin
  execution until the plan is recorded.
- **Check off subtasks** (`- [x]`) as they are completed.
- **Every task must end with a developer-verification subtask** as its final item.
- **Only when all subtasks are done**, archive the task using `dotpy/archive_task.py`:
  ```shell
  # Preview first
  python3 dotpy/archive_task.py --dry-run <index> <ticket_digits> "<one-line summary>"
  # Then archive
  python3 dotpy/archive_task.py <index> <ticket_digits> "<one-line summary>"
  ```
  The script checks off the final subtask, removes the task from `AGENT_TODO.md`, and
  prepends a timestamped entry to `AGENT_DONE.md` in the form:
  ```
  ## YYYY-MM-DDTHH:MM:SS — ARC-nnn: Task Title
  ```
  This keeps `AGENT_DONE.md` in **reverse chronological order** (newest entry first).
- Never leave a completed task in `AGENT_TODO.md`; always archive it to `AGENT_DONE.md`.

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

After reordering, verify task headings are in the expected order then update the Active Work
table in `README.md` to match.

## Keeping `README.md` in Sync

The **Active Work** section of `README.md` (under `## Active Work`) must stay in sync with
`AGENT_TODO.md` at all times. Update it whenever the task list changes:

- **Subtask checked off** → update the `Status` cell and add a bullet to the matching
  "Findings from Step N" block summarising what was done.
- **New step findings discovered** → add or update the relevant "Findings from Step N"
  bullet list under the supporting-files table.
- **New supporting file created** → add it to the repository structure code block in
  `## Repository Structure`, to the supporting-files table in `### Resuming a session`,
  and to `dotpy/README.md` if it is a new Python script.
- **Task completed** → remove it from the Active Work table.
- **New task added** → add a row with status "Not started" (or "Blocked on …").

After editing `README.md`, always run `python3 dotpy/check_tables.py README.md`.

## Kubernetes Cluster Topology

This project uses **three separate Kubernetes clusters**. Always confirm which context is
active before running `kubectl` commands, and switch explicitly when moving between
environments:

| Environment             | kubectl context name     | Namespaces                        |
|-------------------------|--------------------------|-----------------------------------|
| `production`, `preview` | `findingaids-production` | `production`, `preview`, `argocd` |
| `staging`               | `findingaids-staging`    | `staging`, `argocd`               |
| `testing`, `admin`      | `findingaids-workshop`   | `testing`, `admin`, `argocd`      |

**Each cluster is entirely separate** — production is never accessible via the staging or
workshop context, and vice-versa.

### Destructive `kubectl` and `tk apply` commands

**Never run `tk apply` or any state-modifying `kubectl` command without the developer's
explicit instruction.** These operations modify live cluster resources.

Commands that **require explicit developer approval before running:**

- `tk apply <env>` — applies Tanka-rendered manifests directly to the cluster
- `kubectl delete <resource>` — deletes any Kubernetes resource
- `kubectl apply -f ...` / `kubectl create ...` / `kubectl patch ...`
- `kubectl exec` commands that **modify state**

Commands that are **safe to run without prior approval** (read-only):

- `kubectl get`, `kubectl describe`, `kubectl logs`
- `tk show <env>`, `tk diff <env>`
- `kubectl exec -- cat /path/to/file`, `kubectl exec -- ls`
- `kubectl config current-context`, `kubectl config use-context`

### Switching contexts

```shell
# Target production / preview
kubectl config use-context findingaids-production | cat

# Target staging
kubectl config use-context findingaids-staging | cat

# Target testing / admin
kubectl config use-context findingaids-workshop | cat

# Confirm the active context
kubectl config current-context | cat
```

**Rule:** Any time you move from investigating a resource in one cluster to a resource in
another cluster, explicitly switch context before running the next `kubectl` command.

## ArgoCD and the Remote `main` Branch

- **ArgoCD only syncs from the remote `origin/main` branch**, not from local commits.
- **Check for unpushed commits** before concluding that the cluster is out of date:
  ```shell
  git --no-pager log --oneline origin/main..HEAD
  ```
- **When a task is blocked because local commits need to reach the cluster**, ask the
  developer to push:
  > "The fix is committed locally but hasn't been pushed to `origin/main` yet. ArgoCD won't
  > sync until you push."
- **Before asking the developer to push**, check whether any pending commits touch
  production resources (e.g. `lib/arclight.libsonnet`, `lib/release.libsonnet`,
  `environments/findingaids/production/`). If so, warn explicitly:
  > "⚠️ These commits include changes to production resources. Pushing to `origin/main` will
  > trigger an automatic ArgoCD sync and restart affected production pods. Please confirm."
- After a push, wait for ArgoCD to sync:
  ```shell
  kubectl -n argocd get application <app-name> -o jsonpath='{.status.sync.status}' | cat
  ```


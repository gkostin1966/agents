# Agent Rules — findingaids-argocd (project-specific additions)

> Base: `guidelines/base/AGENTS.md`. Matching `## Heading` here replaces base section.
> Task tracking: `guidelines/projects/findingaids-argocd/`

## Task Tracking (AGENT_TODO.md / AGENT_DONE.md)

Files: `guidelines/projects/findingaids-argocd/AGENT_TODO.md` and `AGENT_DONE.md`.

- **Every task heading must be prefixed `ARC-nnn`** (zero-padded), e.g. `## ARC-042: Upgrade Solr CRDs`. Ask developer for ticket number if unknown.
- Record plan in `AGENT_TODO.md` before executing. Check off (`- [x]`) as completed.
- Every task ends with `- [ ] Verify with the developer that the task is complete`.
- **All done → archive using `dotpy/archive_task.py`**:
  ```shell
  python3 dotpy/archive_task.py --dry-run <index> <ticket_digits> "<one-line summary>"
  python3 dotpy/archive_task.py <index> <ticket_digits> "<one-line summary>"
  ```
- Reorder tasks with Python only — never string-replace.

## Keeping `README.md` in Sync

`README.md § Active Work` table must stay in sync with `AGENT_TODO.md`. Update on task/subtask changes.
New supporting file → add to `## Repository Structure` and `dotpy/README.md`.
After editing `README.md`: `python3 dotpy/check_tables.py README.md`

## Kubernetes Cluster Topology

Three separate clusters. **Always confirm context before any `kubectl` command.**

| Environment             | kubectl context name     | Namespaces                        |
|-------------------------|--------------------------|-----------------------------------|
| `production`, `preview` | `findingaids-production` | `production`, `preview`, `argocd` |
| `staging`               | `findingaids-staging`    | `staging`, `argocd`               |
| `testing`, `admin`      | `findingaids-workshop`   | `testing`, `admin`, `argocd`      |

Each cluster entirely separate — switch context explicitly when moving between environments.

```shell
kubectl config use-context findingaids-production | cat
kubectl config use-context findingaids-staging | cat
kubectl config use-context findingaids-workshop | cat
kubectl config current-context | cat
```

### Destructive commands — require explicit approval

- `tk apply <env>`, `kubectl delete`, `kubectl apply/create/patch`, `kubectl exec` with state modification

Safe (no approval needed): `kubectl get/describe/logs`, `tk show/diff`, `kubectl exec -- cat/ls`, context switching.

## ArgoCD and the Remote `main` Branch

- ArgoCD syncs from `origin/main` only — local commits are invisible to the cluster.
- Before concluding cluster is out of date: `git --no-pager log --oneline origin/main..HEAD`
- Blocked on unpushed commits → ask developer to push. Before asking, check if pending commits touch production resources (`lib/arclight.libsonnet`, `lib/release.libsonnet`, `environments/findingaids/production/`). If so, warn: automatic ArgoCD sync will restart production pods.
- After push: `kubectl -n argocd get application <app-name> -o jsonpath='{.status.sync.status}' | cat`


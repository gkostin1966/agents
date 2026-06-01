# Agent Rules — Merged Agent Guidelines

> **This file is auto-generated.** Do not edit it directly.
> Edit `guidelines/base/AGENTS.md` (shared rules) or
> `guidelines/projects/deepblue-documents-kube/AGENTS.md` (project overrides), then regenerate.

## File Access

- Stay within the project directory. Outside file: read only the specific file requested — no browsing.
- **Never read `AGENT_QUIZ_ANSWERS.md`** until all quiz answers written **and** developer explicitly grants permission.

## Command-Line Tool Usage

- Paging: `git --no-pager <cmd>` or `| cat`. Never interactive input.
- **Never multiline code via `-c` flags** — zsh triggers `dquote>` heredoc mode, corrupts session silently.
- **Never shell heredocs** (`<< 'MARKER'`) — same corruption risk; previous unclosed `<<` swallows all subsequent commands.
- Fix for both: write to file, run the file:
  ```shell
  python3 scripts/myscript.py | cat   # reusable
  python3 /tmp/run.py | cat           # one-off
  ```
- If terminal stuck (no output / garbled): run the heredoc end-marker (`EOF`, `PYEOF`, etc.) as a standalone command to escape.

## Python Utility Scripts

- Check project utility-script dir first (`scripts/README.md` or `dotpy/README.md`) before writing ad-hoc helpers.
- Save reusable scripts there; add shebang + Usage docstring + README entry.
- No utility dir → write to `/tmp/run.py`.

## Git Commits

Never amend. Never force-push. **Never `git push`** — developer pushes.

**Never `git commit -m "..."` for multiline.** Use `dotpy/commit.py`:
1. Write message to `dotpy/commit-msg.txt`.
2. `python3 dotpy/commit.py | cat`

Single-line exception: `git commit -m "chore: one line" | cat`

## Pull Request Summaries

- Write to `pr-summary.md` (gitignored). Structure: `## Title`, `### Summary`, `### Changes`, `### Notes`. Delete after use.

## Email Drafts for Third Parties

- Write drafts as `.md` files under `communications/<channel>-<topic>.md` (e.g. `communications/email-its-request.md`).
- `communications/` is tracked in git. Do not gitignore individual draft files.

## Markdown Tables

Data rows define required column width. Pad header and separator to match widest data cell.

## Branch Strategy

ArgoCD GitOps repo. Developer commits directly to `main`. No feature branches unless explicitly requested.

- Commit to whatever `git branch --show-current` returns.
- Tickets: `DEEPBLUE-NNN`. No `tasks/` directories — all tracking in flat `AGENT_TODO.md`/`AGENT_DONE.md`.

## Task Tracking (AGENT_TODO.md / AGENT_DONE.md)

Files: `guidelines/projects/deepblue-documents-kube/AGENT_TODO.md` and `AGENT_DONE.md`.

- Add task to `AGENT_TODO.md` before executing any multi-step plan.
- Every task ends with `- [ ] Verify with the developer that the task is complete`.
- All done → remove from `AGENT_TODO.md`, prepend timestamped entry to `AGENT_DONE.md`.
- Reorder tasks with Python only — never string-replace.

## Plans (`plans/`)

- Plans live in `plans/`. **Never delete or rename** — developer removes manually.
- New plan → `plans/PLAN<ID>.md`. Reference in `AGENT_TODO.md`. Add to `README.md` structure.

## Keeping `README.md` in Sync

`README.md § Active Work` is a status table synced with `AGENT_TODO.md`. Update on task changes.
After editing `README.md`, always run: `python3 dotpy/check_tables.py README.md`

## Kubernetes Cluster Topology

Two separate clusters. **Always confirm context before any `kubectl` command.**

| Environment         | kubectl context name            | Namespaces                   |
|---------------------|---------------------------------|------------------------------|
| `production`        | `deepblue-documents-production` | `production`, `argocd`       |
| `workshop` + `demo` | `deepblue-documents-workshop`   | `workshop`, `demo`, `argocd` |

Switch context explicitly when moving between environments — never assume it is already correct.

```shell
kubectl config use-context deepblue-documents-production | cat
kubectl config use-context deepblue-documents-workshop | cat
kubectl config current-context | cat
```

**Always ask the developer before running any script inside a backend pod** (`/dspace/bin/...`). Scripts operate on live data and may be irreversible.

### Destructive commands — require explicit approval

- `tk apply <env>`, `kubectl delete`, `kubectl apply/create/patch`, `kubectl exec` with state modification

Safe (read-only, no approval needed): `kubectl get/describe/logs`, `tk show/diff`, `kubectl exec -- cat/ls`, context switching.

## ArgoCD and the Remote `main` Branch

- ArgoCD syncs from `origin/main` only — local commits are invisible to the cluster.
- Before concluding cluster is out of date: `git --no-pager log --oneline origin/main..HEAD`
- Blocked on unpushed commits → ask developer to push. Before asking, check if any pending commit touches production resources — if so, warn explicitly about automatic ArgoCD sync and pod restarts.
- After push, verify sync: `kubectl -n argocd get application <app-name> -o jsonpath='{.status.sync.status}' | cat`

## DSpace Configuration — Three-Layer Model

**Before editing any DSpace property**, look it up in `environments/deepblue-documents/configuration/CLASSIFY.md`.

- **Bucket A** (shared non-secret): edit `lib/deepblue-backend-cm.jsonnet`. Do **not** duplicate in per-env files.
- **Bucket B** (env-specific non-secret): edit `environments/deepblue-documents/<env>/backend-cm.jsonnet`.
- **Bucket C** (credentials): `kubectl -n <NS> create secret generic dspace-secrets ...`. Never commit.
- **Layer 3c** (`oidc-cfg` Secret): `kubectl` only. See `CLASSIFY.md § Layer 3c`.
- **Layers 1 & 2** are retired (2026-04-27). Do not reference or recreate.

After editing `.jsonnet`/`.libsonnet`: `tk show environments/deepblue-documents/<env>` then `tk diff`.

## ConfigMap Key Encoding

**Silent failure mode.** Wrong encoding → DSpace silently ignores the key with no error or log.

- `__P__` = `.` (dot)
- `__D__` = `-` (hyphen)
- `_` = literal underscore

After adding/modifying any `__P__`/`__D__` key in `backend-cm.jsonnet`: `python3 dotpy/validate_cm_keys.py`

ERRORS = encoding bug (fix before commit). WARNINGS = key not in upstream (check CLASSIFY.md).

If `upstream.dspace.cfg` missing (gitignored): `docker run --rm ghcr.io/mlibrary/dspace-containerization/dspace-source:umich cat /dspace/config/dspace.cfg > environments/deepblue-documents/configuration/upstream.dspace.cfg`

| DSpace property                              | Correct ConfigMap key                                        |
|----------------------------------------------|--------------------------------------------------------------|
| `handle.remote-resolver.enabled`             | `handle__P__remote__D__resolver__P__enabled`                 |
| `textextractor.max-chars`                    | `textextractor__P__max__D__chars`                            |
| `textextractor.use-temp-file`                | `textextractor__P__use__D__temp__D__file`                    |
| `core.authorization.collection-admin.policy` | `core__P__authorization__P__collection__D__admin__P__policy` |
| `webui.content_disposition_format`           | `webui__P__content_disposition_format`                       |



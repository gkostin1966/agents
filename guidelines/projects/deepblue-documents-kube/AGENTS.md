# Agent Rules — deepblue-documents-kube

## Quick Session Checklist

- `[always]` Run startup orientation commands and stop for unexpected branch/working state.
- `[always]` Read local project `AGENTS.md` and follow project-specific overrides.
- `[always]` Identify the active ticket key from branch naming rules.
- `[when-bookkeeping]` Read/update task state files before and after substantive work.
- `[when-committing]` Base commit guidance on tracked/staged files only.

## Rule Tags

- `[always]` Applies to every session/task.
- `[when-bookkeeping]` Applies when maintaining `.agents` task/status metadata.
- `[when-committing]` Applies when preparing, suggesting, or executing commit actions.

## `.agents` Policy (Canonical)

- `[always]` Treat `.agents/` as shared agent-framework metadata and long-term memory.
- `[always]` Maintain relevant `.agents/` files in place when required for the active task.
- `[always]` Do not treat `.agents/` updates as normal app-code commit content in mounted repositories.
- `[always]` Agents do not commit `.agents/` files in mounted repositories unless the developer explicitly directs otherwise.

## File Access

- `[always]` Stay within the project directory. Outside file: read only the specific file requested — no browsing.
- `[always]` **Never read `AGENT_QUIZ_ANSWERS.md`** until all quiz answers written **and** developer explicitly grants permission.
- `[always]` Follow `## .agents Policy (Canonical)` for ownership and commit-boundary rules.

## Command-Line Tool Usage

- Paging: `git --no-pager <cmd>` or `| cat`. Never interactive input.
- **Never multiline code via `-c` flags** — zsh triggers `dquote>` heredoc mode, corrupts session silently.
- **Never shell heredocs** (`<< 'MARKER'`) — same corruption risk; previous unclosed `<<` swallows all subsequent commands.
- Fix for both: write to file, run the file:
  ```shell
  python3 .agents/scripts/shared/myscript.py | cat   # reusable
  python3 .agents/tmp/run.py | cat    # one-off
  ```
- If terminal stuck (no output / garbled): run the heredoc end-marker (`EOF`, `PYEOF`, etc.) as a standalone command to escape.

## Python Utility Scripts

- Check project utility-script dir first (`.agents/scripts/README.md`) before writing ad-hoc helpers.
- Save reusable scripts there; add shebang + Usage docstring + README entry.
- No utility dir → write to `.agents/tmp/run.py`.

## Git Commits


- `[when-committing]` Never amend. Never force-push. **Never `git push`** — developer pushes.
- `[when-committing]` Base commit suggestions on tracked/staged files only (`git status`, `git diff --staged`).

- `[when-committing]` **Never `git commit -m "..."` for multiline.** Use `.agents/scripts/shared/commit.py`:
  1. Write message to `.agents/scripts/shared/commit-msg.txt`.
  2. `python3 .agents/scripts/shared/commit.py | cat`

- `[when-committing]` Single-line exception: `git commit -m "chore: one line" | cat`

## Pull Request Summaries

- Write to `pr-summary.md` (gitignored). Structure: `## Title`, `### Summary`, `### Changes`, `### Notes`. Delete after use.

## Email Drafts for Third Parties

- Write drafts as `.md` files under `communications/<channel>-<topic>.md` (e.g. `communications/email-its-request.md`).
- `communications/` is tracked in git. Do not gitignore individual draft files.

## Markdown Tables

Data rows define required column width. Pad header and separator to match widest data cell.

## Response Hygiene

- Distinguish verified facts from assumptions. If something is not verified, label it explicitly.
- Do not suggest next steps that conflict with repository rules.
- If task metadata is clearly stale or inconsistent (for example ticket index summary/status drift, or `STATUS.md` not matching `TODO.md`), fix it proactively and report the change. Do not ask for permission first when the correction is clear and non-destructive.

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
After editing `README.md`, always run: `python3 .agents/scripts/shared/check_tables.py README.md | cat`

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

## DSpace Configuration — Current Model

The legacy `environments/deepblue-documents/configuration/` directory has been removed.
Do not recreate it or reference retired docs from that path.

- **Shared non-secret overrides:** edit `lib/deepblue-backend-cm.jsonnet`.
- **Env-specific non-secret overrides:** edit `environments/deepblue-documents/<env>/backend-cm.jsonnet`.
- **Credentials:** manage via Kubernetes Secrets (for example `dspace-secrets`) using `kubectl`; never commit secret values.
- **OIDC module config (`oidc-cfg` Secret):** `kubectl` only.

After editing `.jsonnet`/`.libsonnet`: `tk show environments/deepblue-documents/<env>` then `tk diff`.

## ConfigMap Key Encoding

**Silent failure mode.** Wrong encoding → DSpace silently ignores the key with no error or log.

- `__P__` = `.` (dot)
- `__D__` = `-` (hyphen)
- `_` = literal underscore

After adding/modifying any `__P__`/`__D__` key in `backend-cm.jsonnet`: `python3 .agents/scripts/shared/validate_cm_keys.py | cat`

ERRORS = encoding bug (fix before commit). WARNINGS = potentially custom key — verify intent from current repo files and task context.

| DSpace property                              | Correct ConfigMap key                                        |
|----------------------------------------------|--------------------------------------------------------------|
| `handle.remote-resolver.enabled`             | `handle__P__remote__D__resolver__P__enabled`                 |
| `textextractor.max-chars`                    | `textextractor__P__max__D__chars`                            |
| `textextractor.use-temp-file`                | `textextractor__P__use__D__temp__D__file`                    |
| `core.authorization.collection-admin.policy` | `core__P__authorization__P__collection__D__admin__P__policy` |
| `webui.content_disposition_format`           | `webui__P__content_disposition_format`                       |



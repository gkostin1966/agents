# Agent Rules — findingaids-argocd

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
  python3 scripts/myscript.py | cat   # reusable
  python3 .agents/tmp/run.py | cat    # one-off
  ```
- If terminal stuck (no output / garbled): run the heredoc end-marker (`EOF`, `PYEOF`, etc.) as a standalone command to escape.

## Python Utility Scripts

- Check project utility-script dir first (`scripts/README.md` or `dotpy/README.md`) before writing ad-hoc helpers.
- Save reusable scripts there; add shebang + Usage docstring + README entry.
- No utility dir → write to `.agents/tmp/run.py`.

## Git Commits

- `[when-committing]` Never amend. Never force-push. Never push to `main`.
- `[when-committing]` Base commit suggestions on tracked/staged files only (`git status`, `git diff --staged`).
- `[when-committing]` **Never `git commit -m "..."` for multiline** — write to `.agents/tmp/commit-msg.txt`, then `git commit -F .agents/tmp/commit-msg.txt | cat`.
- `[when-committing]` If project has `scripts/commit.py` or `dotpy/commit.py`, use that instead.
- `[when-committing]` Single-line exception: `git commit -m "chore: one line" | cat`.

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


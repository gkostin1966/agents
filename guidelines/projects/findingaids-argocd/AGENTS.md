# Agent Rules — findingaids-argocd

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

- Never amend. Never force-push. Never push to `main`.
- **Never `git commit -m "..."` for multiline** — write to `/tmp/commit-msg.txt`, then `git commit -F /tmp/commit-msg.txt | cat`.
- If project has `scripts/commit.py` or `dotpy/commit.py`, use that instead.
- Single-line exception: `git commit -m "chore: one line" | cat`.

## Pull Request Summaries

- Write to `pr-summary.md` (gitignored). Structure: `## Title`, `### Summary`, `### Changes`, `### Notes`. Delete after use.

## Email Drafts for Third Parties

- Write drafts as `.md` files under `communications/<channel>-<topic>.md` (e.g. `communications/email-its-request.md`).
- `communications/` is tracked in git. Do not gitignore individual draft files.

## Markdown Tables

Data rows define required column width. Pad header and separator to match widest data cell.

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


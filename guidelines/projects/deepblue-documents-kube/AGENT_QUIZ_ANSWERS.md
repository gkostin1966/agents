# Agent Onboarding Quiz — Answer Key

> ⚠️ **DO NOT READ THIS FILE** until you have answered all 30 questions in
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

**A3.**
- **ArgoCD not reflecting change:** Check for unpushed local commits first:
  `git --no-pager log --oneline origin/main..HEAD`. ArgoCD only syncs from `origin/main`,
  not from local commits. Ask the developer to push if commits are pending.
- **Applying without waiting:** `tk apply <env>` would apply Tanka manifests directly.
  **No** — you may not run `tk apply` without explicit developer approval. It bypasses the
  ArgoCD/git control loop and modifies live resources directly.
- **Safe without approval:** `kubectl get`, `kubectl describe`, `kubectl logs`,
  `tk show`, `tk diff`, read-only `kubectl exec` (e.g. `exec -- cat /path/to/file`),
  `kubectl config current-context / use-context`
- **Require developer approval:** `kubectl delete`, `kubectl apply -f`, `kubectl patch`,
  `kubectl create`, state-modifying `kubectl exec` (e.g. `dspace user --modify`, `psql` writes),
  `tk apply`

*(Source: `AGENTS.md` § ArgoCD and the Remote `main` Branch; § Destructive `kubectl` and `tk apply` commands)*

---

**A4.**
- **Amend request:** Create a **new commit** on top of HEAD with `git commit`. Never use
  `git commit --amend`. The developer will squash commits manually as needed.
- **Branch strategy:** The developer works directly on the `main` branch for day-to-day work.
  The agent commits to whichever branch is currently active (normally `main`) — do not create
  feature branches unless the developer explicitly asks. There is no per-ticket directory
  structure; all task tracking lives in `AGENT_TODO.md` and `AGENT_DONE.md`.
- **`git push`:** Never run `git push`. The developer handles all pushes.

*(Source: `AGENTS.md` § Branch Strategy and § Git Commits)*

---

**A5.** (lowest priority first):
1. **Layer 1** — `dspace.cfg` baked into the Docker image (upstream defaults, unmodified)
2. **Layer 3a** — `backend-environment` ConfigMap env vars (all UM non-secret overrides, Bucket A + B)
3. **Layer 3b** — `dspace-secrets` Secret env vars (credentials, Bucket C)

Layer 2 (`local.cfg` / `local-cfg` Secret) was retired — DSpace 7's kernel does not load it.

There is also **Layer 3c** — the `oidc-cfg` Kubernetes Secret, whose `authentication-oidc.cfg`
file is copied to `/dspace/config/modules/authentication-oidc.cfg` at pod startup. This injects
per-environment OIDC client credentials and Shibboleth endpoints. It is a file-injection
mechanism, not an env-var override, and is NOT covered by `_audit_coverage.py` or
`validate_cm_keys.py`. See `CLASSIFY.md § Layer 3c`.
*(Source: `environments/deepblue-documents/configuration/README.md` § Configuration Layers)*

---

**A6.** Edit **`lib/deepblue-backend-cm.jsonnet`** (it is a Bucket A — common UM non-secret override,
same in all 3 envs). Commit and push to `main`; ArgoCD applies it automatically.
The wrong answer (now retired): editing the `dspace-cfg` Secret.
*(Source: `lib/deepblue-backend-cm.jsonnet` lines ~21–23; `configuration/README.md` § Decision guide)*

---

**A7.** Via `envFrom.secretRef` in the backend container spec. Defined in
`lib/deepblue-documents.libsonnet` in the `backend.deployment` container `envFrom` array
(entry: `{ secretRef: { name: 'dspace-secrets', optional: true } }`).
*(Source: `lib/deepblue-documents.libsonnet` lines ~388–390)*

---

**A8.** DSpace 7's kernel does not load `local.cfg` at all. Verified by running
`dsprop -p mail.admin` after mounting and copying `local.cfg` into place — it returned
the vanilla default, not the UM value. Retired **2026-04-27** alongside the `dspace-cfg` Secret.
*(Source: `environments/deepblue-documents/configuration/README.md` § Working with `local.cfg`)*

---

**A9.** **Demo**: No `handle__P__prefix` in `demo/backend-cm.jsonnet`.
**Production**: Yes — `handle__P__prefix: '2027.42'` in `production/backend-cm.jsonnet`.
**Workshop**: No `handle__P__prefix` in `workshop/backend-cm.jsonnet`.
Upstream default: `123456789` (a placeholder; demo and workshop fall through to this).
*(Source: the three `backend-cm.jsonnet` files; `CLASSIFY.md` Bucket E)*

---

**A10.**
| Task                                                      | Status                                                                                                                                             |
|-----------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| Demo Login Failure — All local accounts unable to log in  | (a/b) partially actionable — root cause fixed; 4 developer actions pending (OIDC client fix, password reset, account creation, item investigation) |
| Verify `handle.prefix` in demo and workshop               | (b) needs team confirmation                                                                                                                        |
| Production Config — Confirm correct `nodoi.email` address | (b) needs team confirmation                                                                                                                        |
| DEEPBLUE-466 DEMO — RT2 reconnection (Steps 4b–10)        | (c) blocked on HITS                                                                                                                                |
| DEEPBLUE-466 — RT2 reconnection production (Steps 2b–10)  | (c) blocked on HITS                                                                                                                                |
| CronJob Stabilisation — Phases 2–5                        | (a) immediately actionable (Phase 2 tee-path fix; Phase 2b developer action for José placeholders)                                                 |

*(Source: `AGENT_TODO.md`)*

---

**A11.** CronJob Stabilisation Phase 2: replace `tee /dspace/data/log/clean-discovery` with
`tee /tmp/clean-discovery` and `tee /dspace/data/log/oai-cron` with `tee /tmp/oai-cron`
in the `index-discovery` and `index-oai` commands across all three `cronjobs.jsonnet` files.
*(Source: `AGENT_TODO.md` CronJob Stabilisation Phase 2; `plans/PLANCRONJOBS.md` § Phase 2)*

---

**A12.**
1. `crosswalks/harvest-demo-patched.xml` — patched harvest crosswalk for demo (DSpace 7 JSONPath)
2. `crosswalks/deposit-demo-patched.xml` — patched deposit crosswalk for demo (collection UUIDs added)
3. `crosswalks/license.txt` — Deep Blue Documents Terms of Deposit (for the Deposit License section)

All in `environments/deepblue-documents/configuration/crosswalks/`.
*(Source: `AGENT_TODO.md` DEEPBLUE-466 DEMO steps 4a, 2, 3; `plans/PLAN466DEMO.md`)*

---

**A13.** `deepblue-elements@umich.edu` (UUID `57f90d39-…`, name "For Deposit, Symplectic").
Documented in `plans/PLAN466.md` Step 1 status note and in
`environments/deepblue-documents/configuration/DSPACE_ADMIN.md`.
*(Source: `plans/PLAN466.md` Step 1 status note)*

---

**A14.** `9dcc2058d206c82b1cf1bf426f0f44e79862e2ec`
*(Source: `lib/deepblue-documents.libsonnet` line 27)*

---

**A15.**
- **Affects live production today:** `nodoi__P__email` is set to `'depositsarefun@acm.org'` — a
  test/placeholder value. This is the address DataCite sends "no-DOI" notification emails to;
  wrong value means important production notifications are silently dropped.
  Tracked by: "Production Config — Confirm Correct `nodoi.email` Address" in `AGENT_TODO.md`.

- **Only matters when a commented-out feature is re-enabled:** All 11 `replicate-bagit` bag-info
  contact fields (e.g. `replicate-bagit.tag.bag-info.contact-email = blancoj@umich.edu`,
  `replicate-bagit.tag.bag-info.source-organization = Jose Org`, etc.) are José Blanco's
  development placeholder values. APTrust AIPs submitted with these values would be attributed
  to the wrong organisation. Tracked by the Phase 2b developer action in
  "CronJob Stabilisation (Phases 2–5)" in `AGENT_TODO.md`.

*(Source: `environments/deepblue-documents/production/backend-cm.jsonnet` — nodoi TODO comment
lines ~28–29; replicate-bagit TODO comment and fields lines ~53–71)*

---

**A16.** Only **production** and **workshop** deploy `express`.
**`oauth2-proxy`** is deployed in production, workshop, and **demo** (added 2026-04-29 per
team decision to require U-M WebLogin at the gate for demo). Demo's oauth2-proxy shares the
workshop OIDC client (`lib/oauth2-proxy.cfg`); the frontend auth annotations are withheld
pending ITS fixing the OIDC client and adding the demo callback URL.
*(Source: `environments/deepblue-documents/production/main.jsonnet`;
`environments/deepblue-documents/workshop/main.jsonnet`;
`environments/deepblue-documents/demo/main.jsonnet` — `preview:` block)*

---

**A17.** Demo runs on the **workshop cluster**
(`https://workshop.cluster.deepblue-documents.lib.umich.edu`) in the **`demo`** namespace.
*(Source: `environments/deepblue-documents/configuration/README.md` § Environment Reference;
`environments/deepblue-documents/demo/spec.json`)*

---

**A18.** The `dspace-data` PVC (`ReadWriteOnce`) is not mounted in CronJob pods.
Reason: all three environments are multi-node vclusters. `dspace-data` is already attached
to the node running the backend Deployment. A CronJob pod scheduled to a different node
gets a `Multi-Attach error` and never starts. `index-discovery` and `index-oai` do not
actually need `/dspace/data` — they communicate with Solr and PostgreSQL over the network.
*(Source: `plans/PLANCRONJOBS.md` § Issue A; `lib/cronjob-production.libsonnet` comment lines ~70–74)*

---

**A19.**
1. `python3 dotpy/format_table.py <file.md>` — rewrites the file with all tables correctly padded
2. `python3 dotpy/check_tables.py <file.md>` — exits 0 if all tables are consistent, 1 with errors

*(Source: `AGENTS.md` § Markdown Formatting)*

---

**A20.**
1. **Remove** the task block from `AGENT_TODO.md`
2. **Prepend** it to `AGENT_DONE.md` (insert after the `# AGENT_DONE` heading, before existing entries)
   with an ISO 8601 timestamp and a brief summary

The archived task moves to **`AGENT_DONE.md`**.
*(Source: `AGENTS.md` § Task Tracking — "Only when all subtasks are done, move the whole task to `AGENT_DONE.md`")*

---

**A21.** `__P__` encodes a **dot** (`.`); `__D__` encodes a **hyphen** (`-`); a literal
**underscore** (`_`) is preserved as-is — no encoding needed.

This third rule is a silent failure risk: if a property name contains `_` and it is
accidentally encoded as `__P__` (dot), DSpace silently ignores the env var. Example of
this bug: `webui__P__content__P__disposition__P__format` was wrong — the correct key is
`webui__P__content_disposition_format` (literal underscores preserved).

Example using both `__P__` and `__D__`: `handle__P__remote__D__resolver__P__enabled`
encodes `handle.remote-resolver.enabled`.
Another: `core__P__authorization__P__collection__D__admin__P__submitters`
encodes `core.authorization.collection-admin.submitters`.
*(Source: `AGENTS.md` § ConfigMap Key Encoding — encoding table; `lib/deepblue-backend-cm.jsonnet`)*

---

**A22.** Root cause: `perl_mailer` contains a Perl indirect-object bug —
`new Mail::Mailer->new('smtp', Server => $server)` instead of
`Mail::Mailer->new('smtp', Server => $server)`. This creates a zero-argument `Mail::Mailer`
first (triggering the `testfile` fallback), then calls `->new` on the result. In the old VM
deployment a local MTA (`sendmail`/`postfix`) masked the bug; in Kubernetes there is no local
MTA. Additionally, `relay.mail.umich.edu` uses port 465 (SMTPS/implicit TLS), which
`Mail::Mailer('smtp', ...)` does not support natively.

Preferred fix: install and configure **`msmtp`** as a local MTA in the `dspace-backend`
container image (`mlibrary/dspace-containerization`), pointing it at
`relay.mail.umich.edu:465` with SSL. `Mail::Mailer->new()` will find `msmtp` as a
sendmail-compatible MTA; `perl_mailer` requires no code changes.
*(Source: `plans/PLANCRONJOBS.md` § Issue B)*

---

**A23.** The image's built-in default is `JAVA_OPTS=-Xmx10g`. Without a container
resource limit, the JVM requests 10 GiB of heap; in a vcluster the pod is
OOM-killed by the kernel or by the namespace LimitRange. The production CronJob lib
overrides it to **`-Xmx4g -Xms512m`** with a container `limits.memory: 6Gi`
(the extra 2 GiB above `-Xmx4g` covers off-heap / metaspace / JVM overhead).
*(Source: `lib/cronjob-production.libsonnet` — `env` block and comment; `plans/PLANCRONJOBS.md` Phase 1)*

---

**A24.** `db-backup` uses the **`postgres:13`** image (not the DSpace backend image).
It runs `pg_dump` and writes a compressed dump to an NFS mount at
`ae-backups.value.storage.umich.edu:/ae-backups` (subPath `app-directed-backups/deepblue-docs`).
It does not use `envFrom: backend-environment`; it pulls `DB_PASSWORD` from the
`perl-environment` Secret via `secretKeyRef`.

Schedules:
- **Workshop**: `30 2 * * 0` — Sundays at 02:30 America/Detroit
- **Production**: `30 2 * * 3,6` — Wednesdays and Saturdays at 02:30 America/Detroit
*(Source: `environments/deepblue-documents/workshop/cronjob_db_backup.libsonnet`;
`environments/deepblue-documents/production/production_cronjob_db_backup.libsonnet`)*

---

**A25.** The only env-specific key is **`DSPACE_REST_HOST`** — the hostname the Angular
SSR frontend connects to when making REST API calls (e.g.
`backend.production.deepblue-documents.lib.umich.edu`).

Common misconception: `DSPACE_UI_HOST: '0.0.0.0'` looks like a service-name or external
hostname. It is actually the **bind address** for the Node.js/Express SSR server — `0.0.0.0`
means "listen on all interfaces," which is the correct container practice. It must **not**
be set to a Kubernetes service name; that would confuse it with `DSPACE_REST_HOST`
(the host it *connects to*).
*(Source: `lib/deepblue-frontend-cm.jsonnet` comment lines ~15–19;
`environments/deepblue-documents/production/frontend-cm.jsonnet`)*

---

**A26.** Workshop mounts the **production assetstore** (`production-dspace-prod-assetstore`
PVC) at `/mnt/prod-assetstore` with **`readOnly: true`** — it can read production
bitstream files but cannot write to them. This allows workshop (which uses the production
`filestorage.dir`) to serve real production files for testing. However, **workshop has its
own independent PostgreSQL database** — it does not share production's database.
*(Source: `environments/deepblue-documents/workshop/backend-cm.jsonnet`;
`environments/deepblue-documents/configuration/README.md` § Environment Reference note)*

---

**A27.** Any two of the following (from `CLASSIFY.md` § Open Questions):

1. **`nodoi.email` in production** is `depositsarefun@acm.org` — a placeholder. Affects
   where DataCite "no-DOI" notification emails are sent; wrong value means important
   production notifications are silently dropped.
2. **`identifier.doi.password_working`** — production-only Secret key; purpose undocumented.
   Must be confirmed before any DataCite credential rotation to avoid breaking DOI registration.
3. **`cc.license.jurisdiction = us`** — active in demo, absent in production/workshop.
   Affects CC license generation; unclear whether the omission in production is intentional.
4. **`core.authorization.collection-admin.submitters`** — `false` in demo, `true` in
   production/workshop. May be intentional demo isolation; should be confirmed to avoid
   unexpected access-control differences.
5. **`dspace.url` in demo** — `dspace.cfg` has stale value `http://deepblue.lib.umich.edu`;
   ConfigMap overrides with `http://localhost`. The mismatch is confusing and should be
   cleaned up.
*(Source: `environments/deepblue-documents/configuration/CLASSIFY.md` § Open Questions)*

---

**A28.** There are **two separate clusters**:

| Context name                    | Namespaces managed           |
|---------------------------------|------------------------------|
| `deepblue-documents-production` | `production`, `argocd`       |
| `deepblue-documents-workshop`   | `workshop`, `demo`, `argocd` |

Production is **never** accessible via the workshop context, and vice versa. Running
`kubectl` on the wrong context returns empty results (or results from the wrong cluster)
with no error — it silently targets the wrong environment.

**Mandatory rule:** Before running any `kubectl` command after switching from a production
investigation to a workshop/demo investigation (or vice versa), explicitly run:
```shell
kubectl config use-context deepblue-documents-production   # for production
kubectl config use-context deepblue-documents-workshop     # for workshop or demo
```
Then confirm with `kubectl config current-context | cat` before proceeding.
*(Source: `AGENTS.md`  Kubernetes Cluster Topology)*

---

**A29.** Use **Rich Text Format (`.rtf`)**.

Save the file as **`emails/<short-descriptive-name>.rtf`** inside the `emails/` directory
at the project root (e.g., `emails/its-oidc-request.rtf`). The `emails/` directory is
**tracked in git** — do not add individual filenames to `.gitignore`. Files remain in the
repo until the developer explicitly removes them.

Required structural elements:
1. **`\b Subject:\b0`** line at the top
2. **`\b To:\b0`** and **`\b CC:\b0`** lines with `[placeholder]` values for the developer to fill in
3. Greeting and body, with `\b … \b0` for bold headings
4. `\f1 … \f0` (monospace/Courier) for technical values — client IDs, URLs, shell commands
5. `\bullet` for bullet lists
6. A closing with a `[Your name]` placeholder

Open the file immediately after creating it so the developer can review it.
*(Source: `AGENTS.md` § Email Drafts for Third Parties)*

---

**A30.** `python3 -c "..."` fails in zsh whenever the code spans multiple lines or
contains inner quotes. zsh treats the unclosed double-quote as the start of a heredoc
(`dquote>` prompt), corrupts the command, and can hang the terminal session.

**The universal fix — write to a file, run the file:**
1. Use `insert_edit_into_file` or `create_file` to write the code to a file:
   - Reusable script → `dotpy/myscript.py`
   - Truly one-off → `/tmp/run.py`
2. Run it: `python3 dotpy/myscript.py | cat`

The same rule applies to generating structured file content (RTF, XML, YAML, etc.) —
never build it by echoing strings through the shell; write a Python script that calls
`open(...).write(...)` instead (`dotpy/_gen_rtf.py` is the worked example).

**The single-line `-c` form is safe only when:**
- The entire command fits on one line, **and**
- It contains no inner quotes (single or double), **and**
- It contains no `$` expansions or backticks

Example of a safe one-liner: `python3 -c "print(42)" | cat`
*(Source: `AGENTS.md` § Command-Line Tool Usage)*

---

## Scoring

| Score      | Verdict                                                                                 |
|------------|-----------------------------------------------------------------------------------------|
| 30 / 30    | ✅ Ready to work — agent understands the current project state                           |
| 26–29 / 30 | ⚠️ Review the missed questions before starting work                                     |
| < 26 / 30  | 🛑 Re-read `AGENTS.md`, `AGENT_TODO.md`, and `configuration/README.md` before proceeding |


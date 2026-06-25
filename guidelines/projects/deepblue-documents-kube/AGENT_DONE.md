# AGENT_DONE

## 2026-06-25T13:17:32Z — Demo Login Failure task closed (developer-confirmed fixed)

Closed `Demo Login Failure — All Local Accounts Unable to Log In` and removed it from
`AGENT_TODO.md` per developer confirmation that the issue is fixed.

Key outcome state at closure:
- Root cause analysis and infra/application fixes were already completed (OIDC gate +
  password-login path for demo, account/flow fixes tracked in prior notes).
- Remaining checklist items were operational follow-ups, and the developer confirmed the
  incident is resolved and should be closed.
- `README.md § Active Work` was synchronized to remove this task from current priorities.

## 2026-05-14T00:00:00 — Refactor coding-agent support files (PR #13)

Renamed `TODO.md` → `AGENT_TODO.md` and `DONE.md` → `AGENT_DONE.md`. Introduced
`AGENT_PROMPT.md` as the single session-start entry point (rewritten from a
dor-react-app copy to correctly describe this Kubernetes/Jsonnet/Tanka repository).
Thoroughly updated `AGENTS.md`: new `## Branch Strategy` section (single `main`
branch, no feature branches, no `tasks/` directories); new `## Plans` section
(flat `plans/` directory, developer deletes manually); new `### Destructive kubectl
and tk apply commands` subsection with explicit approved/not-approved command lists;
`## Reordering Tasks` demoted to `###` subsection inside Task Tracking; all 15
sections reordered into logical groups (ground rules → session management →
infrastructure → utilities). Moved operational resumption context (supporting-files
table, per-step findings) from `README.md § Active Work` into `AGENT_TODO.md`
preamble. Fixed stale Q27/Q28 references in `AGENT_QUIZ.md` header (now Q30).
Added session-orientation step (git branch/status/log) to `AGENT_PROMPT.md`.
All `TODO.md` / `DONE.md` references updated throughout. Merged as PR #13.

## 2026-04-29T09:00:00 — backend-cm / frontend-cm Refactoring — Eliminate Duplication, Promote Bucket A
Cross-env diff found 9 keys verbatim-identical in production + workshop but absent from demo.
Upstream analysis: 7 are genuine UM overrides promoted to Bucket A in `lib/deepblue-backend-cm.jsonnet`;
2 matched upstream defaults exactly and were deleted; `handle__P__canonical__P__prefix` removed from
workshop + demo (production retains its `https://hdl.handle.net/` override). Frontend-cm lib comment
fixed (one env-specific key, not two). `validate_cm_keys.py` passed; `tk show` clean on all 3 envs.
Committed `cad4a45`; docs updated in `f4e3862`.

## 2026-04-29T00:30:00 — Fix webui.content_disposition_format/threshold encoding (security)
Full audit of all from-kube.*.dspace.cfg and secret.*.dspace.cfg files against
ConfigMap keys uncovered two properties encoded with all-dots instead of preserving
the literal underscores. `webui.content_disposition_format` is security-relevant:
the UM Jun-2024 fix adding text/html, text/javascript, and text/xml to force
Content-Disposition on those MIME types was silently not applied (phantom property).
Fixed both keys in lib/deepblue-backend-cm.jsonnet. Updated validate_cm_keys.py regex
and canonical() to also detect dot-vs-underscore confusion as an ERROR. Updated AGENTS.md
encoding table. 75 of 75 override properties now accounted for. Committed 4a0c4f1.

## 2026-04-28T23:59:00 — Add ConfigMap Key Encoding Validation (`validate_cm_keys.py`)
Added `dotpy/validate_cm_keys.py` to prevent recurrence of the silent `__P__`/`__D__`
encoding bug that disabled `handle.remote-resolver.enabled`. The script decodes every
encoded key in all `backend-cm.jsonnet` files back to its DSpace property name and
cross-references against `upstream.dspace.cfg`, reporting ERRORS when the decoded
name is absent but a variant with different dot/hyphen placement exists (clear encoding
bug) and WARNINGS for known UM-specific extensions. Added a mandatory `AGENTS.md`
§ ConfigMap Key Encoding rule requiring `validate_cm_keys.py` to be run after any
`backend-cm.jsonnet` edit. Updated `dotpy/README.md` (new script entry + corrected
an erroneous encoding example in the `find_uncovered_props.py` note that was itself
documenting the bug). Updated `HANDLE_SERVER_ADMIN.md` with commit SHA and verified
`/server/resolve/` status. Committed `b198847`.

## 2026-04-28T23:30:00 — Fix `handle.remote-resolver.enabled` Key Encoding Bug
The ConfigMap key `handle__P__remote__P__resolver__P__enabled` was using `__P__` (dot)
to encode the hyphen in `remote-resolver`, inadvertently setting the non-existent property
`handle.remote.resolver.enabled`. The actual `handle.remote-resolver.enabled` was falling
through to the DSpace 7.6 upstream default of `false`, disabling the remote handle resolver
in production and workshop — the root cause of `hdl.handle.net/2027.42/*` returning HTTP 500.
Fixed to `handle__P__remote__D__resolver__P__enabled` in both environments. Committed `f42bb31`,
pushed to `main`, ArgoCD synced both clusters, backend pods restarted. Verified:
`/server/resolve/2027.42/168547` → HTTP 200 ✅. The `/server/resolve/` endpoint is now live.
HANDLE_SERVER_ADMIN.md updated to document the endpoint and the encoding bug.

## 2026-04-28T22:00:00 — Handle Resolution Follow-up: No Action in This Repo
Confirmed that the handle server lives entirely on `bulleit-2.umdl.umich.edu` outside
the Kubernetes cluster. Both hypotheses (firewall blocking Handle.net's servers from
reaching bulleit-2:2641, and/or the handle daemon using a stale DSpace 6 REST API URL
after the DSpace 7 upgrade) require action on bulleit-2 or at Handle.net — neither
involves any file in this repository. Task closed; all investigation/fix work is
out-of-scope for this repo and handed off to the developer and/or HITS.

## 2026-04-28T21:30:00 — PRODUCTION P1: Handle Resolution Down (hdl.handle.net/2027.42/* → 500)
Investigated production handle resolution failure reported by Chris Powell, Joanna Thielen,
and Peter Cerda (2026-04-28). All `hdl.handle.net/2027.42/*` links returned HTTP 500; items
remained accessible via `/items/<uuid>` UUID paths.

**Root cause:** Handle.net's global resolver cannot reach the handle server registered for
prefix `2027.42`. The prefix record (unchanged since 2016, serial 9) points to
`141.213.128.157:2641` (`bulleit-2.umdl.umich.edu`) — the old production DSpace VM that
pre-dates the Kubernetes migration. Handle.net's external servers receive a TCP connect
timeout (`CANNOT_CONNECT_TO_SERVER: SocketTimeoutException: Connect timed out`). The
handle server daemon itself IS running and responds to local probes, but external
connectivity from Handle.net's servers is blocked — most likely a U-M firewall rule
change affecting inbound TCP/UDP on port 2641 from external IPs.

**Phase 5 refactoring confirmed NOT the cause:** All `handle.*` properties in the live
production ConfigMap env vars match `secret.production.dspace.cfg` exactly — every value
is identical; Phase 5 made no effective change to any handle-related property.

**Remaining work at time of investigation (handed off to HITS/sysadmin):**
- Contact `lit-cs-sysadmin@umich.edu` (Handle.net prefix admin) and/or HITS to restore
  external connectivity to `bulleit-2.umdl.umich.edu:2641`, or update the prefix record
  to use HTTP redirect mode pointing at `https://deepblue.lib.umich.edu/handle/`
- Verify fix: `curl -s "https://hdl.handle.net/api/handles/2027.42/167597"` → `responseCode: 1`
- Longer-term: evaluate migrating handle server into Kubernetes or switching to HTTP proxy mode

> **⚠️ Superseded finding** — This investigation concluded the problem was on `bulleit-2`.
> A subsequent investigation (same date, 23:30 entry above) found the **actual root cause**
> was a `__P__`/`__D__` ConfigMap encoding bug that kept `handle.remote-resolver.enabled`
> disabled in DSpace. Fixing that key (commit `f42bb31`) restored handle resolution fully.
> The bulleit-2 external connectivity question remains open at the sysadmin/HITS level, but
> it is **no longer blocking** Deep Blue Documents handle resolution.

**Addendum 2026-04-28 (hypothesis at time — now resolved):** The handle daemon on bulleit-2
resolves handles by calling back into the DSpace REST API. The DSpace 6 → 7 upgrade changed
the API URL structure (`/rest/handle/…` → `/server/api/…`); this was suspected as a secondary
cause. With `handle.remote-resolver.enabled` now correctly set to `true`, DSpace's own
`/server/resolve/` endpoint is live and serving HTTP 200; the bulleit-2 callback hypothesis
was not separately verified but the resolution is working end-to-end.

## 2026-04-28T17:00:00 — frontend-cm.jsonnet Consolidation
Extracted 8 shared keys from the three `frontend-cm.jsonnet` files into
`lib/deepblue-frontend-cm.jsonnet`. Each env file now overrides exactly one key:
`DSPACE_REST_HOST`. Also standardised `DSPACE_UI_HOST` from `'frontend'`
(demo/workshop, incorrect service-name usage) to `'0.0.0.0'` (bind all interfaces)
across all environments and added comments clarifying bind-address vs connection-hostname.

## 2026-04-28T16:00:00 — PLANDSPACECFG: Verify Production CronJobs (Phase 1 of CronJob stabilisation)
`index-discovery` was OOMKilling repeatedly in production on its first scheduled run after the Phase 5
config refactor. Root causes diagnosed and fixed:
- **OOM**: image sets `JAVA_OPTS=-Xmx10g`; no container limit → kernel OOMKill. Fixed by adding
  `resources` limits and `JAVA_OPTS=-Xmx4g` override to all three `cronjob-*.libsonnet` files.
- **Multi-Attach**: `dspace-data` is ReadWriteOnce; all three envs are multi-node vclusters. CronJob
  pods scheduled to a different node than backend cannot attach. Fixed by removing `dspace-data`
  volume+mount from all three libs (indexing jobs don't need it; `tee` log archive is a convenience only).
- Both jobs verified in production: `index-discovery` 17 min/0 restarts ✓; `index-oai` 20s/0 restarts ✓.
- MTA issue (email reports not delivered) identified as a container image bug; tracked in PLANCRONJOBS.md Phase 3.

## 2026-04-28T10:33:00 — URGENT: Fix Missing `identifier.doi.user` in backend-environment ConfigMap
`identifier.doi.user = umich.library` was classified as Bucket A in CLASSIFY.md but accidentally
omitted from the Phase 5 ConfigMap migration (commit `0394967`). When the `dspace-cfg` Secret was
deleted, DSpace fell back to the upstream default `identifier.doi.user = username`. The
`dspace-secrets` Secret still injected the correct DataCite password, so every DOI update returned
`AUTHENTICATION_ERROR`. Fix: added `identifier__P__doi__P__user: 'umich.library'` to
`lib/deepblue-backend-cm.jsonnet` (shared Bucket A). ArgoCD synced, backend rolled, all 4 DOI env
vars confirmed in pod. Fritz re-ran the update script and confirmed "It's working!" (commit `a4ef922`).

## 2026-04-27T22:00:00 — CronJobs — Enable and Verify in All Environments
Enabled `index-discovery` and `index-oai` in all three environments. Demo and workshop
were manually triggered and verified (only benign warnings: missing log dir, no MTA).
Production CronJobs are uncommented and ArgoCD-synced; cluster run verification is tracked
separately under "PLANDSPACECFG — Verify Production CronJobs". All remaining cron jobs
(reporting, external API integrations) moved to the dedicated review task.

- [x] Step 1 — Verify prerequisites: confirm `perl-environment` Secret exists in demo namespace ✓ (Opaque, 21 keys)
- [x] Step 2 — Apply demo environment; confirm `index-discovery` and `index-oai` CronJobs present ✓ (ArgoCD auto-synced)
- [x] Step 3 — Manually trigger demo index-discovery; verify completion ✓ (only benign warnings)
- [x] Step 4 — Manually trigger demo index-oai; verify completion ✓ (fixed: added dspace-cfg mount to cronjob-demo.libsonnet)
- [x] Step 5a — Workshop: fix cronjob-workshop.libsonnet; uncomment both jobs; verify both run cleanly ✓
- [x] Step 5b — Production: uncomment both jobs; fix cronjob-production.libsonnet (retired dspace-cfg mount); ArgoCD-synced ✓
- [x] Step 6 — Remaining cron jobs moved to separate "CronJobs — Review and Enable Remaining CronJobs" task
- [x] Verify with the developer that the task is complete

## 2026-04-27T21:00:00 — backend-cm.jsonnet Consolidation — Extract Shared Bucket A Fields into Shared Base
Audited all four `*backend-cm.jsonnet` files. The three env-specific files each contained ~70 lines
of verbatim duplicate (Bucket A overrides + 13 shared infrastructure constants). The stale
`lib/deepblue-backend-cm.jsonnet` was rewritten as the authoritative shared base (full ConfigMap
structure + Bucket A + infrastructure constants). Each env file was reduced to a thin Bucket B
mixin using `(import 'deepblue-backend-cm.jsonnet') + { backend+: { configmap+: { data+: { ... } } } }`.
Total line count dropped from 425 → 187 across the four files. All three environments verified via
`tk export` — rendered ConfigMaps are byte-for-byte equivalent to the originals.

- [x] Audit all four `*backend-cm.jsonnet` files (lib + demo + production + workshop) and identify shared vs. env-specific fields
- [x] Rewrite `lib/deepblue-backend-cm.jsonnet` with full ConfigMap structure + all Bucket A fields + shared infrastructure constants
- [x] Rewrite `environments/deepblue-documents/demo/backend-cm.jsonnet` as a thin mixin importing the lib base
- [x] Rewrite `environments/deepblue-documents/production/backend-cm.jsonnet` as a thin mixin importing the lib base
- [x] Rewrite `environments/deepblue-documents/workshop/backend-cm.jsonnet` as a thin mixin importing the lib base
- [x] Verify all three environments render correctly with `tk export` and confirm ConfigMap keys are complete and correct
- [x] Verify with the developer that the task is complete

## 2026-04-27T20:00:00 — Phase 5 — Retire `dspace-cfg` and `local-cfg` Secrets
Completed the PLANDSPACECFG Phase 5 work: retired the `dspace-cfg` Secret (holdover
from the old single-file approach) and discovered and retired the `local-cfg` Secret
(DSpace 7's kernel does not load `local.cfg` at all). All UM configuration is now
exclusively in `backend-environment` ConfigMap env vars (`backend-cm.jsonnet`) and
`dspace-secrets`. The image's unmodified `dspace.cfg` is Layer 1. All six orphaned
Secrets (`dspace-cfg` + `local-cfg` × 3 namespaces) were deleted from the cluster.
Key investigation findings: `OidcAuthenticationBean` requires `ip.*` env vars on every
request (null-split NPE); `core.authorization.*` keys require `__D__` encoding for
hyphens (not `__P__`); all 30+ Bucket A properties migrated to ConfigMap env vars.
Key commits: `41b8930`, `0394967`, `69d49cb`, `c065cb3`, `e2319d7`.
All three environments verified: liveness UP, readiness UP, `/server/api` HTTP 200.

## 2026-04-27T14:00:00 — PLANDSPACECFG — Refactor dspace.cfg Configuration Strategy
Replaced the monolithic `dspace-cfg` Secret with a clean three-layer configuration
stack: upstream image defaults → `local.cfg` Secret (46 common UM non-secret overrides)
→ `backend-environment` ConfigMap (17 Bucket B env-specific properties) +
`dspace-secrets` Secret (6 Bucket C credentials as env vars). All layers are active
in demo, workshop, and production. The `dspace-cfg` Secret still holds the full
original `dspace.cfg`; the physical stripping of now-redundant properties (Phase 5)
is deferred — see `CLASSIFY.md` strip checklist and `plans/PLANDSPACECFG.md`.
Documentation updated across `configuration/README.md`, `CLASSIFY.md`,
`plans/PLANDSPACECFG.md`, and `README.md` for developer onboarding clarity.

- [x] Phase 1 — Obtain upstream dspace.cfg from image; diff against all three envs; classify every
  property into buckets A–E (CLASSIFY.md). ✓ Extracted from `dspace-source:umich` at
  `/DSpace/dspace/config/dspace.cfg` (1 689 lines). Three deltas produced (353/426/398 lines).
  46 Bucket A properties → `local.cfg`; 17 Bucket B properties → ConfigMap; 6 Bucket C credentials;
  16 Bucket D already in ConfigMap (strip only); 2 Bucket E (upstream defaults). See `CLASSIFY.md`.
- [x] Phase 2 — Write shared `local.cfg` (Bucket A: 46 common non-secret UM overrides); this file is
  identical across all three environments and will be mounted read-only from a Secret. ✓ Written to
  `configuration/local.cfg` (mail, DOI, harvest, textextractor, webui, virus check, log dir,
  DataCite crosswalk, IP ranges, replicate/duracloud includes, 16 core.authorization properties).
- [x] Phase 3 — **Demo**: create `local-cfg` Secret in demo namespace; create `dspace-secrets` Secret
  in demo namespace; smoke-test demo. ✓ Code done. ✓ Cluster done: both Secrets created; `local.cfg`
  (6863 bytes) active in pod; all dspace-secrets env vars injected; REST API healthy.
- [x] Phase 4 — **Workshop**: create `local-cfg` Secret in workshop namespace; create `dspace-secrets`
  Secret in workshop namespace; smoke-test workshop. ✓ Code done. ✓ Cluster done: both Secrets
  created; `local.cfg` active in pod (broken subPath dir fixed after push); REST API healthy.
- [x] Phase 5 — **Production**: create `local-cfg` Secret in production namespace; create
  `dspace-secrets` Secret in production namespace; smoke-test production. ✓ Code done.
  ✓ Cluster done: both Secrets created (db-prod creds, doi password, analytics key, api key);
  `local.cfg` (6863 bytes) active in pod; all 9 dspace-secrets env vars injected; REST API healthy.
- [x] Phase 6 — Update `configuration/README.md` and `gen_delta.py` for the new three-layer model.
  ✓ README rewritten: three-layer intro, local.cfg workflow, dspace-secrets rotation guide,
  updated ConfigMap table (Bucket B props), dspace.cfg workflow updated with Bucket A/B/C caveats.
  ✓ gen_delta.py: docstring updated with layer model; finding 6 updated (Bucket A now in local.cfg);
  recommendations rewritten to reference all three layers.
- [x] Verify with the developer that the task is complete

## 2026-04-27T00:00:00 — CronJobs — Remove baked-in env arrays from workshop and production cronjob libs
Switched `cronjob-workshop.libsonnet` and `cronjob-production.libsonnet` from a
hard-coded `environment::` array + `env: $.environment` to
`envFrom: [{configMapRef: backend-environment}, {secretRef: perl-environment}]`,
matching the demo pattern and eliminating config drift risk. Volumes/volumeMounts
preserved in the production lib.

- [x] Remove `environment::` array from `lib/cronjob-workshop.libsonnet`; replace `env: $.environment` + `envFrom:[secretRef]` with `envFrom:[configMapRef:backend-environment, secretRef:perl-environment]`
- [x] Remove `environment::` array from `lib/cronjob-production.libsonnet`; same switch (preserve volumes/volumeMounts)
- [x] Verify with the developer that the task is complete

## 2026-04-24T00:00:00 — Slim Down elements-reconnect PR
Removed 13 Symplectic reference documents from `deepblue-466/` (~1,700 lines) before
merging the elements-reconnect branch. Content is preserved in the
`elements-reconnect-backup` branch and is available from Symplectic support.
Updated `plans/PLAN466.md` and `plans/PLAN466DEMO.md` to replace broken
`deepblue-466/` file references with backup-branch pointers. Removed the
`deepblue-466/` entry from `README.md` repository structure block.

- [x] Step 1 — Remove `deepblue-466/` (12 Symplectic reference docs, ~1,700 lines): research
  notes that informed planning but add no operational value to the repo; content is available
  upstream from Symplectic and in the backup branch
- [x] Step 2 — Confirm nothing else warrants removal (crosswalk XMLs, dotpy scripts, plans/,
  DSPACE_ADMIN.md, crosswalks/ are all active work artifacts — keep)
- [x] Step 3 — Update `README.md` repository structure block to remove the `deepblue-466/` entry
- [x] Step 4 — Validate tables: `python3 dotpy/check_tables.py README.md`
- [x] Step 5 — Commit with message: `chore: remove deepblue-466 reference docs before PR merge`
- [x] Verify with the developer that the task is complete

## 2026-04-22T00:00:00 — Consolidate configuration/dotpy into root dotpy
Removed the duplicate `environments/deepblue-documents/configuration/dotpy/` directory
(all 4 files: `calc_widths.py`, `check_tables.py`, `gen_delta.py`, `README.md`).
The nested copy was stale — missing the `CONFIGMAP_OVERRIDDEN_KEYS` constant and the
corrected Finding #2 text added to the root-level `gen_delta.py`. All `python3 dotpy/`
commands in the configuration README already assume running from the repo root, so no
markdown changes were required. Tables validated with `check_tables.py`.

- [x] Delete `environments/deepblue-documents/configuration/dotpy/` (all 4 files + dir)
- [x] Verify no broken `dotpy/` references remain in any markdown file
- [x] Run `python3 dotpy/check_tables.py` on affected markdown files
- [x] Verify the current state of the project achieves the task goal
- [x] Verify with the developer that the task is complete

## 2026-04-22T00:00:00 — Refactor configuration folder from dspace-containerization
Integrated `environments/deepblue-documents/configuration/` (copied from dspace-containerization)
into this project: updated all `backend/config/` path references to
`environments/deepblue-documents/configuration/`, created a root-level `dotpy/` directory with the
three Python utility scripts (`calc_widths.py`, `check_tables.py`, `gen_delta.py`) and their README,
updated the nested `configuration/dotpy/` scripts to point to the root-level copies as canonical,
updated the root `README.md` repository structure and Other READMEs table, and validated all
Markdown tables with `check_tables.py`.

- [x] Update `.gitignore`: replace `backend/config/*.cfg` with `environments/deepblue-documents/configuration/*.cfg`
- [x] Create root-level `dotpy/` with `calc_widths.py`, `check_tables.py`, `gen_delta.py`, `README.md`
- [x] Update `dotpy/gen_delta.py` default path: `environments/deepblue-documents/configuration`
- [x] Update `environments/deepblue-documents/configuration/README.md`: replace all `backend/config/` paths
- [x] Update `environments/deepblue-documents/configuration/dotpy/gen_delta.py`: fix default path for nested location
- [x] Update `environments/deepblue-documents/configuration/dotpy/README.md`: point to root-level scripts as canonical
- [x] Update root `README.md`: add `configuration/` and `dotpy/` to structure; add `configuration/README.md` to Other READMEs table
- [x] Validate all modified Markdown tables with `check_tables.py`
- [x] Verify the current state of the project achieves the task goal
- [x] Verify with the developer that the task is complete

## 2026-04-21T00:00:00 — Guidelines for Coding Agents
Establish `AGENTS.md` and ensure all developer-facing documentation directs
coding agents to read and follow those guidelines at the start of every session.

- [x] Create `AGENTS.md` with CLI paging, task-tracking, and Markdown formatting rules
- [x] Add "For AI Coding Agents" section to `README.md` pointing to `AGENTS.md`
- [x] Update `AGENTS.md`: prepend `DONE.md` entries to keep list in reverse chronological order
- [x] Update `AGENTS.md`: use task/subtask structure; move a task to `DONE.md` only when all subtasks are complete
- [x] Verify the current state of the project achieves the task goal
- [x] Verify with the developer that the task is complete



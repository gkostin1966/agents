# AGENT_TODO

## Resuming a session

1. Check working state: `git branch --show-current | cat` and `git --no-pager status | cat`
2. Read [`AGENTS.md`](AGENTS.md) (rules and conventions).
3. Read the top entries of [`AGENT_DONE.md`](AGENT_DONE.md) for recent completion context.
4. Read this file — the first unchecked subtask in the first task below is where to pick up.
5. Open the plan file linked in that task for full step-by-step instructions.

### Key supporting files — DEEPBLUE-466 DEMO (Steps 4b–10, blocked on HITS)

> Legacy note: `environments/deepblue-documents/configuration/` has been removed from this repository.
> Any references to that path below are historical context only and should not be treated as active file locations.

| File                                                            | Purpose                                                                                    |
|-----------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| `.agents/scripts/shared/check_dspace_rt2.py`                    | Verify DSpace REST API, OAI-PMH, auth, and deposit access before configuring Elements      |
| `plans/PLAN466DEMO.md`                                          | Step-by-step plan with demo-specific URLs and UUIDs                                        |
| `.agents/scripts/shared/patch_harvest_crosswalk.py`             | Step 2 first pass: replaces `select-using="xpath"` → `"jsonpath"` in field-source elements |
| `.agents/scripts/shared/fix_harvest_crosswalk_dspace7.py`       | Step 2 second pass: fixes JSONPath expressions, conditions, repository-status mapping      |
| `.agents/scripts/shared/patch_deposit_crosswalk.py`             | Step 3: adds collection UUID `id=` attributes to deposit crosswalk                         |
| `environments/deepblue-documents/demo/backend-cm.jsonnet`       | Demo ConfigMap — contains PR collection UUID and all env-specific overrides                |

**Findings from Step 1 (completed 2026-04-22):**
- Demo REST API: `https://backend.demo.deepblue-documents.lib.umich.edu/server/api` ✓ DSpace 7.6
- Demo OAI-PMH: `https://backend.demo.deepblue-documents.lib.umich.edu/server/oai/request` ✓ (path is `/server/oai/request`, not `/oai/request`)
- Demo DSpace collections (3 total): `pacerda Testing ground`, `Wiley`, `ME450` — UUIDs in `dotpy/patch_deposit_crosswalk.py`
- PR collection UUID from ConfigMap (`65543b2d-…`) is **not** in the live demo — substituted with `pacerda Testing ground` in deposit crosswalk
- Elements service account for demo REST connection: **`deepblue@umich.edu`** — created 2026-05-15 (UUID `7bef0d0f-134d-4a22-9d69-f6e49a9ba59e`), Administrator group member ✓; password not in repo
- **Note:** `dbrrds@umich.edu` exists in the DSpace DB and was used for API readiness testing, but is NOT the account for the Elements connection

**Findings from Step 2 (completed 2026-04-23):**
- `harvest-demo-patched.xml` is fully patched and ready to upload to Elements
- 26 object-type-selector XPath conditions → JSONPath `(?i)` regex (critical: without this all items classified as "other")
- `public-url` XPath `//handle[1]` → JSONPath `$.handle`
- `funding-acknowledgements` XPath condition removed; all sponsorship values mapped as grants
- `c-citation` XPath `position()`/`last()` replaced with standard `dc.contributor.author`
- `authors` XPath count arithmetic removed; always uses `dc.contributor.author`
- `"Private (in review)"` value-map added for DSpace 7 workflow items

**Findings from Step 3 (completed 2026-04-23):**
- `deposit-demo-patched.xml` is ready to upload to Elements
- Production target collection 'Michigan Research Experts Deposits' does not exist in demo
- Substituted with 'pacerda Testing ground' (`80ca6e1d-fcc4-407f-9484-d3c64a420c73`) — comment in XML flags this for production restore

**Findings from Step 3b — DSpace readiness check (completed 2026-04-23):**
- `dbrrds@umich.edu` password was unknown; reset via `dspace user --modify` (legacy note referenced `configuration/DSPACE_ADMIN.md`, now removed)
- All 5 `check_dspace_rt2.py` checks PASS: REST API ✓, OAI-PMH ✓, auth ✓, collection ✓, deposit ✓
- Fixed CSRF rotation bug in `check_dspace_rt2.py`: DSpace 7 issues a new CSRF token after login and after each POST; script now captures token from response headers at each step

**Findings from Step 4a (completed 2026-04-23):**
- `license.txt` obtained from `/dspace/config/default.license` in the demo pod — Deep Blue Documents Terms of Deposit
- Saved to `crosswalks/license.txt`; same license text applies to production; ready to upload to Elements when HITS session begins

**Production pre-work (completed 2026-04-23):**
- Production REST API ✓ DSpace 7.6; OAI-PMH ✓ HTTP 200
- Production Elements service account: **`deepblue-elements@umich.edu`** (UUID `57f90d39-…`, name "For Deposit, Symplectic") — dedicated account, not `dbrrds`
- 'Michigan Research Experts Deposits' collection UUID in production: `ee9d8886-9a8f-47d9-99d0-923d687fe381`
- `harvest-production-patched.xml` ready: patched from `dspace-Harvest-XwalkIn-map.xml` (already in repo)
- `deposit-production-patched.xml` ready: patched from `dspace-Deposit-XwalkOut-map.xml` (DEEPBLUE-497-fixed) with production UUID

---


## Verify `handle.prefix` in Demo and Workshop
Production sets `handle__P__prefix: '2027.42'` in `backend-cm.jsonnet`. Demo and workshop
do not set this key at all. The DSpace upstream default in `dspace.cfg` is `123456789`
(a placeholder). If demo or workshop items generate handles they may use the wrong prefix,
producing bad `hdl.handle.net` URLs. Confirm whether this is intentional (demo/workshop
don't register handles externally) or whether a correct prefix should be set.

- [ ] Check the upstream `dspace.cfg` default value for `handle.prefix`
- [ ] Confirm with the team whether demo and workshop should have a real or suppressed prefix
- [ ] If needed, add `handle__P__prefix` to `demo/backend-cm.jsonnet` and `workshop/backend-cm.jsonnet`
- [ ] Verify with the developer that the task is complete



## Production Config — Confirm Correct `nodoi.email` Address
The current value `depositsarefun@acm.org` in `production/backend-cm.jsonnet` is a placeholder
set during the PLANDSPACECFG ConfigMap expansion. Confirm the correct address with the team
and update before the next production maintenance window.
Reference: `CLASSIFY.md` open question 1.

Also: `nodoi__P__email: 'abcblancoj@umich.edu'` in both `workshop/backend-cm.jsonnet` and
`demo/backend-cm.jsonnet` are also José test placeholders (the `blancoj@umich.edu` pattern
appears in the replicate-bagit bag-info fields as well). Confirm and update all three envs at
the same time.

- [ ] Confirm the correct `nodoi.email` address with the team (production, workshop, demo)
- [ ] Update `nodoi__P__email` in `production/backend-cm.jsonnet`, `workshop/backend-cm.jsonnet`, and `demo/backend-cm.jsonnet`
- [ ] Commit and push to `main` (ArgoCD applies the ConfigMap update automatically;
  no pod restart required — the new value takes effect on the next backend restart)
- [ ] Verify with the developer that the task is complete



## DEEPBLUE-466 DEMO — Execute RT2 Reconnection Plan in Demo Environment
Run every step in `plans/PLAN466DEMO.md` against `environments/deepblue-documents/demo`
and verify the integration works before proceeding to production.

**Findings from MITS follow-up (2026-06-24):**
- MITS granted Greg access to Elements DEV at `https://dev.umich.elements.symplectic.org/` using Level 1 login.
- Current observed behavior in Elements DEV is deposit failure with HTTP 403.
- Enabling "Automated Metadata Updates" changed the error to HTTP 401.
- Disabling that feature reverted behavior back to HTTP 403.
- MITS requested additional configuration/permission guidance and offered a live troubleshooting call.

**Next investigation checklist (DEV, before production changes):**
- [ ] Use runbook `/.agents/DEEPBLUE-466-DEV-LIVE-TROUBLESHOOTING.md` during the next live Elements DEV troubleshooting session.
- [ ] Reproduce the DEV deposit workflow with the new account access and capture exact timestamp, user, and item used.
- [ ] Confirm the Elements data source `DSpace 7.0+` setting and API/OAI URLs still match the current demo backend endpoints.
- [ ] Verify which REST account is configured in Elements DEV (`deepblue@umich.edu` expected for demo service account) and whether it differs from prior `dbrrds@umich.edu` testing.
- [ ] Verify the configured REST account has required DSpace permissions for deposit target collection access in demo.
- [ ] Request MITS-side error details tied to the failing deposit attempt (status code + endpoint + response body or stack trace).

- [x] Step 1 — Verify demo prerequisites: REST API (`https://backend.demo.deepblue-documents.lib.umich.edu/server/api`) ✓ DSpace 7.6; OAI-PMH (`https://backend.demo.deepblue-documents.lib.umich.edu/server/oai/request`) ✓ HTTP 200; ⚠️ OAI path corrected from `/oai/request` to `/server/oai/request` in `plans/PLAN466DEMO.md` — Elements version, data source status, and admin credentials require manual verification
- [x] Step 2 — Update harvest crosswalk: downloaded → saved to `crosswalks/harvest-demo.xml` → ran `patch_harvest_crosswalk.py` (5 field-source xpath→jsonpath) → ran `fix_harvest_crosswalk_dspace7.py` (fixed expressions, simplified authors/funding, converted 26 object-type-selector conditions to JSONPath, added "Private (in review)" value-map) → `harvest-demo-patched.xml` ready to upload
- [x] Step 3 — Update deposit crosswalk: downloaded → saved to `crosswalks/deposit-demo.xml` → ran `patch_deposit_crosswalk.py` → deposit target 'Michigan Research Experts Deposits' not in demo; substituted 'pacerda Testing ground' (UUID `80ca6e1d-…`) with explanatory comment → `deposit-demo-patched.xml` ready to upload
- [x] Step 3b — Verified DSpace demo readiness with `check_dspace_rt2.py`: all 5 checks PASS (REST API, OAI-PMH, auth as `dbrrds@umich.edu`, collection accessible, workspace item created and deleted); fixed CSRF token rotation bug in script (DSpace 7 rotates CSRF on login and on POST — now captured from response headers)
- [x] Step 4a — Obtained `license.txt` from `/dspace/config/default.license` in the demo pod; saved to `crosswalks/license.txt` — ready to upload to Elements
- [ ] Step 4b — Upload updated `license.txt` (v2.1, "Deep Blue Documents Terms of Use version 2.1", identifier `deepblue-docs-terms-of-use-v2.1`) in the Deposit License section — **waiting for Joanna Thielen to finalise the updated text**; use `deepblue@umich.edu` credentials
- [ ] Step 5 — Reconfigure the demo data source: set the version to `DSpace 7.0+`, API Base URL to `https://backend.demo.deepblue-documents.lib.umich.edu/server`, OAI-PMH URL to `https://backend.demo.deepblue-documents.lib.umich.edu/server/oai/request`, REST credentials; click Update
- [ ] Step 6 — Enable the demo data source; stop then restart the Synchroniser on the Scheduled Jobs page
- [ ] Step 7 — Test harvest: first run `kubectl -n demo exec deploy/backend -- /dspace/bin/dspace oai import | cat` to ensure the OAI feed is current; then turn on verbose logging, run Edit & Test Harvest Crosswalk with a known demo item UUID, review Output tab, let the first harvest complete, review sample records, turn off logging
- [ ] Step 8 — Test deposit: enable Allow Deposit, run Edit & Test Deposit Crosswalk, make a live test deposit into the demo PR collection, confirm the item appears in DSpace and is harvested back into Elements
- [ ] Step 9 — If settings do not take effect: cycle the data source (disable → stop Synchroniser → start Synchroniser → re-enable)
- [ ] Step 10 — Demo sign-off: confirm harvest and deposit are stable, disable verbose logging, record final API Base URL / version / collection UUIDs, confirm with the team that demo is good before proceeding to production
- [ ] Verify with the developer that the task is complete

## DEEPBLUE-466 — Re-establish Symplectic Elements ↔ Deep Blue RT2 Connection
Re-enable and reconfigure the Elements RT2 DSpace integration following the
Elements 7.0 upgrade (March 5–6, 2026) and the earlier DSpace 7.6.0 upgrade
(November 2025). Full plan in `plans/PLAN466.md`.

- [x] Step 1a — Verify production prerequisites (REST API, OAI-PMH): REST API (`https://backend.production.deepblue-documents.lib.umich.edu/server/api`) ✓ DSpace 7.6; OAI-PMH (`https://backend.production.deepblue-documents.lib.umich.edu/server/oai/request`) ✓ HTTP 200 — Elements version and data source status require manual verification with HITS
- [x] Step 1b — Locate production DSpace admin credentials: **`deepblue-elements@umich.edu`** (UUID `57f90d39-…`, name "For Deposit, Symplectic") — dedicated production service account for Elements RT2. Password not in repo; reset via `kubectl -n production exec ... dspace user --modify` if needed. (Legacy note referenced `configuration/DSPACE_ADMIN.md`, now removed.)
- [x] Step 2a — Production harvest crosswalk already downloaded: `crosswalks/dspace-Harvest-XwalkIn-map.xml` (original in repo). Ran both patch scripts → `harvest-production-patched.xml` ready: 0 remaining `select-using="xpath"`, 26 JSONPath conditions, authors/funding/public-url/repository-status all fixed
- [x] Step 3a — Production deposit crosswalk already downloaded: `crosswalks/dspace-Deposit-XwalkOut-map.xml` (DEEPBLUE-497-fixed canonical version; pre-fix original saved as `PRE-DEEPBLUE-497_dspace-Deposit-XwalkOut-map.xml`). Deposit target 'Michigan Research Experts Deposits' **exists** in production (UUID `ee9d8886-9a8f-47d9-99d0-923d687fe381`, confirmed from REST API). Ran patch script → `deposit-production-patched.xml` ready
- [x] Step 4a — `license.txt` already prepared from demo pod (same license text applies to production); file at `crosswalks/license.txt`
- [ ] Step 2b — Upload `harvest-production-patched.xml` to Elements (requires HITS): System Admin → Data Source Management → DSpace (production) → Crosswalk Map Files → Harvest → Upload Harvest Map File
- [ ] Step 3b — Upload `deposit-production-patched.xml` to Elements (requires HITS): Crosswalk Map Files → Deposit → Upload Deposit Map File
- [ ] Step 4b — Upload `license.txt` in the Deposit License section of the production data source in Elements (requires HITS)
- [ ] Step 5 — Reconfigure the production data source: set version to `DSpace 7.0+`, API Base URL to `https://backend.production.deepblue-documents.lib.umich.edu/server`, OAI-PMH URL to `https://backend.production.deepblue-documents.lib.umich.edu/server/oai/request`, REST credentials to `deepblue-elements@umich.edu`; click Update (requires HITS)
- [ ] Step 6 — Enable the production data source; stop then restart the Synchroniser (requires HITS)
- [ ] Step 7 — Test harvest: first run `kubectl -n production exec deploy/backend -- /dspace/bin/dspace oai import | cat` to ensure the OAI feed is current; then verbose logging, Edit & Test Harvest Crosswalk with a known production item UUID, review Output tab, let first harvest complete, review sample records, turn off logging (requires HITS)
- [ ] Step 8 — Test deposit: enable Allow Deposit, run Edit & Test Deposit Crosswalk, make a live test deposit into the PR collection (`4fdfaf57-d4ad-437f-9cf4-a2070e529d6e`), confirm item appears in DSpace and harvests back (requires HITS + Repository Tools license)
- [ ] Step 9 — If settings do not take effect: cycle the data source (disable → stop Synchroniser → start Synchroniser → re-enable) (requires HITS)
- [ ] Step 10 — Production sign-off: confirm harvest and deposit stable, disable verbose logging, notify stakeholders, record final API Base URL / version / collection UUIDs
- [ ] Verify with the developer that the task is complete


## CronJob Stabilisation — Phases 2–5 (planned)
Full plan and background in [`plans/PLANCRONJOBS.md`](plans/PLANCRONJOBS.md).
Phase 1 complete 2026-04-28.

**Phase 2 — Fix `tee` log paths (replace `/dspace/data/log/` with `/tmp/` in all CronJob commands):**
- [ ] Replace `tee /dspace/data/log/clean-discovery` with `tee /tmp/clean-discovery` in all envs
- [ ] Replace `tee /dspace/data/log/oai-cron` with `tee /tmp/oai-cron` in all envs

**Phase 2b — Audit and recover module configs discarded during Phase 5 dspace.cfg refactoring:**
The from-kube files showed Deep Blue Documents loaded 3 extra DSpace module config files not in
the upstream DSpace 7.6 defaults: `replicate.cfg`, `replicate-bagit.cfg`, `replicate-mets.cfg`.
These configure the APTrust preservation replication framework used by the APTrust CronJobs.
With the dspace-cfg Secret deleted in Phase 5, these module includes are gone. Since every
commented-out CronJob will eventually be re-enabled, all required configuration must be
present in the current 3-layer model before any CronJob is uncommented.
- [x] Extract `replicate.cfg`, `replicate-bagit.cfg`, `replicate-mets.cfg` from production pod at `/dspace/config/modules/`
- [x] Diff each against upstream defaults; identify UM-specific overrides
- [x] For any UM override found: add to `lib/deepblue-backend-cm.jsonnet` (Bucket A) or the appropriate `backend-cm.jsonnet` (Bucket B); credentials go to `dspace-secrets`
- [x] Audit ALL other commented-out CronJobs (filter-media, checksum-checker, sub-daily/weekly/monthly, reporting jobs, pubmed-ver2, doi-process) — check whether each needs module config not currently in the 3-layer model
- [x] For APTrust credential keys: verify `perl-environment` Secret already holds them; document in `CLASSIFY.md`
- [x] Update `PLANCRONJOBS.md` with findings from this audit
- [x] Run `python3 dotpy/validate_cm_keys.py` after any ConfigMap additions
- [x] Commit all replicate module config additions (commit `1db988b`)
- [x] Full module diff audit (pod vs upstream image for all 46 module files): 45 byte-for-byte identical; `authentication-oidc.cfg` customised via Layer 3c `oidc-cfg` Secret + startup `cp` — documented in `CLASSIFY.md § Layer 3c` (commit `9860a59`)
- [ ] ⚠️ Developer action: replace "Jose*" placeholder values in `production/backend-cm.jsonnet` (replicate-bagit bag-info contact fields) with real Deep Blue Documents / UM Library contact information before APTrust CronJobs are re-enabled (see PLANCRONJOBS.md Phase 2b for the full table)

**Phase 3 — Fix MTA / email delivery (all environments — affects production too):**
- [ ] File issue in `mlibrary/dspace-containerization`: install `msmtp` as local MTA in backend image
- [ ] Once new image available, update `image_tag_app` and verify email delivery via manual CronJob test

**Phase 4 — Consolidate `cronjob-*.libsonnet` into shared base lib**
- [ ] Create `lib/cronjob-base.libsonnet`; refactor all three env libs as thin mixins

**Phase 5 — Review and re-enable remaining CronJobs (see PLANCRONJOBS.md for full list)**
- [ ] Work through all commented-out CronJobs across all three environments
- [ ] For stats jobs (`prep-logs`, `monthly-report`): implement pod affinity before enabling
- [ ] Verify with the developer that all phases are complete

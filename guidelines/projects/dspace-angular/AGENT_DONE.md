# AGENT_DONE — dspace-angular

## 2026-07-22 — DEEPBLUE-466 migration and guidance import

- Migrated project-root agent files into framework-managed `.agents/` equivalents.
- Added `dspace-angular` to `config/projects.json` and initialized mount + `.agents` link.
- Added `communications/` scaffold support for mounted projects.

## DEEPBLUE-466 implementation commits (source repo history)

- `90a6627c3` — initial plan
- `54c6b93c4` — showPasswordLogin feature implementation
- `531f1e703` — test unblock and spec stabilization

## Notes

- Detailed implementation rationale lives in `PLAN_DSPACE_ANGULAR_PASSWORD_LOGIN.md`.
- Kubernetes follow-up for `DSPACE_AUTH_SHOWPASSWORDLOGIN=true` remains tracked in `AGENT_TODO.md`.


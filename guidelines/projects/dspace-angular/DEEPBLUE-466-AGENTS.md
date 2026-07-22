# DEEPBLUE-466 archived context

This file keeps a minimal archive for the completed `show-password-login` feature.

## Problem

- Demo environment required DSpace password login, but UI filtered password auth out.

## Solution

- Added config flag `auth.showPasswordLogin` (default `false`).
- Login template now uses an exclusive condition to show either password or OIDC method.

## Key commit

- `54c6b93c4` — feature implementation in `mlibrary/dspace-angular`.

## Follow-up

- Kubernetes demo frontend still needs `DSPACE_AUTH_SHOWPASSWORDLOGIN=true`.
- Track remaining work in `AGENT_TODO.md`.


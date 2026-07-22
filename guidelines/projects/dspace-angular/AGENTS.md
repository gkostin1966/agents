# AGENTS.md — dspace-angular

Project-specific rules for `mlibrary/dspace-angular`.
Base framework rules still apply from `guidelines/base/AGENTS.md`.

## Project Context

| Item              | Value                                              |
|-------------------|----------------------------------------------------|
| Repo              | `mlibrary/dspace-angular`                          |
| Framework         | Angular 14 / DSpace 7.6.0                          |
| Language          | TypeScript + HTML templates                        |
| Base branch       | `umich` (customized downstream branch at 7.6.0)    |
| Ticket prefix     | `DEEPBLUE-`                                        |
| Commit convention | `feat\|fix\|chore\|docs\|test: message (DEEPBLUE-NNN)` |

## Task Files

| File                                           | Purpose                          |
|------------------------------------------------|----------------------------------|
| `.agents/AGENT_TODO.md`                        | Active task list                 |
| `.agents/AGENT_DONE.md`                        | Completed task archive           |
| `.agents/PLAN_DSPACE_ANGULAR_PASSWORD_LOGIN.md`| DEEPBLUE-466 implementation plan |
| `.agents/DEEPBLUE-466-PR.md`                   | DEEPBLUE-466 PR draft            |

## Branch Naming

- `umich` is the downstream branch with customizations to the upstream fork at release 7.6.0.
- `show-password-login` maps to `DEEPBLUE-466` (already merged to `umich`).
- New feature branches should be cut from `umich`.

## Test Commands

```shell
npx ng test --include='**/log-in/log-in.component.spec.ts' --watch=false --configuration test --browsers=ChromeHeadless
npx ng test --watch=false --configuration test --browsers=ChromeHeadless
```

## Project-Specific Notes

- Keep communication drafts in `communications/` in the mounted project root.
- Keep framework memory/state files in `.agents/`; do not treat them as app-code changes.

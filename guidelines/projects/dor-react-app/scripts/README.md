# .agents/scripts Conventions — dor-react-app

This directory is for project-local agent helper scripts when working in `mounted-projects/dor-react-app`.

## Purpose

- Keep repetitive helper commands close to the project workflow.
- Allow agent work inside project/devcontainer sessions without host-only paths.
- Separate quick one-off scripts from reusable scripts.

## Layout

- `scripts/local/` — throwaway or ticket-specific helpers.
- `scripts/shared/` — reusable project helpers to keep and review.

## Rules

- Prefer `/tmp/run.py` for one-off scripts unless reuse is likely.
- Promote useful one-off helpers into `scripts/shared/`.
- Use non-interactive commands and append `| cat` for potentially paged output.
- Add a short usage header comment at top of reusable scripts.
- Keep scripts project-safe: no writes outside the project unless explicitly required.

## Examples

```shell
python3 /tmp/run.py | cat
python3 .agents/scripts/shared/my_helper.py | cat
```

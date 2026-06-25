# .agents/scripts Conventions — deepblue-documents-kube

This directory is for project-local agent helper scripts when working in `mounted-projects/deepblue-documents-kube`.

## Purpose

- Keep repetitive helper commands close to the project workflow.
- Allow agent work inside project/devcontainer sessions without host-only paths.
- Separate quick one-off scripts from reusable scripts.

## Layout

- `.agents/scripts/local/` — throwaway or ticket-specific helpers.
- `.agents/scripts/shared/` — reusable project helpers to keep and review.

## Rules

- Prefer `.agents/tmp/run.py` for one-off scripts unless reuse is likely.
- Promote useful one-off helpers into `.agents/scripts/shared/`.
- Use non-interactive commands and append `| cat` for potentially paged output.
- Add a short usage header comment at top of reusable scripts.
- Keep scripts project-safe: no writes outside the project unless explicitly required.

## Shared Scripts

- `.agents/scripts/shared/check_tables.py` — validate Markdown table padding/consistency.
- `.agents/scripts/shared/format_table.py` — rewrite Markdown tables with normalized widths.
- `.agents/scripts/shared/commit.py` — run `git commit -F` using a message file.
- `.agents/scripts/shared/validate_cm_keys.py` — validate encoded backend ConfigMap keys.
- `.agents/scripts/shared/check_dspace_rt2.py` — non-destructive endpoint readiness checks.
- `.agents/scripts/shared/patch_harvest_crosswalk.py` — first-pass `xpath` → `jsonpath` selector patch.
- `.agents/scripts/shared/fix_harvest_crosswalk_dspace7.py` — second-pass deterministic harvest fixes.
- `.agents/scripts/shared/patch_deposit_crosswalk.py` — add collection `id` attributes.
- `.agents/scripts/shared/_gen_rtf.py` — generate an RTF draft template.

## Examples

```shell
python3 .agents/tmp/run.py | cat
python3 .agents/scripts/shared/my_helper.py | cat
python3 .agents/scripts/shared/check_tables.py README.md | cat
python3 .agents/scripts/shared/format_table.py README.md | cat
python3 .agents/scripts/shared/commit.py --dry-run | cat
python3 .agents/scripts/shared/validate_cm_keys.py | cat
python3 .agents/scripts/shared/check_dspace_rt2.py --api-url https://example/api --oai-url https://example/oai | cat
```

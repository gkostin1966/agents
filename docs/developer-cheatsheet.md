# Developer Cheatsheet

Practical daily commands for working in the `agents` framework repo.

## Start of session

```bash
git branch --show-current | cat
git --no-pager status | cat
git --no-pager log --oneline -5 | cat
```

## Check the framework state

```bash
PYTHONPATH=src python3 -m agents_framework.cli scan
PYTHONPATH=src python3 -m agents_framework.cli validate
```

## Regenerate merged guidance for a project

```bash
PYTHONPATH=src python3 -m agents_framework.cli guidelines generate dor-depot
PYTHONPATH=src python3 -m agents_framework.cli prompt generate dor-depot
PYTHONPATH=src python3 -m agents_framework.cli bootstrap dor-depot
```

## Regenerate all configured projects

```bash
PYTHONPATH=src python3 -m agents_framework.cli guidelines generate all
PYTHONPATH=src python3 -m agents_framework.cli prompt generate all
```

## Mount projects from a source root

```bash
PYTHONPATH=src python3 -m agents_framework.cli init-mounts --source-root /path/to/source-root
```

## Run checks before asking for help

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py'
bash scripts/smoke_run.sh
python3 scripts/check_token_budgets.py | cat
```

## Work with mounted projects

```bash
PYTHONPATH=src python3 -m agents_framework.cli run test --projects dor-depot --dry-run
PYTHONPATH=src python3 -m agents_framework.cli run test --projects all
```

## Commit flow

```bash
git --no-pager diff --stat | cat
git --no-pager status | cat
```

- Write commit messages to a file if they are multiline.
- Keep `mounted-projects/` read-only from the framework repo side.
- Mounted projects should expose guidance through `.agents` symlinks into `guidelines/projects/<name>`.


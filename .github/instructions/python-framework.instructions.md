---
applyTo: "src/agents_framework/**/*.py"
---
# Framework Python rules

- Package layout: `src/agents_framework/` (src layout).
- Modules: `cli.py` (dispatch), `config.py` (dataclasses + load), `framework.py` (mounts/scan/run), `merge.py` (shared section merge), `guidelines.py`, `prompts.py`, `validate.py`.
- Always run tests after changes: `PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py'`
- No external deps. Stdlib only.
- Python 3.10+: `list[str]`, `dict[str, str]` — not `typing.List`/`typing.Dict`.
- New module → add to `src/agents_framework/`, import in `cli.py`, add `tests/test_<module>.py`.
- New CLI subcommand → `sub.add_parser(...)` in `build_parser()`, wire `which` key in `main()`, add tests.


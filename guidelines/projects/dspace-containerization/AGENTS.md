# Agent Rules — dspace-containerization (project-specific additions)

> Base: `guidelines/base/AGENTS.md`. Matching `## Heading` here replaces base section.
> Task tracking: `guidelines/projects/dspace-containerization/`

## Task Tracking (TODO.md / DONE.md)

Files: `guidelines/projects/dspace-containerization/TODO.md` and `DONE.md`.

- Record plan in `TODO.md` before executing. Check off (`- [x]`) as completed.
- Every task ends with `- [ ] Verify with the developer that the task is complete`.
- All done → remove from `TODO.md`, prepend timestamped entry to `DONE.md`. Reorder with Python only.

## Docker / Make Conventions

- Primary workflow: `make` targets. Check `make help` or `Makefile` for targets. Key: `make build`, `make up`, `make down`, `make test`.
- **Never `docker build` directly** — always use `docker compose build` or `make build`.
- After build, run `bash tests/smoke.sh` before committing.
- `.env`: copy from `.env.example`, fill required values before `make up`. Never commit `.env`.


# AGENT_QUIZ_ANSWERS — dspace-containerization

> **Do not read this file until you have answered all questions in `AGENT_QUIZ.md`
> and the developer has told you to compare.**

---

## Section 1 — Project Structure and Purpose

**A1.** `dspace-containerization` containerises DSpace (v7+) using Docker and Docker Compose,
enabling local development and CI testing. Services typically include: `backend` (Spring Boot),
`frontend` (Node/React), `db` (PostgreSQL), and `solr` (Solr search).

**A2.** Make targets are defined in `Makefile`. Run `make help` (or read the Makefile directly)
to see all targets. Key targets from `AGENTS.md`: `make build`, `make up`, `make up-all`,
`make down`, `make clean`, `make rebuild`, `make test`.

**A3.** Multiple Dockerfiles:
- `backend.dockerfile` — Spring Boot DSpace backend service
- `frontend.dockerfile` — Node/React DSpace UI frontend
- `db.dockerfile` — PostgreSQL database
- `solr.dockerfile` — Solr search service

Always build through `docker compose build` or `make build`, never `docker build` directly.

**A4.** Copy `.env.example` to `.env` and fill in required values before running `make up`.
`.env` must never be committed.

**A5.** GitHub Actions workflows live in `.github/workflows/`. CI must pass before any
work is declared complete.

---

## Section 2 — Configuration Pattern

**A6.** DSpace property names are encoded for Docker Compose `environment:` keys using the
same `__P__`/`__D__` encoding as the Kubernetes ConfigMap:
- `__P__` encodes a dot (`.`)
- `__D__` encodes a hyphen (`-`)

Example with dot: `dspace.server.url` → `dspace__P__server__P__url`
Example with hyphen: `handle.remote-resolver.enabled` → `handle__P__remote__D__resolver__P__enabled`

**A7.** Both use the `__P__`/`__D__` encoding because DSpace reads configuration from
environment variables injected at startup. The Docker Compose file mirrors what the
Kubernetes ConfigMap (`backend-cm.jsonnet`) provides in production, allowing the same
DSpace startup behavior locally and in-cluster.

**A8.** The smoke test is `tests/smoke.sh`. It verifies basic service availability
(HTTP endpoints return expected responses). It uses `jq` to check JSON fields
(e.g., `"authenticated": false`) rather than exact string matching, making assertions
format-agnostic across DSpace versions.

---

## Section 3 — Task Tracking

**A9.** Task tracking lives in the `agents` repository at
`guidelines/projects/dspace-containerization/`. The two files are `TODO.md` (active tasks)
and `DONE.md` (archived tasks) — note the absence of the `AGENT_` prefix used by other projects.

**A10.** The open task in `TODO.md` is "Scrub Deleted `.cpt` Files from Git History".
It is blocked because: the `.cpt` files are ccrypt-encrypted, and verifying whether they
ever contained real credentials requires the decryption passphrase — which must be confirmed
by the developer before running `git filter-repo` to rewrite history.

---

## Section 4 — Agent Framework Integration

**A11.** Agent files live in the `agents` repository at:
`guidelines/projects/dspace-containerization/`

**A12.**
```shell
PYTHONPATH=src python3 -m agents_framework.cli guidelines generate dspace-containerization
```
Or using the `all` shorthand to regenerate all projects:
```shell
PYTHONPATH=src python3 -m agents_framework.cli guidelines generate all
```

**A13.** The path is called `AGENTS_ROOT`. It is not hardcoded because the `agents`
repository can live at any absolute path depending on the developer's machine, and
hardcoding it would make `AGENT_PROMPT.md` non-portable across different workstations.


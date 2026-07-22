# AGENT_QUIZ_ANSWERS — dspace-containerization

> **Do not read this file until you have answered all questions in `AGENT_QUIZ.md`
> and the developer has told you to compare.**

---

## Section 1 — Project Structure and Purpose

**A1.** `dspace-containerization` is the containerization and deployment infrastructure for
Deep Blue Documents (U-M Library), built on DSpace 7+. It supports local development
and CI testing with Docker/Docker Compose. The targeted upstream patch level called out
in `README.md` is **DSpace 7.6.0** (`DSPACE_VERSION=7.6`). Core services are `backend`
(Spring Boot), `frontend` (Angular SSR app), `db` (PostgreSQL), and `solr` (Solr).
Optional services are `apache` and `express`.

**A2.** Make targets are defined in `Makefile`, with `help` as the default goal.
Run `make help` (or simply `make`) to see available targets. Key targets called out in
`AGENTS.md`: `make build`, `make up`, `make down`, `make test`.

**A3.** Multiple Dockerfiles:
- `Dockerfile` — shared source image (`dspace-containerization-source`)
- `backend.dockerfile` — Spring Boot DSpace backend service
- `frontend.dockerfile` — Angular SSR DSpace UI frontend
- `db.dockerfile` — PostgreSQL database
- `solr.dockerfile` — Solr search service
- `apache.dockerfile` — optional Apache service
- `express.dockerfile` — optional Express metrics service

Always build through `docker compose build` or `make build`, never `docker build` directly.

**A4.** Copy `.env.example` to `.env` and fill in required values before running `make up`.
`.env` must never be committed.

**A5.** GitHub Actions workflows live in `.github/workflows/`.
Before declaring work complete, CI should pass and local smoke checks should pass
for changed build/runtime behavior (see `make test` / `tests/smoke.sh`).

---

## Section 2 — Configuration Pattern

**A6.** DSpace property names are encoded for Docker Compose `environment:` keys by
replacing dot separators with `__P__`:
- `__P__` encodes a dot (`.`)

Example with dot: `dspace.server.url` -> `dspace__P__server__P__url`
Example with hyphen-containing segment (hyphen preserved, dots encoded):
`rest.cors.allowed-origins` -> `rest__P__cors__P__allowed-origins`

**A7.** Both use the same env-var key encoding pattern because DSpace reads configuration from
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
It is blocked/deferred because it is explicitly a post-merge cleanup action that must not
block `DEEPBLUE-466/Refactor` from merging. (Related credential/passphrase verification is
tracked context, but the explicit blocker in `TODO.md` is the post-merge dependency.)

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


# AGENT_QUIZ — dspace-containerization

> Answer every question below by looking up the answer in the actual project files.
> Do **not** read `AGENT_QUIZ_ANSWERS.md` until you have answered all questions and the
> developer has told you to compare.
>
> Write your answers inline under each question before moving on.

---

## Section 1 — Project Structure and Purpose

**Q1.** What is the primary purpose of the `dspace-containerization` repository?
What DSpace version does it target, and what services does it run?

**A1.** It is the containerization and deployment infrastructure for Deep Blue Documents (U-M Library's DSpace-based repository), and acts as the source of truth for building/deploying that stack. It targets DSpace **7.6.0** (configured as `DSPACE_VERSION=7.6`, with README noting upstream patch target 7.6.0). Core services are `db`, `solr`, `backend`, and `frontend`; optional services are `apache` and `express`.

**Q2.** How are Make targets organised? What command shows all available targets?
List the key targets mentioned in `AGENTS.md`.

**A2.** Targets are organized around a default `help` goal (`.DEFAULT_GOAL := help`) with documented workflow targets in `Makefile`. Run `make help` (or just `make`) to see available targets. `AGENTS.md` calls out key targets: `make build`, `make up`, `make down`, and `make test`.

**Q3.** The project has multiple Dockerfiles for different services. List them and
state which service each one builds.

**A3.**
- `Dockerfile` - shared source image (`dspace-containerization-source`)
- `frontend.dockerfile` - `frontend`
- `backend.dockerfile` - `backend`
- `solr.dockerfile` - `solr`
- `db.dockerfile` - `db`
- `apache.dockerfile` - optional `apache`
- `express.dockerfile` - optional `express`

There are also parallel Dockerfiles under `dspace/` and `dspace-uid/` for Kubernetes/OpenShift deployment variants.

**Q4.** Where do environment variables go before running `make up`? What file must
never be committed?

**A4.** Copy `.env.example` to `.env` and set values there before `make up`/build steps. The `.env` file must never be committed.

**Q5.** Where do CI workflows live and what must pass before work is considered complete?

**A5.** CI workflows live in `.github/workflows/` (primary stack validation workflow: `.github/workflows/ci.yml`). Before considering work complete, smoke tests must pass (`bash tests/smoke.sh`, typically via `make test` in full flow).

---

## Section 2 — Configuration Pattern

**Q6.** The project uses an env-var based configuration approach instead of `local.cfg`.
How are DSpace property names encoded as Docker Compose environment variable keys?
Give one example of a property with a dot and one with a hyphen.

**A6.** DSpace property keys are encoded by replacing each `.` with `__P__` in the env-var key name.
- Dot example: `dspace.server.url` -> `dspace__P__server__P__url`
- Hyphen example (hyphen preserved, dots encoded): `rest.cors.allowed-origins` -> `rest__P__cors__P__allowed-origins`

**Q7.** What is the relationship between the Docker Compose `environment:` config and
the Kubernetes ConfigMap (`backend-cm.jsonnet`) config? Why do they use the same key encoding?

**A7.** They represent the same runtime configuration pattern in different environments: local Docker Compose sets backend properties via env vars, while production/staging injects corresponding values from Kubernetes ConfigMap/Secrets. They use the same encoding so the backend receives consistent property keys across local and cluster deployments.

**Q8.** What is the smoke test script and what does it verify?
What tool does it use to make assertions format-agnostic?

**A8.** The smoke test script is `tests/smoke.sh`. It verifies backend API/health endpoints, Solr system/core readiness, and frontend/SSR responses. It uses `jq` for JSON assertions (with grep fallback in the script), making checks format-agnostic.

---

## Section 3 — Task Tracking

**Q9.** Where does task tracking for this project live, and what are the two tracking file names
(note: they differ from the `AGENT_TODO.md`/`AGENT_DONE.md` pattern used by other projects)?

**A9.** Task tracking lives at `guidelines/projects/dspace-containerization/` in the agents repo (mounted locally as `.agents/` in this workspace). The files are `TODO.md` and `DONE.md`.

**Q10.** What is the open task listed in `TODO.md`, and why is it blocked?

**A10.** The open blocked task is **"Scrub Deleted `.cpt` Files from Git History"**. It is explicitly deferred until after `DEEPBLUE-466/Refactor` merges; that post-merge dependency is the blocking condition.

---

## Section 4 — Agent Framework Integration

**Q11.** Where do agent guideline files for this project live in the `agents` repository?

**A11.** `guidelines/projects/dspace-containerization/`

**Q12.** What command generates the merged `AGENTS.md` for this project?

**A12.** `PYTHONPATH=src python3 -m agents_framework.cli guidelines generate dspace-containerization`

**Q13.** The `AGENT_PROMPT.md` for this project asks the agent to request a path at session
start. What is that path called, and why is it not hardcoded?

**A13.** The path is `AGENTS_ROOT`. It is not hardcoded because `.agents` is a local symlink/mount to an agents-repo location outside this project, so the absolute location can vary by environment.


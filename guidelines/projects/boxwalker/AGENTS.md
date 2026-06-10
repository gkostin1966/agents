# Agent Rules — boxwalker (project-specific additions)

> Base: `guidelines/base/AGENTS.md`. Matching `## Heading` here replaces base section.
> Task tracking primary path: `.agents/tasks/` (fallback: `AGENTS_ROOT/guidelines/projects/boxwalker/tasks/`)

## Session State (`tasks/BW-nnn/STATUS.md`)

At session start: (1) identify ticket from branch name (e.g. `BW-42/my-feature` → `BW-42`), (2) read `tasks/BW-nnn/STATUS.md` in full, (3) cross-check open subtasks against `TODO.md` — `TODO.md` is authoritative.

During session: update `STATUS.md` when a subtask completes, a plan changes, or a key decision is made.

End of session: update Last Updated, Recent Activity, Next Steps. Commit `STATUS.md` in final commit.

| Section         | Contents                                                               |
|-----------------|------------------------------------------------------------------------|
| Last Updated    | ISO date + one-line session summary                                    |
| Current Branch  | Active git branch name; brief note on other local branches if relevant |
| Open Tasks      | Copy of unchecked subtasks from `TODO.md`; key files for each task     |
| Open Plans      | Table of files in `tasks/BW-nnn/plans/` with purpose and status       |
| Recent Activity | Bullet list of meaningful changes made in the most recent session      |
| Key Context     | Decisions, design notes, or gotchas the next agent needs to understand |
| Next Steps      | Ordered list of what to do next, specific enough to act on immediately |

## Task Tracking (`tasks/BW-nnn/TODO.md` / `tasks/BW-nnn/DONE.md`)

Primary location: `.agents/tasks/BW-nnn/` (TODO.md, DONE.md, STATUS.md, plans/).

Fallback location when `.agents` is unavailable: `AGENTS_ROOT/guidelines/projects/boxwalker/tasks/BW-nnn/`.

New ticket: `mkdir -p .agents/tasks/BW-nnn/plans` + create TODO.md + STATUS.md + row in `.agents/tasks/README.md`.

- Record plan in `TODO.md` before executing. Check off (`- [x]`) as completed.
- Every task ends with `- [ ] Verify with the developer that the task is complete`.
- All done → create `tasks/BW-nnn/DONE.md` with timestamp + summary + checklist.
- Complete ticket (after PR merges): `git mv .agents/tasks/BW-nnn .agents/archive/BW-nnn`
- Reorder subtasks with Python only — never string-replace.

## Ruby on Rails Conventions

- **All application commands run inside the Docker container.** Never against system Ruby/Node.
- Start stack: `docker compose up` (starts `app`, `solr`, `zookeeper`).
- After first `docker compose up`, initialize Solr collection: `/bin/bash ./solr/dev-init.sh`
- **RuboCop before committing Ruby files**:
  - Auto-fix: `docker compose exec app bundle exec rubocop -a | cat`
  - Check: `docker compose exec app bundle exec rubocop | cat`
- **Tests**: `docker compose exec app bundle exec rails test | cat`
- **Rails console**: `docker compose exec app bundle exec rails console`
- **Ruby version**: 3.4.9 (see `.ruby-version` and `Dockerfile ARG RUBY_VERSION`).
- **Rails version**: ~> 8.1.3 (see `Gemfile`).
- **Database**: SQLite 3 (see `Gemfile`; `db:prepare` runs automatically in `docker-entrypoint`).
- **Solr**: version 9.7, SolrCloud mode with ZooKeeper. Collection name: `blacklight-collection`. Config dir: `solr/conf/`.
- `SOLR_URL` env var: `http://solr:8983/solr/blacklight-collection` (set in `compose.yml`).


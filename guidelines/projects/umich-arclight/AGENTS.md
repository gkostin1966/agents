# Agent Rules — umich-arclight (project-specific additions)

> Base: `guidelines/base/AGENTS.md`. Matching `## Heading` here replaces base section.
> Task tracking: `guidelines/projects/umich-arclight/tasks/`

## Session State (`tasks/ARC-nnn/STATUS.md`)

At session start: (1) identify ticket from branch name (e.g. `ARC-123/my-feature` → `ARC-123`), (2) read `tasks/ARC-nnn/STATUS.md` in full, (3) cross-check against `TODO.md` — `TODO.md` is authoritative.

During session: update `STATUS.md` when a subtask completes, plan changes, or key decision made.

End of session: update Last Updated, Recent Activity, Next Steps. Commit `STATUS.md` in final commit.

| Section         | Contents                                                               |
|-----------------|------------------------------------------------------------------------|
| Last Updated    | ISO date + one-line session summary                                    |
| Current Branch  | Active git branch name; brief note on other local branches if relevant |
| Open Tasks      | Copy of unchecked subtasks from `TODO.md`; key files for each task     |
| Open Plans      | Table of files in `tasks/ARC-nnn/plans/` with purpose and status       |
| Recent Activity | Bullet list of meaningful changes made in the most recent session      |
| Key Context     | Decisions, design notes, or gotchas the next agent needs to understand |
| Next Steps      | Ordered list of what to do next, specific enough to act on immediately |

## Task Tracking (`tasks/ARC-nnn/TODO.md` / `tasks/ARC-nnn/DONE.md`)

Files live at `guidelines/projects/umich-arclight/tasks/ARC-nnn/` (TODO.md, DONE.md, STATUS.md, plans/).

New ticket: `mkdir -p guidelines/projects/umich-arclight/tasks/ARC-nnn/plans` + create TODO.md + STATUS.md + row in `tasks/README.md`.

- Record plan in `TODO.md` before executing. Check off (`- [x]`) as completed.
- Every task ends with `- [ ] Verify with the developer that the task is complete`.
- All done → create `tasks/ARC-nnn/DONE.md` with timestamp + summary + checklist.
- Complete ticket: `git mv guidelines/projects/umich-arclight/tasks/ARC-nnn guidelines/projects/umich-arclight/archive/ARC-nnn`
- Reorder subtasks with Python only — never string-replace.

## Ruby on Rails Conventions

- **All application commands must run inside the Docker container.** Never against system Ruby/Node. Prefix: `docker-compose exec -- app <command>`
- **RuboCop before committing Ruby files**: `docker-compose exec -- app bundle exec rubocop | cat`
  Auto-fix: `docker-compose exec -- app bundle exec rubocop -a | cat`
- **JS lint**: `docker-compose exec -- app yarn lint | cat`
- **Tests**: `docker-compose exec -- app bundle exec rake test | cat` and `docker-compose exec -- app bundle exec rspec | cat`
- **Run app**: `docker-compose up -d` then `docker-compose exec -- app bundle exec rails s -b 0.0.0.0` → `http://localhost:3000/`
- **Background jobs (Resque)**: monitor at `http://localhost:8080/overview`. Restart: `docker-compose restart resque`.
- **Key config files**: `config/repositories.yml` (institution slugs), `config/blacklight.yml` (Solr URL), `config/database.yml` (Postgres, overridden by `DATABASE_URL`), `lib/dul_arclight.rb` (`FINDING_AID_DATA` default: `/data`).


# Session Status — deepblue

> Last updated: 2026-07-30
> Branch: `gkostin`
> Ticket: none (personal dev setup branch)

## Session Summary

This session completed initial local development environment setup from a clean
clone on macOS (arm64, macOS Tahoe). All four services were verified healthy
before the session ended.

## What Was Done

### Gem/Bundle Setup
- Commented out auto-execution block in `Gemfile` (lines 54–57) before `bundle install`
- Created `.bundle/config` with required native build flags for `mysql2`, `posix-spawn`, `libxml-ruby`, `unicode`
- Installed `mysql2 0.5.6` with explicit OpenSSL and zstd linker flags
- Ran `bundle install` successfully — 431 gems installed

### Database / Hyrax Bootstrap
- `bundle exec rails db:migrate` — all migrations applied, `db/schema.rb` updated
- `bundle exec rake hyrax:default_collection_types:create`
- Created user `gkostin@umich.edu` via `rails runner`
- Created default admin set "DataSet Admin Set" via `Hyrax::AdminSetCreateService`
- Added `gkostin@umich.edu` to `admin` section in `config/role_map.yml`

### fcrepo_wrapper Compatibility Fixes (applied to `.bundle` local gem)
- Added `require 'open-uri'` and changed `open(url,` → `URI.open(url,` in `downloader.rb`
- Replaced all `File.exists?` → `File.exist?` in `configuration.rb`, `instance.rb`, `md5.rb`

### Solr Startup Fix (applied to `tmp/solr-development/bin/solr`)
- Removed deprecated CMS JVM GC flags incompatible with modern Java:
  `-XX:+UseConcMarkSweepGC`, `-XX:+CMSScavengeBeforeRemark`, `-XX:+UseCMSInitiatingOccupancyOnly`,
  `-XX:CMSInitiatingOccupancyFraction=50`, `-XX:CMSMaxAbortablePrecleanTime=6000`,
  `-XX:+CMSParallelRemarkEnabled`

### Tools Added
- `bin/dev-stack` — start/status helper for Redis, Fedora, Solr, and Rails
- `SETUP_NOTES.md` — full setup walkthrough with verified commands and caveats
- `STACK_HEALTH.md` — service health verification guide

### Commits Made
- `chore(setup): finalize local dev bootstrap changes` — `Gemfile`, `config/role_map.yml`, `db/schema.rb`
- Pending commit: `bin/dev-stack`, `SETUP_NOTES.md`, `STACK_HEALTH.md`

## Current Stack Health (verified end of session)

| Service | Port | Endpoint | Status |
|---------|------|----------|--------|
| Redis   | 6379 | —        | up (PONG) |
| Fedora  | 8984 | `/rest`  | HTTP 200 |
| Solr    | 8983 | `/solr/` | HTTP 200 |
| Rails   | 3000 | `/data/` | HTTP 200 |

## Key Configuration Facts

| Item | Value |
|------|-------|
| Ruby version | `3.3.10` |
| Rails relative URL root | `/data` (verified in `Settings.relative_url_root`) |
| App landing URL (dev) | `http://localhost:3000/data/` |
| Hyrax app mount | `/data/` scope via `config/routes.rb` conditional on `Settings.relative_url_root` |
| Admin user email | `gkostin@umich.edu` |
| Fedora requires | Java 8 (`temurin@8`) — newer JDK caused 503 throughout session |
| `bin/dev-stack` logs | `log/fcrepo_wrapper.out`, `log/solr_wrapper.out`, `log/rails-server.out`, `log/redis-server.out` |

## Pending Manual UI Steps

The following must be completed in the browser UI at `http://localhost:3000/data/`:

1. Edit default admin set:
   - Click **Allow Everyone to Deposit**
   - Set workflow to **mediated** (last radio button)
2. Create a new admin collection named `Draft works Admin Set`
   - Set workflow to **draft** (second radio button)

## Pending Commits

Two new files need to be staged and committed:

```zsh
cd "/Users/gkostin/GitHub/mlibrary/deepblue"
git add bin/dev-stack SETUP_NOTES.md STACK_HEALTH.md
git commit -m "docs(setup): add repeatable local dev stack helper and setup notes" | cat
```

## Notes for Next Agent

- `.bundle/` and `tmp/solr-development/` patches are environment-local; they may
  need re-application after clean bundle installs or solr-development resets.
- `fcrepo_wrapper` 0.9.0 is incompatible with Ruby 3.3 out of the box; compatibility
  patches were applied manually to the local gem copy under `.bundle/`.
- Always run `./bin/dev-stack status` at session start before any code work.
- The correct app URL is `http://localhost:3000/data/` (trailing slash), not `/data.`.


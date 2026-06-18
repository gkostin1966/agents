# ARC-139 — STATUS

## Last Updated
2026-06-18 — Developer verified jobs-to-services refactor completion; ARC-139 moved to Developer Verified.

## Current Branch
ARC-139-IngestAutomationJob

## Open Tasks
- None (all TODO subtasks are checked)

## Open Plans
| File       | Purpose                      | Status      |
|------------|------------------------------|-------------|
| (none yet) | Document changes are in TODO | Completed   |

## Recent Activity
- Developer confirmed the jobs-to-services refactor task is complete.
- Marked final verification subtask complete in `.agents/tasks/ARC-139/TODO.md` and set `ARC-139` status to `Developer Verified` in `.agents/tasks/README.md`.
- Moved `lib/box/traject/ead2_config.rb` to `config/traject/ead2_config.rb` and removed the legacy lib copy to avoid Zeitwerk constant autoload mismatch.
- Updated `app/services/finding_aids/index_from_ead.rb` to load traject config from `config/traject/ead2_config.rb`.
- Rebuilt the app image and verified Rails boots in-container (`rails runner "puts :boot_ok"` -> `boot_ok`).
- Ran targeted specs in test mode and resolved service spec harness issues; final run passed with `28 examples, 0 failures`.
- Updated ARC-139 summary/title metadata in `.agents/tasks/README.md` and `.agents/tasks/ARC-139/TODO.md` so task descriptors match the expanded refactor scope.
- Added formal ARC-139 refactor checklist and completed extraction of business logic from all jobs into new service objects under `app/services/`.
- Updated all job classes in `app/jobs/` to keep orchestration in `perform` and delegate to service objects.
- Updated all job specs in `spec/jobs/` to validate queueing and service delegation.
- Added focused service specs under `spec/services/` for `Solr::BuildSuggest`, `FindingAids::DeleteFromIndex`, `FindingAids::IndexFromEad`, `FindingAids::IngestRecord`, `FindingAids::PackageArtifact`, and `IngestAutomation::Dispatch`.
- Attempted in-container spec execution via `docker compose exec` and `docker compose run --rm`; runs are blocked by existing app boot errors (`Zeitwerk::NameError` for `lib/box/traject/ead2_config.rb` and follow-on `FrozenError` during Rails initialization).
- Replaced the prior loose follow-up list with a formal multi-step jobs-to-services refactor checklist in `.agents/tasks/ARC-139/TODO.md`.
- Developer requested follow-up work before PR and asked to add job specs for all `app/jobs/` classes.
- Reopened ARC-139 by adding new unchecked subtasks to `.agents/tasks/ARC-139/TODO.md` for job-spec implementation, validation, and developer verification.
- Set `.agents/tasks/README.md` ticket status for `ARC-139` back to `Open` for the reopened work.
- Developer confirmed the follow-up CSS warning reduction task is complete.
- Marked final verification subtask complete in `.agents/tasks/ARC-139/TODO.md`.
- Updated `.agents/tasks/README.md` status for `ARC-139` to `Developer Verified`.
- Refreshed `.agents/tasks/ARC-139/DONE.md` with full completion checklist and files-updated list.
- Updated `AGENT_QUIZ.md` Q8: replaced "three services" premise with "list every service" to match current `compose.yml`.
- Updated `AGENT_QUIZ_ANSWERS.md` A8: expanded table from 3 rows (app/solr/zookeeper) to all 6 services with correct ports (app:3000, redis:6379, resque:none, resque-web:5678, solr:8983, zookeeper:2181).
- Updated `AGENTS.md` § Ruby on Rails Conventions "Start stack" line to list all six services instead of the outdated three.
- Created task directory `.agents/tasks/ARC-139/` with `TODO.md`, `STATUS.md`, and `plans/`.
- Confirmed quiz mismatch points from prior self-grade (`Q16`, `Q17`).
- Updated `.agents/AGENTS.md` to define missing-ticket bootstrap behavior and explicit archive move command.
- Updated `.agents/AGENT_PROMPT.md` startup workflow to require creating missing task files.
- Updated `.agents/AGENT_QUIZ.md` and `.agents/AGENT_QUIZ_ANSWERS.md` to grade active tickets from live state.
- Developer confirmed the onboarding/documentation updates are acceptable.
- Added a follow-up task to suppress dependency-origin Sass deprecation warnings.
- Updated `package.json` `build:css:compile` with `--quiet-deps` and verified via `yarn build:css`.
- Confirmed color-function deprecation spam from Bootstrap dependencies is suppressed; remaining warnings are top-level `@import` deprecations.
- Updated `package.json` `build:css:compile` with `--silence-deprecation=import`.
- Re-ran `yarn build:css`; compile completed with no Sass deprecation warning output.
- Added `//= link_tree ../../javascript .js` to `app/assets/config/manifest.js` to resolve importmap asset lookup for `application.js`.
- Attempted container verification via `docker compose exec app ... rails runner`, but `docker compose` failed because `.env` is missing in this workspace.
- Developer ran `bin/rails runner 'puts ActionController::Base.helpers.asset_path("application.js")'` and confirmed digest asset output.
- Added `//= link blacklight/bookmark_toggle.js` to `app/assets/config/manifest.js`.
- Verified with `bin/rails runner 'puts ActionController::Base.helpers.asset_path("blacklight/bookmark_toggle.js")'` returning a digest asset path.
- Added `//= link blacklight/button_focus.js` to `app/assets/config/manifest.js`.
- Verified with `bin/rails runner 'puts ActionController::Base.helpers.asset_path("blacklight/button_focus.js")'` returning a digest asset path.
- Added `//= link blacklight/checkbox_submit.js` to `app/assets/config/manifest.js`.
- Verified with `bin/rails runner 'puts ActionController::Base.helpers.asset_path("blacklight/checkbox_submit.js")'` returning a digest asset path.
- Replaced one-off `blacklight/*.js` links in `app/assets/config/manifest.js` with initializer-generated string entries in `config/initializers/assets.rb`.
- Verified `blacklight/bookmark_toggle.js`, `blacklight/button_focus.js`, and `blacklight/checkbox_submit.js` all resolve to digest asset paths after the initializer change.
- Added `.github/workflows/sync-repositories-yml.yml` to sync `config/repositories.yml` from `mlibrary/boxwalker` on schedule/manual run.
- Validated the new workflow YAML parses successfully with Ruby `YAML.load_file`.
- Updated `.devcontainer/compose.yml` environment to set `BUNDLE_PATH=/rails/vendor/bundle`, `BUNDLE_APP_CONFIG=/rails/.bundle`, and `BUNDLE_DISABLE_SHARED_GEMS=true`.
- Updated `.devcontainer/devcontainer.json` `postCreateCommand` to write local Bundler config before `bin/setup`.
- Validated `.devcontainer/compose.yml` and `.devcontainer/devcontainer.json` syntax.

## Key Context
- The quiz should grade against current repository state, not bootstrap assumptions.
- Archive guidance must be explicitly present in `AGENTS.md` if the answer key requires it.

## Verification Evidence
- Command: `git --no-pager branch --show-current && git --no-pager status` -> confirmed branch `ARC-139-IngestAutomationJob` with clean working tree before closeout updates.
- Command: `read_file` on `.agents/tasks/ARC-139/TODO.md` and `.agents/tasks/ARC-139/STATUS.md` -> verified only one remaining unchecked subtask before developer confirmation.
- Developer confirmation: received explicit confirmation in session chat that the warning reduction change is complete.
- Command: `docker compose exec app bundle exec rspec spec/jobs spec/services | cat` -> failed with `service "app" is not running`.
- Command: `docker compose up -d | cat` and `docker compose build app | cat` -> stack/app image started/rebuilt successfully.
- Command: `docker compose run --rm app bundle exec rspec spec/jobs/*_spec.rb spec/services/**/*_spec.rb | cat` -> failed during Rails boot with `Zeitwerk::NameError` (`expected file /rails/lib/box/traject/ead2_config.rb to define constant Box::Traject::Ead2Config`) and follow-on `FrozenError` in Rails initialization.
- Command: `docker compose run --rm app ruby -c app/jobs/*.rb app/services/**/*.rb | cat` -> `Syntax OK` for refactored job files and new service files.
- Command: `docker compose run --rm app bundle exec rails runner "puts :boot_ok" | cat` -> `boot_ok` after moving traject config and rebuilding.
- Command: `docker compose run --rm -e RAILS_ENV=test app bundle exec rspec spec/jobs/*_spec.rb spec/services/**/*_spec.rb | cat` -> `28 examples, 0 failures`.
- Developer confirmation: explicit in-session approval to close out ARC-139.
- Remaining unverified scope: post-merge archive step.

## Next Steps
1. After the related PR merges, archive with `git mv .agents/tasks/ARC-139 .agents/archive/ARC-139`.


# ARC-139 — Harden agent onboarding docs
## Plan
- [x] Review `.agents/AGENT_QUIZ.md`, `.agents/AGENT_QUIZ_ANSWERS.md`, and `.agents/AGENTS.md` for ambiguity and drift
- [x] Update quiz and answer key wording so live task state and archive behavior are unambiguous
- [x] Update supporting onboarding docs to prevent branch/task bootstrap confusion
- [x] Verify docs are internally consistent and reference the same archive workflow
- [x] Verify with the developer that the task is complete
- [x] Add `--quiet-deps` to the Sass compile command in `package.json` to suppress dependency deprecation warnings
- [x] Run `yarn build:css` and confirm dependency color-function warning spam is suppressed
- [x] Add `--silence-deprecation=import` to Sass compile command to suppress remaining import deprecation warnings
- [x] Run `yarn build:css` and confirm import deprecation warnings are suppressed
- [x] Fix `AssetNotPrecompiledError` for `application.js` by linking `app/javascript` in `app/assets/config/manifest.js`
- [x] Verify `application.js` resolves via `bin/rails runner 'puts ActionController::Base.helpers.asset_path("application.js")'`
- [x] Fix `AssetNotPrecompiledError` for `blacklight/bookmark_toggle.js` by linking it in `app/assets/config/manifest.js`
- [x] Verify `blacklight/bookmark_toggle.js` resolves via `bin/rails runner 'puts ActionController::Base.helpers.asset_path("blacklight/bookmark_toggle.js")'`
- [x] Fix `AssetNotPrecompiledError` for `blacklight/button_focus.js` by linking it in `app/assets/config/manifest.js`
- [x] Verify `blacklight/button_focus.js` resolves via `bin/rails runner 'puts ActionController::Base.helpers.asset_path("blacklight/button_focus.js")'`
- [x] Fix `AssetNotPrecompiledError` for `blacklight/checkbox_submit.js` by linking it in `app/assets/config/manifest.js`
- [x] Verify `blacklight/checkbox_submit.js` resolves via `bin/rails runner 'puts ActionController::Base.helpers.asset_path("blacklight/checkbox_submit.js")'`
- [x] Replace one-off Blacklight manifest links with initializer-managed precompile entries generated from `node_modules/blacklight-frontend/app/javascript/blacklight/*.js`
- [x] Verify `blacklight/bookmark_toggle.js`, `blacklight/button_focus.js`, and `blacklight/checkbox_submit.js` resolve after initializer change
- [x] Add a GitHub Action that syncs `config/repositories.yml` from `mlibrary/boxwalker`
- [x] Verify the sync workflow YAML is valid and follows existing repo conventions
- [x] Configure devcontainer Bundler settings to install gems in a user-writable project path
- [x] Validate `.devcontainer/compose.yml` and `.devcontainer/devcontainer.json` syntax after Bundler configuration changes
- [ ] Verify with the developer that the follow-up CSS warning reduction change is complete


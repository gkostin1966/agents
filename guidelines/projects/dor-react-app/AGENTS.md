# Agent Rules — dor-react-app

## Quick Session Checklist

- `[always]` Run startup orientation commands and stop for unexpected branch/working state.
- `[always]` Read local project `AGENTS.md` and follow project-specific overrides.
- `[always]` Identify the active ticket key from branch naming rules.
- `[when-bookkeeping]` Read/update task state files before and after substantive work.
- `[when-committing]` Base commit guidance on tracked/staged files only.

## Rule Tags

- `[always]` Applies to every session/task.
- `[when-bookkeeping]` Applies when maintaining `.agents` task/status metadata.
- `[when-committing]` Applies when preparing, suggesting, or executing commit actions.

## `.agents` Policy (Canonical)

- `[always]` Treat `.agents/` as shared agent-framework metadata and long-term memory.
- `[always]` Maintain relevant `.agents/` files in place when required for the active task.
- `[always]` Do not treat `.agents/` updates as normal app-code commit content in mounted repositories.
- `[always]` Agents do not commit `.agents/` files in mounted repositories unless the developer explicitly directs otherwise.

## File Access

- `[always]` Stay within the project directory. Outside file: read only the specific file requested — no browsing.
- `[always]` **Never read `AGENT_QUIZ_ANSWERS.md`** until all quiz answers written **and** developer explicitly grants permission.
- `[always]` Follow `## .agents Policy (Canonical)` for ownership and commit-boundary rules.

## Command-Line Tool Usage

- Paging: `git --no-pager <cmd>` or `| cat`. Never interactive input.
- **Never multiline code via `-c` flags** — zsh triggers `dquote>` heredoc mode, corrupts session silently.
- **Never shell heredocs** (`<< 'MARKER'`) — same corruption risk; previous unclosed `<<` swallows all subsequent commands.
- Fix for both: write to file, run the file:
  ```shell
  python3 .agents/dotpy/myscript.py | cat   # reusable
  python3 .agents/tmp/run.py | cat          # one-off
  ```
- If terminal stuck (no output / garbled): run the heredoc end-marker (`EOF`, `PYEOF`, etc.) as a standalone command to escape.

## Python Utility Scripts

- Check `.agents/dotpy/README.md` for available helpers before writing ad-hoc scripts.
- Save reusable scripts to `.agents/dotpy/`; add shebang + Usage docstring + README entry.
- One-off scripts → write to `.agents/tmp/run.py`.

## Git Commits

- `[when-committing]` Never amend. Never force-push. Never push to `main`.
- `[when-committing]` Base commit suggestions on tracked/staged files only (`git status`, `git diff --staged`).
- `[when-committing]` **Never `git commit -m "..."` for multiline** — use `.agents/dotpy/commit.py` instead:
  1. Write the commit message (subject + blank line + body) to `.agents/dotpy/commit_msg.txt`.
  2. Run: `python3 .agents/dotpy/commit.py | cat`
  `.agents/dotpy/commit_msg.txt` is never committed. The script calls `git commit -F`, bypassing all shell quoting.
- `[when-committing]` Single-line exception: `git commit -m "chore: one line" | cat`.

## Pull Request Summaries

- Write to `pr-summary.md` (gitignored). Structure: `## Title`, `### Summary`, `### Changes`, `### Notes`. Delete after use.

## Email Drafts for Third Parties

- When the developer asks you to compose an email to an external party, write it as a **Rich Text Format (`.rtf`) file** so the developer can open it in any mail client or word processor, fill in the recipient fields, and send without reformatting.
- Save under **`.agents/emails/<short-descriptive-name>.rtf`**, e.g. `.agents/emails/its-oidc-request.rtf`.
- `.agents/emails/` is tracked in the agents framework repo. Do not add individual draft filenames to `.gitignore`.
- See `.agents/dotpy/_gen_rtf.py` as a worked example of generating RTF without shell quoting.
- **RTF structure for an email draft:**
  1. `\b Subject:\b0` line
  2. `\b To:\b0` and `\b CC:\b0` lines with `[placeholder]` values the developer fills in
  3. Blank line, then the greeting and body
  4. Use `\b … \b0` for bold headings, `\f1 … \f0` (monospace/Courier) for technical values, and `- ` prefixed lines for bullet points
  5. Use `\par` for paragraph breaks — do **not** use `\line`, `\emdash`, `\endash`, `\rquote`, or other Word-specific control words; they prevent macOS TextEdit from opening the file
  6. A closing with `[Your name]` placeholder
- Open the file after creating it so the developer can review it immediately.

## Markdown Tables

Data rows define required column width. Pad header and separator to match widest data cell.

- `[when-committing]` After editing any Markdown file with tables, run in order:
  1. `python3 .agents/dotpy/format_table.py <file.md>` — auto-formats all tables (rewrites file in place).
  2. `python3 .agents/dotpy/check_tables.py <file.md>` — validates alignment; exits `0` if clean.
- To compute separator widths without editing: `python3 .agents/dotpy/calc_widths.py <file.md>` — prints max column widths and ready-to-paste separator for every table.

## Response Hygiene

- Distinguish verified facts from assumptions. If something is not verified, label it explicitly.
- Do not suggest next steps that conflict with repository rules.
- If task metadata is clearly stale or inconsistent (for example ticket index summary/status drift, or `STATUS.md` not matching `TODO.md`), fix it proactively and report the change. Do not ask for permission first when the correction is clear and non-destructive.

## Environment Check (New Session)

Run at session start to confirm devcontainer type:
```shell
printenv | grep -i "container\|remote\|codespace" | cat
```
Key signal: `DEVCONTAINER_CONFIG_PATH=/.jbdevcontainer/...` = JetBrains devcontainer. Ports/paths are container-relative; IDE handles port-forwarding automatically.

## Session State (`tasks/DOR-nnn/STATUS.md`)

At session start: (1) identify ticket from branch name, (2) read `tasks/DOR-nnn/STATUS.md` in full, (3) cross-check against `TODO.md` — `TODO.md` is authoritative.

During session: update `STATUS.md` when a subtask completes, plan changes, or key decision made.

End of session: update Last Updated, Recent Activity, Next Steps. Commit `STATUS.md` in final commit.

| Section         | Contents                                                               |
|-----------------|------------------------------------------------------------------------|
| Last Updated    | ISO date + one-line session summary                                    |
| Current Branch  | Active git branch name; brief note on other local branches if relevant |
| Open Tasks      | Copy of unchecked subtasks from `TODO.md`; key files for each task     |
| Open Plans      | Table of files in `tasks/DOR-nnn/plans/` with purpose and status       |
| Recent Activity | Bullet list of meaningful changes made in the most recent session      |
| Key Context     | Decisions, design notes, or gotchas the next agent needs to understand |
| Next Steps      | Ordered list of what to do next, specific enough to act on immediately |

## Task Tracking (`tasks/DOR-nnn/TODO.md` / `tasks/DOR-nnn/DONE.md`)

Files live at `guidelines/projects/dor-react-app/tasks/DOR-nnn/` (TODO.md, DONE.md, STATUS.md, plans/).

New ticket: `mkdir -p guidelines/projects/dor-react-app/tasks/DOR-nnn/plans` + create TODO.md + STATUS.md + row in `tasks/README.md`.

- **Record plan in `TODO.md` first, then ask developer to review. Wait for explicit approval before implementing.**
- Check off (`- [x]`) as completed. Every task ends with `- [ ] Verify with the developer that the task is complete`.
- All done → create `tasks/DOR-nnn/DONE.md` with timestamp + summary + checklist.
- Complete ticket: `git mv guidelines/projects/dor-react-app/tasks/DOR-nnn guidelines/projects/dor-react-app/archive/DOR-nnn`
- Reorder subtasks with Python only — never string-replace.

## Test-Driven Development (TDD)

Write tests before implementation. Order: Test → Implementation → Documentation. Frameworks: Vitest + React Testing Library (JS), pytest/unittest (Python).

## React / Node.js / Vite Conventions

- **Package manager**: `npm` only. Never `yarn` or `pnpm`.
- **Lint before commit**: `npm run lint | cat`
- **Development server**: `npm run dev` (typically `http://localhost:5173` — container-relative in devcontainer).
- **Production build**: `npm run build` → output in `dist/`.
- **Project structure**:
  - `src/` — all source code
  - `src/apps/` — application modules (e.g. `OsDorDcApp`, `RsDorDcApp`)
  - `src/apps/*/components/` — React components specific to an app module
  - `src/apps/*/services/` — API clients and data services
  - `src/apps/*/utils/` — utility functions and constants
  - `src/assets/` — static assets
  - `public/` — public static files served at root
- **Key dependencies** (don't swap without reason):
  - `antd` — Ant Design UI component library
  - `@appbaseio/reactivesearch` — Elasticsearch/OpenSearch search UI components
  - `dompurify` — HTML sanitization (use when rendering user-generated or external HTML)
  - `react-router-dom` — client-side routing
  - `vite` — build tool and dev server


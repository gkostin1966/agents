# AGENT_QUIZ_ANSWERS — Base

> Fill this only after quiz answers are complete and comparison is explicitly authorized.

## Q1
Branch is `gkostin`. No ticket key is embedded in the branch name — this branch is
the developer's personal working branch, not a ticket-scoped feature branch.

## Q2
Agent operating rules and startup behavior are defined by:

- `.agents/AGENTS.md` — canonical rules for all sessions
- `.agents/AGENT_PROMPT.md` — startup workflow (base version)
- `.agents/AGENT_PROMPT_MERGED.md` — auto-generated merged prompt (do not edit directly)

## Q3
No active or completed task tracking files are currently present under `.agents/`.

Expected format: "No active/completed task tracking files are currently present under `.agents/`."

## Q4
No application test command selected for this task; no code changes were made to
application logic. Setup and configuration work only.

## Q5
Most relevant file-access and commit constraints from `AGENTS.md`:

- Stay within the project directory; outside files: read-only and only when explicitly requested.
- Never read `AGENT_QUIZ_ANSWERS.md` until all quiz answers are written **and** developer explicitly grants permission.
- Treat `.agents/` as shared framework metadata; do not include `.agents/` updates in normal app-code commits.
- Agents do not commit `.agents/` files in mounted repositories unless the developer explicitly directs otherwise.
- Never use heredocs (`<<`) or multiline `-c` flags in shell commands; write to file and run the file instead.
- Commit rules: no amend, no force-push, never push to `main`. Single-line commits use `-m`; multiline use `-F .agents/tmp/commit-msg.txt`.

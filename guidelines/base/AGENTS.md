# Agent Rules — Base Guidelines

> **These are the shared base rules for all projects in this multi-project workspace.**
> They are automatically merged with each project's specific guidelines.
> Project-specific guidelines override any section here with the same `## Heading`.
>
> **Read this file at the start of every new agent session, before taking any action.**
> These rules apply to all AI coding agents (GitHub Copilot, Claude, Cursor, etc.) working
> in any repository under this workspace.

## File Access

- **Stay within the project directory**: Only read, write, or search files that are under
  the project root directory. Do not access files outside the project directory unless the
  developer **explicitly** requests it.
  - When a developer does request access to an outside file, read **only that specific file**
    — do not browse, list, or search the surrounding directory or any parent directories.
  - Never speculatively explore paths outside the project root.

- **Never read `AGENT_QUIZ_ANSWERS.md` before completing the quiz.** When taking the
  `AGENT_QUIZ.md` onboarding quiz, do not open or read `AGENT_QUIZ_ANSWERS.md` until
  you have written out answers to **all** questions **and** the developer has explicitly
  told you to compare. Reading the answer file in advance defeats the purpose of the quiz.

## Command-Line Tool Usage

- **Disable interactive paging**: When running commands that may invoke a pager (e.g.,
  `git`, `less`, `man`, `kubectl`, etc.), always suppress paging so the command returns
  immediately and its output is captured. For example:
  - Use `git --no-pager <command>` for git commands.
  - Append `| cat` to commands that might page output (e.g., `kubectl ... | cat`).
  - Set `GIT_PAGER=cat` or `PAGER=cat` in the environment when needed.
  - Never rely on interactive input; all commands must run non-interactively and return
    their full output.

- **Never pass multi-line code via `-c` flags.** zsh mangles multi-line quoted strings
  passed to `python3 -c "..."`, `bash -c "..."`, or any other `exec -c "..."` invocation —
  unclosed inner quotes trigger `dquote>` heredoc mode, corrupting the terminal session.
  This is the same class of failure as `git commit -m "..."` (see § Git Commits).

  **The universal fix — write to a file, run the file:**

  1. Use `insert_edit_into_file` (or `create_file`) to write the code to a file.
     - Reusable scripts → `dotpy/myscript.py` (follow the `dotpy/` conventions).
     - Truly one-off scripts → `/tmp/run.py` (no need to commit).
  2. Run it:
     ```shell
     python3 dotpy/myscript.py | cat
     # or
     python3 /tmp/run.py | cat
     ```

  Additional zsh quoting rules:
  - **Single-line `-c` commands are safe** only when they contain no inner quotes and no
    `$` expansions, e.g. `python3 -c "print(42)" | cat`.
  - **Never generate file content** (RTF, XML, YAML, etc.) by echoing or printing strings
    through the shell. Write a Python script that builds the content and writes it with
    `open(...).write(...)` — this sidesteps all shell quoting entirely.
  - **Dollar signs and backticks in double-quoted strings** are expanded by zsh; wrap them
    in single quotes or use a `$'...'` ANSI-C quote string only for truly simple one-liners.

- **Never use shell heredocs (`<< 'MARKER'`) to write multi-line content.**
  zsh heredocs are extremely fragile in a tool-driven terminal session:
  - If a previous command left the terminal in `heredoc>` prompt mode (e.g. an unclosed
    `<<` from a failed command), all subsequent commands are silently consumed as heredoc
    body instead of being executed — corrupting the session without any error message.
  - The `heredoc>` prompt gives no indication that commands are being swallowed.
  - Recovery requires sending the exact end-marker string, which itself may be mangled.

  **Never use this pattern:**
  ```shell
  # ❌ — heredoc in a tool-driven shell session
  cat > file.txt << 'EOF'
  content here
  EOF
  ```

  **Always use Python instead:**
  ```python
  # ✅ — write a Python file, run it
  # Step 1: use insert_edit_into_file / create_file to write dotpy/myscript.py
  # Step 2: python3 dotpy/myscript.py | cat
  ```

  If the terminal ever appears stuck (commands produce no output, or output looks like
  garbled repeated text), it is almost certainly in `heredoc>` mode. To escape:
  1. Identify the heredoc end-marker that was used (e.g. `EOF`, `PYEOF`).
  2. Run that marker as a standalone command to close the heredoc.
  3. Verify the shell is back to a normal prompt before continuing.

## Python Utility Scripts (`dotpy/`)

- **Use existing scripts** in `dotpy/` before writing ad-hoc Python one-liners. See
  [`dotpy/README.md`](dotpy/README.md) for the full list and usage instructions.
- **Save reusable scripts** to `dotpy/` rather than running them once and discarding them:
  - Add a `#!/usr/bin/env python3` shebang and a module-level docstring with a **Usage** section.
  - Accept a file path as the first positional argument and fall back to stdin.
  - Add an entry to `dotpy/README.md` following the existing format.

## Git Commits

- **Never amend existing commits.** Always create a new commit on top of the current HEAD
  using `git commit` (not `git commit --amend`). The developer will squash or amend commits
  manually as needed.
- **Do not force-push** or rewrite history in any way unless the developer explicitly
  instructs it.
- **Never push to `main`.** Only the developer may push to the `main` branch. The agent may
  commit locally but must never run `git push` (or any variant that targets `main`) unless
  the developer explicitly instructs it.

### Writing commit messages — use `dotpy/commit.py`, never `git commit -m`

**Never use `git commit -m "..."` for multi-line messages.** zsh mangles multi-line quoted
strings and triggers heredoc mode, corrupting the terminal.

**Always use this two-step pattern instead:**

1. Use `insert_edit_into_file` (or `create_file`) to write the desired commit message
   (subject + blank line + body) to `dotpy/commit_msg.txt`.
2. Run:
   ```shell
   python3 dotpy/commit.py | cat
   ```

`dotpy/commit.py` reads `dotpy/commit_msg.txt`, writes its contents to a temp file, and
calls `git commit -F`, bypassing all shell quoting entirely. `dotpy/commit_msg.txt` is
listed in `.gitignore` and is never committed.

Single-line subject-only commits are the **one exception** where `-m` is safe:
```shell
git commit -m "chore: single line message" | cat
```

## Pull Request Summaries

- **At developer sign-off** (when the final "Verify with the developer" subtask is checked
  off), proactively create the PR summary without waiting to be asked.
- **When the developer asks for a PR summary**, write it to `pr-summary.md` in the project
  root and open the file so they can select-all and copy from the editor. `pr-summary.md`
  is listed in `.gitignore` and will never be accidentally committed.
- Use standard GitHub-flavoured Markdown: `##` / `###` headings, `**bold**`, inline
  backticks, and bullet lists. Do not use HTML tags.
- Structure the summary as:
  1. **`## <Title>`** — one-line description matching the branch purpose.
  2. **`### Summary`** — 2–4 sentences on what the PR does and why.
  3. **`### Changes`** — one bold entry per changed file or directory with bullet
     sub-points explaining what changed.
  4. **`### Notes`** *(optional)* — follow-up items, known limitations, or things the
     reviewer should verify manually.
- Delete `pr-summary.md` after the PR is created; do not commit it.

## Email Drafts for Third Parties

- **When the developer asks you to compose an email** to be sent to an external party
  (e.g., ITS, HITS, a vendor, or any recipient outside the development team), write it
  as a **Rich Text Format (`.rtf`) file** so the developer can open it in any mail client
  or word processor, fill in the recipient fields, and send without reformatting.
- Save the file under **`emails/<short-descriptive-name>.rtf`**, e.g.
  `emails/its-oidc-request.rtf`, `emails/hits-elements-request.rtf`.
- The `emails/` directory is **tracked in git**. Files are committed and remain in the
  repository until the developer explicitly removes them. Do not add individual draft
  filenames to `.gitignore`.
- **RTF structure for an email draft:**
  1. `\b Subject:\b0` line
  2. `\b To:\b0` and `\b CC:\b0` lines with `[placeholder]` values the developer fills in
  3. Blank line, then the greeting and body
  4. Use `\b … \b0` for bold headings, `\f1 … \f0` (monospace/Courier) for technical values
     (client IDs, URLs, commands), and `- ` prefixed lines for bullet points
  5. Use `\par` for paragraph breaks — do **not** use `\line`, `\emdash`, `\endash`,
     `\rquote`, or other Word-specific control words; they prevent macOS TextEdit from
     opening the file
  6. A closing with `[Your name]` placeholder
- **Open the file** after creating it so the developer can review it immediately.

## Markdown Formatting

- **Format tables correctly**: Every column in a Markdown table must be padded so that all
  cells in that column (header, separator, and every data row) are the same width. The
  separator row must use dashes (`-`) at least as wide as the widest cell in each column.
  Mismatched widths cause IDE warnings ("Table is not correctly formatted").
  - Determine the widest cell in each column (considering the rendered source text, not the
    display text of links).
  - Pad every shorter cell with trailing spaces to match that width.
  - Use the same number of dashes in the separator row as the column width.
  - **The data rows — not just the header — define the required column width.** The header
    and separator must be padded/extended to match the widest data cell, not the other way
    around.
  - To auto-format a table (strip whitespace, recalculate all widths, pad in place), run:
    `python3 dotpy/format_table.py <file.md>` — rewrites the file with every table correctly
    padded. **Use this first.**
  - To compute the exact separator without editing, run:
    `python3 dotpy/calc_widths.py <file.md>` — it prints the maximum between-pipe width per
    column and the ready-to-paste separator row for every table in the file.
  - To validate alignment after editing, run:
    `python3 dotpy/check_tables.py <file.md>` — exits `0` if all tables are consistent, `1`
    with error details if not.
  - If a table requires very long lines (e.g., > 120 characters per row), prefer using a
    shorter link display text or a bullet-list format instead of a wide table.


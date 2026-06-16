# dotpy — Python Utility Scripts

This directory contains small Python helper scripts used by developers and AI
coding agents working in this repository. All scripts require only the Python
standard library (no `pip install` needed) and are invoked directly with
`python3`.

Scripts live at `.agents/dotpy/` — invoke from the project root:

```shell
python3 .agents/dotpy/<script>.py | cat
```

---

## Scripts

### `commit.py` — Safe multi-line git commit helper

Reads a commit message from `.agents/dotpy/commit_msg.txt` and calls `git commit -F`,
bypassing all shell quoting. This avoids the zsh heredoc-mode bug that occurs
when using `git commit -m "..."` with multi-line strings.

`.agents/dotpy/commit_msg.txt` is never committed.

**Usage (per `AGENTS.md` § Git Commit Messages)**

1. Use `insert_edit_into_file` (or `create_file`) to write the desired commit
   message to `.agents/dotpy/commit_msg.txt` (subject line + blank line + body).
2. Run:
   ```shell
   python3 .agents/dotpy/commit.py | cat
   ```

**When to use**

- Every time a multi-line commit message is needed.
- Single-line subject-only commits may still use `git commit -m "subject" | cat`.

---

### `write_commit_msg.py` — Write commit message from stdin

Reads from stdin and writes to `.agents/dotpy/commit_msg.txt`.

**Usage**

```shell
echo "subject line" | python3 .agents/dotpy/write_commit_msg.py
python3 .agents/dotpy/commit.py | cat
```

---

### `calc_widths.py` — Markdown table column-width calculator

Reads a Markdown file (or stdin) and, for every table found, prints the maximum
between-pipe cell width for each column and a correctly sized separator row.

**Usage**

```shell
python3 .agents/dotpy/calc_widths.py <file.md>
python3 .agents/dotpy/calc_widths.py          # reads from stdin
```

**When to use**

- When authoring a new Markdown table: draft the rows first, run this script,
  then paste in the printed separator and pad every cell to the reported widths.

---

### `check_tables.py` — Markdown table column-width validator

Reads a Markdown file (or stdin) and checks that every row in every table —
header, separator, and data rows — has the same between-pipe column widths.

**Usage**

```shell
python3 .agents/dotpy/check_tables.py <file.md>
python3 .agents/dotpy/check_tables.py          # reads from stdin
```

**Exit codes:** `0` = all tables pass, `1` = one or more errors found.

**When to use**

- After editing any Markdown table, run to confirm nothing is misaligned.

---

### `format_table.py` — Auto-format Markdown tables in place

Reads a Markdown file (or stdin), strips unnecessary whitespace from every
table cell, recalculates column widths, and rewrites the file with all tables
correctly padded.

**Usage**

```shell
python3 .agents/dotpy/format_table.py <file.md>   # formats in place
python3 .agents/dotpy/format_table.py             # reads from stdin, writes to stdout
```

**When to use**

- After writing or editing a Markdown table without worrying about alignment.
- Follow up with `check_tables.py` to confirm the result is valid.

---

### `_gen_rtf.py` — RTF email draft generator (internal helper)

Generates `.agents/emails/its-oidc-request.rtf` — a macOS TextEdit-compatible RTF
draft for the ITS OIDC client request. Used as the canonical example of generating
structured file content from Python without shell quoting.

**Usage**

```shell
python3 .agents/dotpy/_gen_rtf.py
```

---

### `write_pr_summary.py` — DOR-159 PR summary writer (archived one-off)

Writes the DOR-159 Phase 2 PR summary to `pr-summary.md` in the project root.
Preserved for historical reference.

---

## Conventions for adding new scripts

1. Place the `.py` file in this `.agents/dotpy/` directory.
2. Add a `#!/usr/bin/env python3` shebang and a module-level docstring with a **Usage** section.
3. Accept an input path as the first positional argument and/or fall back to stdin.
4. Add an entry to this README under **Scripts**.
5. Reference the script from `AGENTS.md` if agents should know about it.


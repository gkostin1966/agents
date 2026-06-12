# Agent Onboarding Quiz — Answer Key

> ⚠️ **DO NOT READ THIS FILE** until you have answered all questions in
> `AGENT_QUIZ.md` and the developer has told you to compare your answers.
> Reading this file before completing the quiz defeats its purpose.

---

> Every answer below can be verified by reading the cited source file.
> If an answer here contradicts what you find in the source, **the source file wins**.

---

## Section 1 — Ground Rules

**A1.** Record the plan in `.agents/tasks/ARC-nnn/TODO.md` before executing any step.
*(Source: `AGENTS.md` § Task Tracking)*

---

**A2.** Use Python only (`python3 <script>`). Never use string-replace (sed, awk, or
text-editor find-and-replace) to reorder subtasks.
*(Source: `AGENTS.md` § Task Tracking)*

---

**A3.** Never amend. Create a new commit with the fix instead.
*(Source: `AGENTS.md` § Git Commits)*

---

**A4.** `python3 -c "..."` with multiline code in zsh triggers `dquote>` heredoc mode,
silently corrupting the terminal session. Fix: write the snippet to a file (e.g.
`.agents/tmp/run.py`) and run `python3 .agents/tmp/run.py | cat`.
*(Source: `AGENTS.md` § Command-Line Tool Usage)*

---

**A5.** Data rows define the required column width. Pad the header and separator to
match the widest data cell.
*(Source: `AGENTS.md` § Markdown Tables)*

---

## Section 2 — Project Stack and Build

**A6.** Ruby 3.4.9.
*(Source: `.ruby-version`; `Dockerfile ARG RUBY_VERSION=3.4.9`)*

---

**A7.** Rails ~> 8.1.3.
*(Source: `Gemfile` — `gem "rails", "~> 8.1.3"`)*

---

**A8.**

| Service   | Localhost port |
|-----------|---------------|
| app       | 3000          |
| solr      | 8983          |
| zookeeper | 2181          |

*(Source: `compose.yml` `ports:` entries)*

---

**A9.** Collection name: `blacklight-collection`.
Creation command (run after stack is up):
```shell
/bin/bash ./solr/dev-init.sh
```
Which executes: `docker compose exec solr solr create -c blacklight-collection -d /opt/solr/conf`
*(Source: `compose.yml` `SOLR_URL`; `solr/dev-init.sh`)*

---

**A10.** SQLite 3 (`gem "sqlite3", ">= 2.1"`). The `bin/docker-entrypoint` script
runs `./bin/rails db:prepare` automatically when the Rails server starts.
*(Source: `Gemfile`; `bin/docker-entrypoint`)*

---

**A11.**
```shell
docker compose exec app bundle exec rails test | cat
```
*(Source: `AGENTS.md` § Ruby on Rails Conventions)*

---

**A12.**
```shell
docker compose exec app bundle exec rubocop -a | cat   # auto-fix
docker compose exec app bundle exec rubocop | cat      # check
```
*(Source: `AGENTS.md` § Ruby on Rails Conventions)*

---

## Section 3 — Domain Concepts

**A13.** `boxrunner` is an archival finding-aid discovery application. Primary discovery/search
stack: `arclight`, built on Blacklight.
*(Source: `Gemfile`; `AGENT_PROMPT.md` session context)*

---

**A14.** Solr 9.7, running in SolrCloud mode. SolrCloud requires a ZooKeeper service.
*(Source: `compose.yml` — `image: solr:9.7`; `ZK_HOST=zookeeper:2181`)*

---

**A15.** The app connects to `http://solr:8983/solr/blacklight-collection`. This URL
is passed via the `SOLR_URL` environment variable set in `compose.yml`.
*(Source: `compose.yml` — `SOLR_URL=http://solr:8983/solr/blacklight-collection`)*

---

## Section 4 — Active Work and Task Management

**A16.** *(Agent must look this up live from `.agents/tasks/README.md`.
No tasks exist at project bootstrap — answer: "No active tickets.")*

---

**A17.** Create `.agents/tasks/ARC-nnn/DONE.md` with timestamp, summary, and completed checklist.
Then, after the PR merges:
```shell
git mv .agents/tasks/ARC-nnn .agents/archive/ARC-nnn
```
*(Source: `AGENTS.md` § Task Tracking)*

---

**A18.** Full startup from scratch:
```shell
docker compose up
/bin/bash ./solr/dev-init.sh
```
*(Source: `AGENTS.md` § Ruby on Rails Conventions; `solr/dev-init.sh`)*


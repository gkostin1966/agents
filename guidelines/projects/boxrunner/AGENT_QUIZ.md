# Agent Onboarding Quiz — boxrunner

> 🚫 **DO NOT read `AGENT_QUIZ_ANSWERS.md`** until you have written out answers to all
> questions below and the developer has told you to compare. Reading the answer file
> first defeats the purpose of the quiz.
>
> **Instructions for the quiz-taker (agent):**
> Answer every question by looking it up in the actual project files — do not rely on
> memory or training data. Each question includes a hint pointing to the authoritative
> source. Write your answers in your response, then stop and prompt the developer
> (see the instruction after Q18).
>
> **Instructions for the quiz-giver (developer):**
> Run this quiz at the start of a new agent session to confirm the agent has read and
> understood the project state before it begins work. When the agent prompts you after
> Q18, open `AGENT_QUIZ_ANSWERS.md` and grade the answers yourself, or ask the agent
> to read that file and self-grade at that point.

---

## Section 1 — Ground Rules (AGENTS.md)

**Q1.** You are about to start a multi-step task. What must you do *before* executing
the first step, and how should you treat files under `.agents/` when they are relevant
to the current task and their commits belong to the separate agent-framework project
outside this repository? Include the rule about whether agents in this project ever
commit `.agents/` files, and what to do when task metadata drift is clear and non-destructive.

*(Hint: `AGENTS.md` § File Access; `AGENTS.md` § Task Tracking; `AGENTS.md` § Git Commits)*

---

**Q2.** You need to reorder two subtasks in `.agents/tasks/ARC-nnn/TODO.md`. What tool must you use, and what
tool must you **never** use for this operation?

*(Hint: `AGENTS.md` § Task Tracking)*

---

**Q3.** The developer asks you to amend the most recent commit to include a small fix.
What should you do instead?

*(Hint: `AGENTS.md` § Git Commits — base rules)*

---

**Q4.** You need to run a short multi-line Python snippet. Your first instinct is to
write `python3 -c "..."`. What is wrong with that approach in this environment, and
what is the universal fix?

*(Hint: `AGENTS.md` § Command-Line Tool Usage)*

---

**Q5.** After editing a Markdown file that contains tables, what rule governs column
widths in the table?

*(Hint: `AGENTS.md` § Markdown Tables)*

---

## Section 2 — Project Stack and Build

**Q6.** What Ruby version does this project use?

*(Hint: `.ruby-version` and `Dockerfile`)*

---

**Q7.** What Rails version does this project require?

*(Hint: `Gemfile`)*

---

**Q8.** List every Docker Compose service defined in `compose.yml`, and state what
localhost port is exposed for each (write "none" if no port is published).

*(Hint: `compose.yml` — `services:` and `ports:` entries)*

---

**Q9.** What is the name of the Solr collection used by this application, and what
command creates it after the stack first starts?

*(Hint: `compose.yml` `SOLR_URL`; `solr/dev-init.sh`)*

---

**Q10.** What database does this application use, and how is it initialised when the
Rails server starts inside the container?

*(Hint: `Gemfile`; `bin/docker-entrypoint`)*

---

**Q11.** What command runs the full Rails test suite inside the container?

*(Hint: `AGENTS.md` § Ruby on Rails Conventions)*

---

**Q12.** Before committing Ruby source files, what two RuboCop commands should you run
(auto-fix then check), written as full `docker compose exec` invocations?

*(Hint: `AGENTS.md` § Ruby on Rails Conventions)*

---

## Section 3 — Domain Concepts

**Q13.** What is this application? Name the primary discovery/search gem in this app,
and the upstream discovery framework it is built on.

*(Hint: `Gemfile`; ArcLight/Blacklight stack context in project docs and prompts)*

---

**Q14.** What Solr image version and mode (standalone vs. SolrCloud) does this project
run, and what additional service does SolrCloud require?

*(Hint: `compose.yml`)*

---

**Q15.** Where does the application expect to find the Solr instance at runtime, and
how is that URL passed to Rails?

*(Hint: `compose.yml` — `SOLR_URL` environment variable)*

---

## Section 4 — Active Work and Task Management

**Q16.** At session start, how do you determine which ticket to focus on from the
current branch name using the `ARC-\d+` key pattern, and what must you do if the
branch name does not contain an `ARC-\d+` key (for example `main`)? Also list every currently active ticket with
its key and a one-sentence summary. If there are no active tickets, answer exactly:
`No active tickets.`

*(Hint: `AGENTS.md` § Session State; `.agents/tasks/README.md`; each active `.agents/tasks/ARC-nnn/STATUS.md`)*

---

**Q17.** A task in `.agents/tasks/ARC-nnn/TODO.md` has all subtasks checked off including the
developer-verification subtask. What are the required closeout steps, and after the
PR merges where does the task directory move to? If PR review comments later require
more work, how do you reopen and track that follow-up work?

*(Hint: `AGENTS.md` § Task Tracking)*

---

**Q18.** How do you fully start the local development environment from scratch?
List every command in order, including the Solr initialisation step. Also, if
verification is blocked during task work, what exact details must be reported in
`STATUS.md`?

*(Hint: `AGENTS.md` § Ruby on Rails Conventions; `solr/dev-init.sh`; `AGENTS.md` § Session State)*

---

## When You Have Answered All 18 Questions

Stop here. Do **not** open `AGENT_QUIZ_ANSWERS.md`.

Tell the developer:

> "I have answered all quiz questions. Please open `AGENT_QUIZ_ANSWERS.md` to grade
> my answers, or let me know when I may read it to self-grade."

Wait for the developer's instruction before proceeding.


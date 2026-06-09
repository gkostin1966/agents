# Agent Onboarding Quiz — boxwalker

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
the first step?

*(Hint: `AGENTS.md` § Task Tracking)*

---

**Q2.** You need to reorder two subtasks in `tasks/BW-nnn/TODO.md`. What tool must you use, and what
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

**Q8.** What three Docker Compose services make up the local development stack, and
what localhost port is exposed for each?

*(Hint: `compose.yml`)*

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

**Q13.** What is this application? Name the two primary Ruby gems that provide its
discovery/search functionality.

*(Hint: `Gemfile`; `README.md`)*

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

**Q16.** Look at `tasks/README.md`. List every currently active ticket with its key and
a one-sentence summary of what it is working on.

*(Hint: `tasks/README.md` and each active `tasks/BW-nnn/STATUS.md` in `AGENTS_ROOT`)*

---

**Q17.** A task in `tasks/BW-nnn/TODO.md` has all subtasks checked off including the
developer-verification subtask. What are the steps required to archive it, and where
does the task directory move to?

*(Hint: `AGENTS.md` § Task Tracking)*

---

**Q18.** How do you fully start the local development environment from scratch?
List every command in order, including the Solr initialisation step.

*(Hint: `README.md`; `solr/dev-init.sh`)*

---

## When You Have Answered All 18 Questions

Stop here. Do **not** open `AGENT_QUIZ_ANSWERS.md`.

Tell the developer:

> "I have answered all 18 quiz questions. Please open `AGENT_QUIZ_ANSWERS.md` to grade
> my answers, or let me know when I may read it to self-grade."

Wait for the developer's instruction before proceeding.


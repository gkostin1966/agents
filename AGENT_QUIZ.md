# AGENT_QUIZ — agents (meta-framework)

> Answer every question below by looking up the answer in the actual project files.
> Do **not** read `AGENT_QUIZ_ANSWERS.md` until you have answered all questions and the
> developer has told you to compare.
>
> This quiz is scoped to the `agents` framework itself.
> Treat mounted projects as abstract configured entries (not stack-specific trivia targets).
>
> Write your answers inline under each question before moving on.

---

## Section 1 — Framework Scope and Layout

**Q1.** What are the two primary roles of this repository, as described in root `AGENTS.md`?

**Q2.** What is the Python package path for the framework code, and what is the package name?

**Q3.** List every module in `src/agents_framework/` and give a one-line purpose for each.

**Q4.** What file defines the mounted-project catalog, and which fields are required per project entry in the current schema?

**Q5.** In this framework, what does `mounted-projects/` represent, and what are the read/write restrictions for that directory?

---

## Section 2 — Config and Registration Rules

**Q6.** When a project is mounted for the first time, what must be updated first so the framework recognizes it?

**Q7.** In `config/projects.json`, what is the purpose of `relative_path`, and where in the code is it used to resolve mount paths?

**Q8.** If a project uses a stack value not currently listed in `STACK_MARKERS`, what code file and symbol must be updated?

**Q9.** What is the difference between `name` and `relative_path` in practical CLI behavior?

---

## Section 3 — Merge Architecture

**Q10.** What are the source and generated files for guidelines merging?

**Q11.** What are the source and generated files for prompt merging?

**Q12.** What happens when a `## Heading` exists in both base and project files during merge?

**Q13.** Which shared module implements section splitting/merging, and what are its three public functions?

**Q14.** Which two modules import that shared merge helper?

---

## Section 4 — CLI Behavior

**Q15.** What is the console entry point (`module:function`) for `agentsfw`?

**Q16.** What does `agentsfw scan` report at a high level?

**Q17.** What does `agentsfw validate` check, and which files are required vs recommended?

**Q18.** What safety rule applies to `guidelines generate all --output ...` and `prompt generate all --output ...`?

**Q19.** What command should be used to run the full test suite without installing the package?

---

## Section 5 — Task Tracking and Workflow

**Q20.** Where does task tracking for framework work live, and what is the required final subtask in every task?

**Q21.** Before executing any multi-step plan, what must be done in `AGENT_TODO.md`?

**Q22.** When a framework task is fully complete, how is it archived from `AGENT_TODO.md` to `AGENT_DONE.md`?

**Q23.** What is the rule about reading `AGENT_QUIZ_ANSWERS.md`?

---

## Section 6 — Operational Checks

**Q24.** What startup git-orientation commands must be run at the beginning of a new session?

**Q25.** If branch or working state is unexpected during startup checks, what should the agent do next?

**Q26.** You update `guidelines/base/AGENTS.md`. What is the next framework step to validate merged outputs across all configured projects?

**Q27.** What does `agentsfw prompt generate all` do, and where are outputs written?

**Q28.** Looking at current git history, what is the most recent commit message?



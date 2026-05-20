# AGENT_QUIZ — dspace-containerization

> Answer every question below by looking up the answer in the actual project files.
> Do **not** read `AGENT_QUIZ_ANSWERS.md` until you have answered all questions and the
> developer has told you to compare.
>
> Write your answers inline under each question before moving on.

---

## Section 1 — Project Structure and Purpose

**Q1.** What is the primary purpose of the `dspace-containerization` repository?
What DSpace version does it target, and what services does it run?

**Q2.** How are Make targets organised? What command shows all available targets?
List the key targets mentioned in `AGENTS.md`.

**Q3.** The project has multiple Dockerfiles for different services. List them and
state which service each one builds.

**Q4.** Where do environment variables go before running `make up`? What file must
never be committed?

**Q5.** Where do CI workflows live and what must pass before work is considered complete?

---

## Section 2 — Configuration Pattern

**Q6.** The project uses an env-var based configuration approach instead of `local.cfg`.
How are DSpace property names encoded as Docker Compose environment variable keys?
Give one example of a property with a dot and one with a hyphen.

**Q7.** What is the relationship between the Docker Compose `environment:` config and
the Kubernetes ConfigMap (`backend-cm.jsonnet`) config? Why do they use the same key encoding?

**Q8.** What is the smoke test script and what does it verify?
What tool does it use to make assertions format-agnostic?

---

## Section 3 — Task Tracking

**Q9.** Where does task tracking for this project live, and what are the two tracking file names
(note: they differ from the `AGENT_TODO.md`/`AGENT_DONE.md` pattern used by other projects)?

**Q10.** What is the open task listed in `TODO.md`, and why is it blocked?

---

## Section 4 — Agent Framework Integration

**Q11.** Where do agent guideline files for this project live in the `agents` repository?

**Q12.** What command generates the merged `AGENTS.md` for this project?

**Q13.** The `AGENT_PROMPT.md` for this project asks the agent to request a path at session
start. What is that path called, and why is it not hardcoded?


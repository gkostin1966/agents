# AGENT_QUIZ — agents (meta-framework)

> Answer every question below by looking up the answer in the actual project files.
> Do **not** read `AGENT_QUIZ_ANSWERS.md` until you have answered all questions and the
> developer has told you to compare.
>
> Write your answers inline under each question before moving on.

---

## Section 1 — Project Structure

**Q1.** What is the absolute path to the Python source package for the framework, and
what is the name of the Python package?

**Q2.** List every module (`.py` file) inside `src/agents_framework/` and give one
sentence describing what each one does.

**Q3.** What file controls the list of mounted projects, and what are the six project
names registered in it?

**Q4.** The `mounted-projects/` directory is gitignored. How are the actual source
repositories made available under it?

**Q5.** Where does task tracking for work on the `agents` project itself live? How is
this different from where task tracking for mounted projects lives?

---

## Section 2 — Guidelines Architecture

**Q6.** What is the path to the shared base guidelines file? What sections does it
currently define?

**Q7.** What is the merge rule when a section heading appears in both
`guidelines/base/AGENTS.md` and `guidelines/projects/<name>/AGENTS.md`?

**Q8.** Which two projects override the `## Email Drafts for Third Parties` section, and
what is the key difference from the base?

**Q9.** Which projects use a flat `AGENT_TODO.md` / `AGENT_DONE.md` pattern at the
project level (not per-ticket), and which use a `tasks/<ticket-id>/` directory structure?

**Q10.** The `AGENTS_MERGED.md` files are gitignored. What command generates one for
`dor-react-app`?

---

## Section 3 — Framework Code

**Q11.** What is the class name and file that loads the project catalog from
`config/projects.json`? What two dataclasses does it return?

**Q12.** What is `STACK_MARKERS` in `framework.py`? Give the markers for the `rails-arclight`
stack as evidence you have read the file.

**Q13.** What argument must be passed to `agentsfw run` to target only `dor-depot` and
`umich-arclight`?

**Q14.** A call to `merge_guidelines(base_path, proj_path)` where the project file has a
`## Git Commits` section: what happens to the base `## Git Commits` section in the output?

**Q15.** What function in `guidelines.py` writes the merged file to disk, what is the
default output path, and is that file committed to git?

---

## Section 4 — Testing

**Q16.** How do you run the full test suite without installing the package? What is the
exact command?

**Q17.** How many tests exist as of your reading? List the test class names and the name
of each test method.

**Q18.** `test_real_base_and_project_files_exist_and_merge` verifies two specific
`## Heading` values are present in the merged output. What are they?

---

## Section 5 — Guidelines Content

**Q19.** The base `## Command-Line Tool Usage` section includes a warning about shell
heredocs that is **not** present in most of the original per-project `AGENTS.md` files.
Which project introduced that rule, and why should it be in the base?

**Q20.** What is the exact `## Heading` of the section in
`guidelines/projects/deepblue-documents-kube/AGENTS.md` that explains ConfigMap key
encoding, and what are the two encoding tokens and what each represents?

**Q21.** The `dor-depot` project uses Spring Modulith. What constraint does this impose
on cross-module calls, and what is the name of the Java package that contains the web UI?

**Q22.** Read `guidelines/projects/findingaids-argocd/AGENTS.md`. How many Kubernetes
clusters does that project use, and what are their kubectl context names?

**Q23.** What is the Jira ticket prefix used in `umich-arclight` task tracking, and what
is the directory path where a new ARC-050 ticket's files should be created?

---

## Section 6 — Operational Knowledge

**Q24.** You want to add a seventh mounted project called `new-project` with stack
`ruby-rails`. Using the **current** `config/projects.json` schema, list every file or
directory you must create or modify inside the `agents` repository to fully register it.

**Q25.** An agent working on `deepblue-documents-kube` tries to run `tk apply
environments/deepblue-documents/production` without asking the developer first. According
to the project guidelines, is this allowed? Where exactly is the rule that says so?

**Q26.** The `AGENT_QUIZ_ANSWERS.md` quiz-protection rule appears in the base guidelines.
Look at the base `## File Access` section: what is the exact condition under which an
agent may finally read `AGENT_QUIZ_ANSWERS.md`?

**Q27.** You modify `guidelines/base/AGENTS.md` to add a new rule. What is the next step
you must perform, and what is the new CLI command to regenerate all six projects at once
(added in the refactor — no shell loop required)?

**Q28.** Where does the `agentsfw` CLI entry point live (module + function name)?

**Q29.** The framework has a shared merge module. What is its name, what are its three
public functions, and which two modules import from it?

**Q30.** The `agentsfw validate` command checks each project for required and recommended
files. What are the required files and what are the recommended files?

**Q31.** What does `agentsfw prompt generate all` do, and where is the merged output
file written for each project?

**Q32.** Looking at the git log of this repository, what is the most recent commit message?



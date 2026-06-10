#!/usr/bin/env python3
"""Flatten all project AGENTS.md and AGENT_PROMPT.md files to self-contained.

Reads base + project files, merges them, strips framework-internal headers,
updates AGENTS_ROOT path references to use .agents/ first, and writes the
result back as the canonical project source file.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from agents_framework.merge import split_sections, merge_sections


PROJECTS = [
    "boxwalker",
    "deepblue-documents-kube",
    "dor-depot",
    "dor-react-app",
    "dspace-containerization",
    "findingaids-argocd",
    "umich-arclight",
]


def flatten(base_text: str, project_text: str, project_name: str) -> str:
    """Merge base + project, strip framework headers, return clean self-contained text."""
    base_header, project_header, merged_chunks = merge_sections(base_text, project_text)

    # Pull the title from the project header if present, else derive it.
    title_match = re.search(r"^# .+$", project_header, flags=re.MULTILINE)
    if title_match:
        title = title_match.group(0)
        # Remove "(project-specific additions)" qualifier - no longer relevant.
        title = re.sub(r"\s*\(project-specific additions\)", "", title).strip()
    else:
        title = f"# Agent Rules — {project_name}"

    return title + "\n\n" + "".join(merged_chunks)


def update_agents_root_refs(text: str, project_name: str) -> str:
    """Replace AGENTS_ROOT/guidelines/projects/<name>/... with .agents/... as primary."""
    # Already-updated boxwalker format: leave alone.
    if ".agents/" in text and "Primary:" in text:
        return text

    prefix = f"AGENTS_ROOT/guidelines/projects/{project_name}/"

    def replace_ref(m: re.Match) -> str:
        suffix = m.group(1)
        return f".agents/{suffix}"

    return re.sub(re.escape(prefix) + r"([^\s`\n]+)", replace_ref, text)


def flatten_agents_md(repo_root: Path, project_name: str) -> None:
    base_path = repo_root / "guidelines" / "base" / "AGENTS.md"
    proj_path = repo_root / "guidelines" / "projects" / project_name / "AGENTS.md"

    base_text = base_path.read_text(encoding="utf-8")
    proj_text = proj_path.read_text(encoding="utf-8")

    flat = flatten(base_text, proj_text, project_name)
    proj_path.write_text(flat, encoding="utf-8")
    print(f"flattened {project_name}/AGENTS.md")


def flatten_agent_prompt_md(repo_root: Path, project_name: str) -> None:
    base_path = repo_root / "guidelines" / "base" / "AGENT_PROMPT.md"
    proj_path = repo_root / "guidelines" / "projects" / project_name / "AGENT_PROMPT.md"

    base_text = base_path.read_text(encoding="utf-8")
    proj_text = proj_path.read_text(encoding="utf-8")

    flat = flatten(base_text, proj_text, project_name)
    flat = update_agents_root_refs(flat, project_name)

    # Also update the Required Developer Input section for non-boxwalker projects.
    # Replace the AGENTS_ROOT ask with .agents-first approach.
    old_required = (
        "Before reading framework-managed files, ask for the absolute path to the `agents`\n"
        "repository root and store it as `AGENTS_ROOT` for this session."
    )
    new_required = (
        "Use local `.agents` paths first.\n\n"
        "- Primary: read guidance from `.agents/` in the project root.\n"
        "- Fallback only if `.agents/` is missing or unreadable: ask for absolute `AGENTS_ROOT`."
    )
    flat = flat.replace(old_required, new_required)

    # Remove the old base startup workflow note referencing AGENTS_ROOT cross-repo.
    flat = flat.replace(
        "3. **Read framework-managed task state** under `AGENTS_ROOT/guidelines/projects/<project>/...`\n"
        "   as defined in the project-specific `## Task Files` block.\n",
        "3. **Read task state** from `.agents/` as defined in the `## Task Files` block below.\n",
    )

    proj_path.write_text(flat, encoding="utf-8")
    print(f"flattened {project_name}/AGENT_PROMPT.md")


def main() -> None:
    repo_root = ROOT
    for project_name in PROJECTS:
        flatten_agents_md(repo_root, project_name)
        flatten_agent_prompt_md(repo_root, project_name)
    print("\nAll project files flattened.")


if __name__ == "__main__":
    main()


from __future__ import annotations

"""Per-project agent-file completeness validation.

Checks that every registered project has the expected agent files under
``guidelines/projects/<name>/``.  Reports missing files and exits non-zero
when any project is incomplete.
"""

from dataclasses import dataclass, field
from pathlib import Path

from .config import FrameworkConfig


# Files that every project must have.
REQUIRED_FILES: tuple[str, ...] = (
    "AGENTS.md",
    "AGENT_PROMPT.md",
)

# Files that are strongly recommended but not required to pass.
RECOMMENDED_FILES: tuple[str, ...] = (
    "AGENT_QUIZ.md",
    "AGENT_QUIZ_ANSWERS.md",
)


@dataclass
class ProjectValidation:
    name: str
    missing_required: list[str] = field(default_factory=list)
    missing_recommended: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return len(self.missing_required) == 0


def validate_projects(
    repo_root: Path,
    config: FrameworkConfig,
    project_names: list[str] | None = None,
) -> list[ProjectValidation]:
    """Validate agent files for each project in *config*.

    If *project_names* is given, only those projects are checked.
    """
    results: list[ProjectValidation] = []

    for project in config.projects:
        if project_names is not None and project.name not in project_names:
            continue

        project_dir = repo_root / "guidelines" / "projects" / project.name
        result = ProjectValidation(name=project.name)

        for filename in REQUIRED_FILES:
            if not (project_dir / filename).exists():
                result.missing_required.append(filename)

        for filename in RECOMMENDED_FILES:
            if not (project_dir / filename).exists():
                result.missing_recommended.append(filename)

        results.append(result)

    return results


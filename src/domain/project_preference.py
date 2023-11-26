
from dataclasses import dataclass

from .project import Project


@dataclass(frozen=True)
class ProjectPreference:
    project: Project
    score: int


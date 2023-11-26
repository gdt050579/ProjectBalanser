
from dataclasses import dataclass

from domain.project_category import ProjectCategory


@dataclass(frozen=True)
class Project:
    id: int
    category: ProjectCategory


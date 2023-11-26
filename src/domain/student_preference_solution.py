
from dataclasses import dataclass

from .student import Student
from .project_category import ProjectCategory
from .project_preference import ProjectPreference


@dataclass(frozen=True)
class StudentPreferenceSolution:
    student: Student
    projects: dict[ProjectCategory, ProjectPreference]


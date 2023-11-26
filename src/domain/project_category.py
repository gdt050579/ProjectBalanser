
from enum import Enum


class ProjectCategory(Enum):
    A = "A"
    B = "B"
    C = "C"

    def __repr__(self) -> str:
        return f"project_category_{self.value}"


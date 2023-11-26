
import copy

from domain import StudentPreference
from fixer.fixer import Fixer
from fixer.fix_error import FixError


class ProjectsPreferenceFixer(Fixer[list[StudentPreference]]):
    def __init__(self, students_preferences: list[StudentPreference]):
        Fixer.__init__(self)

        self.__students_preferences = students_preferences

    def _fix(self) -> list[StudentPreference]:
        students_preferences = copy.deepcopy(self.__students_preferences)

        for student_preferences in students_preferences:
            pass


        return students_preferences


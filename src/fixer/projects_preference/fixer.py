
import copy

import config
from domain import StudentPreference, ProjectPreference, ProjectCategory, Project
from fixer.fixer import Fixer
from fixer.fix_error import FixError


class ProjectsPreferenceFixer(Fixer[list[StudentPreference]]):
    def __init__(self, students_preferences: list[StudentPreference]):
        Fixer.__init__(self)

        self.__students_preferences = students_preferences

    def __remove_invalid_projects(self, project_preferences: list[ProjectPreference], project_category: ProjectCategory) -> list[ProjectPreference]:
        max_id_project_category = config.MAXIM_ID_PROJECT_CATEGORY.get(project_category)

        new_project_preferences = list()
        for project_preference in project_preferences:
            if 1 <= project_preference.project.id <= max_id_project_category:
                new_project_preferences.append(project_preference)

        return new_project_preferences

    def _fix(self) -> list[StudentPreference]:
        students_preferences = copy.deepcopy(self.__students_preferences)

        for student_preferences in students_preferences:
            projects_preferences = student_preferences.projects

            for project_category in ProjectCategory:
                project_preferences = projects_preferences[project_category]
                project_preferences = self.__remove_invalid_projects(project_preferences, project_category)

                projects_preferences[project_category] = project_preferences

        return students_preferences


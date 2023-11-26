
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

    def __unique_project_category(self, project_preferences: list[ProjectPreference]) -> list[ProjectPreference]:
        already_added_project_id = set()
        for project_preference in project_preferences:
            already_added_project_id.add(project_preference.project.id)

        new_project_preferences = list()
        for project_preference in project_preferences:
            if project_preference.project.id in already_added_project_id:
                new_project_preferences.append(project_preference)

        return new_project_preferences

    def __reassign_score(self, project_preferences: list[ProjectPreference]) -> list[ProjectPreference]:
        project_preferences.sort(key=lambda project_preference: project_preference.score)

        new_project_preferences = list()
        score_start = 1
        for project_preference in project_preferences:
            new_project_preference = ProjectPreference(
                project=project_preference.project,
                score=score_start
            )
            score_start += 1

            new_project_preferences.append(new_project_preference)

        return new_project_preferences

    def __add_missing_projects(self, project_preferences: list[ProjectPreference], project_category: ProjectCategory) -> list[ProjectPreference]:
        max_id_project_category = config.MAXIM_ID_PROJECT_CATEGORY.get(project_category)

        already_added_project_id = set()
        for project_preference in project_preferences:
            already_added_project_id.add(project_preference.project.id)

        new_project_preferences = list()
        for project_preference in project_preferences:
            new_project_preferences.append(project_preference)

        # Get ceil of 10's for the biggest project category id
        score_start = 10 ** len(str(max(config.MAXIM_ID_PROJECT_CATEGORY.values())))

        for id in range(1, max_id_project_category+1):
            if id not in already_added_project_id:
                project = Project(
                    id=id,
                    category=project_category
                )
                project_preference = ProjectPreference(
                    project=project,
                    score=score_start
                )
                score_start += 1

                new_project_preferences.append(project_preference)

        return new_project_preferences

    def _fix(self) -> list[StudentPreference]:
        students_preferences = copy.deepcopy(self.__students_preferences)

        for student_preferences in students_preferences:
            projects_preferences = student_preferences.projects

            for project_category in ProjectCategory:
                project_preferences = projects_preferences[project_category]
                project_preferences = self.__remove_invalid_projects(project_preferences, project_category)
                project_preferences = self.__unique_project_category(project_preferences)
                project_preferences = self.__reassign_score(project_preferences)
                project_preferences = self.__add_missing_projects(project_preferences, project_category)

                projects_preferences[project_category] = project_preferences

        return students_preferences


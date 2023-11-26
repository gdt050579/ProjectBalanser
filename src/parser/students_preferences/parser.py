
import pathlib

import pandas

from domain import ProjectCategory, Project, ProjectPreference, Student, StudentPreference
from parser.parser import Parser
from parser.parse_error import ParseError


class StudentsPreferencesParser(Parser[list[StudentPreference]]):
    def __init__(self, file_path: pathlib.Path):
        Parser.__init__(self)

        self.__file_path = file_path

    def __parse_projects(self, project_preferences_raw: str, project_category: ProjectCategory) -> list[ProjectPreference]:
        project_preferences = list()

        for i, project_preference_id_raw in enumerate(project_preferences_raw.split(",")):
            if project_preference_id_raw:
                try:
                    project_preference_id = int(project_preference_id_raw.strip())
                except Exception as exception:
                    raise ParseError(exception)

                project = Project(
                    id=project_preference_id,
                    category=project_category
                )

                project_preference = ProjectPreference(
                    project=project,
                    score=i+1
                )

                project_preferences.append(project_preference)

        return project_preferences

    def _parse(self) -> list[StudentPreference]:
        students_preferences = list()

        students_df = pandas.read_csv(self.__file_path)
        students_df.fillna("", inplace=True)

        for _, student_row in students_df.iterrows():

            project_preferences = dict()

            for project_category in ProjectCategory:
                project_preferences[project_category] = self.__parse_projects(
                        student_row[f"Projects Preference {project_category.value}"], project_category
                )

            student = Student(
                id=student_row["ID"],
                name=student_row["Name"],
                email=student_row["Email Address"]
            )

            student_preference = StudentPreference(
                student=student,
                projects=project_preferences
            )

            students_preferences.append(student_preference)

        return students_preferences



import pathlib
import argparse

import config
from domain import ProjectCategory, StudentPreferenceSolution
from parser.students_preferences import StudentsPreferencesParser
from fixer.projects_preference import ProjectsPreferenceFixer
from solver.jury import JurySolver
from utils import logs, dryable


def get_arguments():
    parser = argparse.ArgumentParser(
        prog="Assigner",
        description="Assigning project to students by their preference on projects."
    )

    parser.add_argument("filepath", type=str, help="CSV File path of students preferences.")

    return parser.parse_args()


@dryable.Dryable
def write_file_solution(students_solutions: list[StudentPreferenceSolution]) -> None:
    with open(config.FILE_NAME_STUDENTS_SOLUTION, "wt") as file:
        for student_solution in students_solutions:
            student = student_solution.student
            projects = student_solution.projects

            line = f"{student.id}"
            for project_category in ProjectCategory:
                project_preference = projects[project_category]
                project = project_preference.project
                line += f"|{project_category.value}:{project.id}"
            line += "\n"

            file.write(line)


def main():
    logs.info("Started app")

    args = get_arguments()

    # Get students preferences file path
    students_preferences_file_path = pathlib.Path(args.filepath)

    logs.info(students_preferences_file_path)

    # Get students preferences
    students_preferences_parser = StudentsPreferencesParser(students_preferences_file_path)
    students_preferences = students_preferences_parser.parse()

    logs.info(students_preferences)

    # Fix students preferences projects
    projects_preference_fixer = ProjectsPreferenceFixer(students_preferences)
    students_preferences = projects_preference_fixer.fix()

    logs.info(students_preferences)

    # Find solution
    jury_solver = JurySolver(config.SOLVER_NO_ITERATIONS, students_preferences)
    students_preferences_solutions = jury_solver.solve()

    logs.info(students_preferences_solutions)

    # Write solution
    write_file_solution(students_preferences_solutions)

    logs.info("Finished app")


if __name__ == "__main__":
    main()


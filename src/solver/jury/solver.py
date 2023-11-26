
import random

import config
from domain import StudentPreference, StudentPreferenceSolution, ProjectCategory, Student, ProjectPreference
from solver.solver import Solver
from solver.solve_error import SolveError


class JurySolver(Solver[StudentPreferenceSolution]):
    def __init__(self, no_iterations: int, students_preferences: list[StudentPreference]):
        Solver.__init__(self, no_iterations)

        self.__students_preferences = students_preferences

    def _compute_score(self, students_preferences_solutions: list[StudentPreferenceSolution]) -> int:
        score = 0

        for student_preferences_solution in students_preferences_solutions:
            selected_projects = student_preferences_solution.projects
            for project_category in ProjectCategory:
                score += selected_projects[project_category].score

        return score

    def _solve_category(self, project_category: ProjectCategory) -> dict[Student, ProjectPreference]:
        max_no_student_per_project = len(self.__students_preferences) // config.MAXIM_ID_PROJECT_CATEGORY[project_category] + 1

        no_assigned_projects = [0] * (config.MAXIM_ID_PROJECT_CATEGORY[project_category] + 1)
        random.shuffle(self.__students_preferences)

        solution = dict()
        for student_preferences in self.__students_preferences:
            student = student_preferences.student
            project_preferences = student_preferences.projects[project_category]

            found_solution = False
            for project_preference in project_preferences:
                project = project_preference.project
                if no_assigned_projects[project.id] < max_no_student_per_project:
                    no_assigned_projects[project.id] += 1
                    solution[student] = project_preference
                    found_solution = True
                    break
            if not found_solution:
                raise SolveError(f"Unable to find a solution for student: {student}")

        return solution

    def _solve(self) -> list[StudentPreferenceSolution]:
        students_preferences_solutions: dict[Student, dict[ProjectCategory, ProjectPreference]] = dict()

        for student_preferences in self.__students_preferences:
            student = student_preferences.student
            students_preferences_solutions[student] = dict()

        for project_category in ProjectCategory:
            project_category_solutions = self._solve_category(project_category)

            for student, project_preference in project_category_solutions.items():
                students_preferences_solutions[student][project_category] = project_preference 

        new_student_preferences_solutions = list()
        for student, project_preferences in students_preferences_solutions.items():
            student_preference_solution = StudentPreferenceSolution(
                student=student,
                projects=project_preferences
            )

            new_student_preferences_solutions.append(student_preference_solution)

        return new_student_preferences_solutions


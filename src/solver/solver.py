
from abc import ABC
from typing import Generic, TypeVar

from .solve_error import SolveError
from utils import logs


T = TypeVar("T")

class Solver(Generic[T], ABC):
    def __init__(self, no_iterations: int):
        assert no_iterations > 0, "Invalid number of iterations for solver"

        self.__no_iterations = no_iterations

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def _compute_score(self, solution) -> int:
        raise NotImplementedError

    def _solve(self) -> T:
        raise NotImplementedError

    @logs.FunctionDebug
    def solve(self) -> T:
        try:
            best_score = 0
            best_solution = None
            for iteration in range(self.__no_iterations):
                solution = self._solve()
                score = self._compute_score(solution)

                if best_score > score or best_solution is None:
                    best_score = score
                    best_solution = solution

                logs.info(f"{self.__class__.__name__}, Iteration: {iteration}, Solution Score: {score}")

            logs.info(f"{self.__class__.__name__}, Best Solution Score: {best_score}")

            return best_solution
        except SolveError as error:
            logs.exception(f"Failed to solve {self.__class__.__name__} because of {error}.")
            raise
        except Exception:
            logs.exception(f"Failed to solve {self.__class__.__name__} because of an unexpected exception.")
            raise


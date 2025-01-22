

class SATSolver:
    def __init__(self, clauses: list) -> None:
        self.clauses: list[list[int]] = clauses
       # self.assignments: dict[int, bool] = {}

    def _unit_propagate(self):
        pass

    def _pure_literal_elimination(self):
      pass

    def _simplify_clauses(self, literal):
      pass

    def _dpll(self):
        pass

    def solve(self):
      for clause in self.clauses:
        print(clause)


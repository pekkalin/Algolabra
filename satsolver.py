"""
Simple SAT Solver using DPLL Algorithm

This class implements a simple SAT (Boolean Satisfiability Problem) solver using 
the Davis-Putnam-Logemann-Loveland (DPLL) algorithm. The SAT solver takes as input 
a list of clauses in Conjunctive Normal Form (CNF) and determines whether the 
propositional logic formula is satisfiable. If satisfiable, it also provides a 
truth assignment for the variables.

Key Components:
- **Unit Propagation**: Simplifies the formula by assigning values to variables that 
  appear as unit clauses (clauses with a single literal).
- **Pure Literal Elimination**: Identifies literals that appear in only one polarity 
  (either positive or negative) and assigns them values to satisfy all their clauses.
- **Backtracking Search**: Selects unassigned variables, assigns values, and recursively 
  explores solutions. If a conflict is encountered, it backtracks and tries alternative assignments.

Structure:
1. `__init__`: Initializes the solver with a list of clauses and an empty assignments dictionary.
2. `_unit_propagate`: Simplifies the formula using unit clauses.
3. `_pure_literal_elimination`: Simplifies the formula by assigning pure literals.
4. `_simplify_clauses`: Updates the formula after a variable assignment.
5. `_dpll`: Implements the recursive DPLL algorithm with backtracking.
6. `solve`: Entry point for solving the SAT problem. Returns whether the formula 
   is satisfiable and, if so, the satisfying assignment.

Author: Pekka Linna
Email: pekka.j.linna@helsinki.fi

Usage:
- Instantiate the `SATSolver` class with a list of clauses.
- Call the `solve` method to determine satisfiability.

Example:
    clauses = [[1, -3, 4], [-1, 2, 3], [-2, -4]]
    solver = SATSolver(clauses)
    satisfiable, assignment = solver.solve()
"""
class SATSolver:
    def __init__(self, clauses: list) -> None:
        self.clauses: list[list[int]] = clauses
        self.assignments: dict[int, bool] = {}

    def _unit_propagate(self):
        changed = True
        while changed:
            changed = False
            unit_clauses = [c[0] for c in self.clauses if len(c) == 1]
            
            for literal in unit_clauses:
                if literal in self.assignments:
                    continue
                self.assignments[abs(literal)] = literal > 0
                self.clauses = self._simplify_clauses(literal)
                changed = True

    def _pure_literal_elimination(self) -> None:
        all_literals = [literal for clause in self.clauses for literal in clause]
        pure_literals = [l for l in set(all_literals) if -l not in all_literals]

        for literal in pure_literals:
            if abs(literal) not in self.assignments:
                self.assignments[abs(literal)] = literal > 0
                self.clauses = self._simplify_clauses(literal)

    def _simplify_clauses(self, literal) -> list[list[int]]:
        new_clauses = []
        for clause in self.clauses:
            if literal in clause:
                continue 
            new_clause = [x for x in clause if x != -literal]

            if not new_clause:
                return [[]]
            new_clauses.append(new_clause)
            
        return new_clauses

    def _dpll(self) -> bool:
        self._unit_propagate()
        self._pure_literal_elimination()

        if not self.clauses:
            return True

        if any(len(c) == 0 for c in self.clauses):
            return False

        # Choose branching variable easy way. Could be improved..
        unassigned = [l for clause in self.clauses for l in clause if abs(l) not in self.assignments]
        if not unassigned:
            return False

        var = abs(unassigned[0])

        for value in [True, False]:
            saved_clauses = [clause[:] for clause in self.clauses]
            saved_assignments = self.assignments.copy()

            self.assignments[var] = value
            self.clauses = self._simplify_clauses(var if value else -var)

            if self._dpll():
                return True

            # Return state to previous if branching was not successful
            self.clauses = saved_clauses
            self.assignments = saved_assignments

        return False

    def solve(self) -> tuple[bool, dict[int, bool]]:
        if self._dpll():
            return True, self.assignments
        else:
            return False, None


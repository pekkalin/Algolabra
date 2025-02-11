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
5. `_choose_branching_variable`: Chooses the next variable to branch on using the MOM heuristic.
6. `_dpll`: Implements the recursive DPLL algorithm with backtracking.
7. `solve`: Entry point for solving the SAT problem. Returns whether the formula 
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
from collections import Counter


class SATSolver:
    def __init__(self, clauses: list) -> None:
        self.clauses: list[list[int]] = clauses
        self.assignments: dict[int, bool] = {}

    def _choose_branching_variable(self) -> int:
        """
        Choose the next variable to branch on using the MOM (Maximum Occurrences in Minimum-sized clauses) heuristic.
        This method selects the variable that occurs most frequently in the smallest clauses,
        aiming to maximize the impact of the branching decision.
        """
        # Find the smallest clause length
        min_length = min((len(clause) for clause in self.clauses if clause), default=0)
        
        # Collect all variables in the smallest clauses
        candidates = [var for clause in self.clauses if len(clause) == min_length for var in clause]
        
        # Count occurrences
        counts = Counter(candidates)
        
        # Return the most frequent variable
        return max(counts, key=lambda var: counts[var])

    def _unit_propagate(self):
        """
        Perform unit propagation on the formula.

        This method identifies and processes unit clauses (clauses containing a 
        single literal). It assigns truth values to the variables in these unit 
        clauses to satisfy them, simplifying the formula iteratively. The process 
        continues until no more unit clauses are found.

        - Unit clauses are extracted from the list of clauses.
        - For each unit clause:
            - If the literal is already assigned, it is skipped.
            - Otherwise, the literal is assigned a truth value based on its sign.
            - The formula is simplified by removing clauses satisfied by this 
              literal and literals with the opposite value in other clauses.
        - The method repeats this process until no further changes are made.

        This operation helps reduce the search space in the SAT solving process 
        and may directly resolve simple satisfiability conditions or expose conflicts.
        """
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
        """
        Perform pure literal elimination on the formula.

        This method identifies pure literals in the formula and assigns them truth
        values to simplify the clauses. A pure literal is a variable that appears 
        only with a consistent sign (positive or negative) across all clauses.

        - All literals are extracted from the current set of clauses.
        - Pure literals are determined by checking for literals whose negation 
          does not appear in the formula.
        - For each pure literal:
            - If the literal is unassigned, assign it a truth value based on its sign.
            - Simplify the formula by removing all clauses containing the pure literal.

        This process reduces the complexity of the formula and can eliminate
        some variables and clauses directly, helping the SAT solver progress more
        efficiently.
        """
        all_literals = [literal for clause in self.clauses for literal in clause]
        pure_literals = [l for l in set(all_literals) if -l not in all_literals]

        for literal in pure_literals:
            if abs(literal) not in self.assignments:
                self.assignments[abs(literal)] = literal > 0
                self.clauses = self._simplify_clauses(literal)

    def _simplify_clauses(self, literal) -> list[list[int]]:
        """
        Simplify the list of clauses by applying the given literal's assignment.

        This function processes the current formula to simplify it based on the
        assignment of a specific literal:
        - If a clause contains the given literal, it is considered satisfied and removed.
        - If a clause contains the negation of the given literal, the negation is removed
          from the clause since it can no longer contribute to the clause's satisfaction.
        - If removing a negated literal results in an empty clause (a conflict), an empty
          clause is returned to signal the conflict.

        :param literal: The literal being assigned a truth value.
        :return: A simplified list of clauses, or an empty clause if a conflict is detected.
        """
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
        """
        Implements the DPLL (Davis-Putnam-Logemann-Loveland) algorithm to solve the SAT problem.

        The DPLL algorithm is a recursive backtracking algorithm that:
        1. Simplifies the formula through unit propagation and pure literal elimination.
        2. Checks for a solution or conflicts.
        3. Makes decisions by branching on unassigned variables and recursively attempting to solve.

        Steps:
        - Perform unit propagation to assign truth values to unit clauses.
        - Eliminate pure literals to further simplify the formula.
        - If no clauses remain, the formula is satisfiable, and the function returns `True`.
        - If an empty clause is found, a conflict exists, and the function returns `False`.
        - If neither condition is met, select an unassigned variable and attempt assignments (True or False).
        - Recursively solve the simplified formula.
        - If both branches fail, restore the previous state and backtrack.

        :return: `True` if the formula is satisfiable, `False` otherwise.
        """
        self._unit_propagate()
        self._pure_literal_elimination()

        if not self.clauses:
            return True

        if any(len(c) == 0 for c in self.clauses):
            return False
        
        # # Choose branching variable using MOM heuristic
        var = self._choose_branching_variable()

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
        """
        Solve the SAT problem using the DPLL algorithm.

        This method wraps the internal DPLL process to determine whether the SAT problem is satisfiable.
        It invokes the DPLL algorithm and returns the result along with the variable assignments if satisfiable.

        :return: 
            - A tuple where the first element is a boolean indicating satisfiability (`True` if satisfiable, `False` otherwise).
            - The second element is a dictionary mapping variables to their boolean assignments if satisfiable.
              If not satisfiable, the second element is `None`.
        """
        if self._dpll():
            return True, self.assignments
        else:
            return False, None


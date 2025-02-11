"""
This script implements a SAT solver using the DIMACS format for representing Boolean formulas.

The SAT solver reads a DIMACS file, extracts the clauses, and then attempts to solve the Boolean satisfiability problem 
using a custom SAT solver (`SATSolver`). If the formula is satisfiable, it outputs a satisfying assignment of truth 
values for the variables. If unsatisfiable, it reports that the formula cannot be satisfied.

The DIMACS format consists of:
- 'c' lines for comments
- 'p' lines indicating problem type and size
- Clauses represented as lists of integers where each integer represents a literal.

 Author: Pekka Linna
 Email: pekka.j.linna@helsinki.fi

Usage:
    poetry run python satsolver.py <DIMACS-file-name>

Where <DIMACS-file-name> is the path to the DIMACS file that contains the SAT problem.
"""
import sys

from satsolver import SATSolver


def read_file_and_create_clauses(filename) -> list[list[int]]:
    """
    Reads a DIMACS file and converts it into a list of clauses.

    This function processes the given DIMACS file, ignoring comments and problem declarations, 
    and creates a list of clauses. Each clause is represented as a list of integers, where each 
    integer corresponds to a literal in the clause. A positive integer represents a variable, 
    and a negative integer represents its negation.

    Parameters:
    - filename (str): The path to the DIMACS file containing the SAT problem.

    Returns:
    - list[list[int]]: A list of clauses, each represented as a list of integers (literals).
    """
    clauses = []
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()

            if line.startswith('c') or line.startswith('p') or not line:
                continue
            clause = list(map(int, line.split()))

            if clause[-1] == 0:
                clause.pop()
            clauses.append(clause)

    return clauses
 

def main() -> None:
    """
    Main entry point of the program.

    This function handles the command-line interface, reads the DIMACS file, and passes the list 
    of clauses to the SAT solver. It also handles displaying the results, either a satisfying 
    assignment of variables or a message indicating that the formula is unsatisfiable.

    Steps:
    - Checks if a DIMACS file is provided as a command-line argument.
    - Reads the file and creates the list of clauses using the `read_file_and_create_clauses` function.
    - Uses the `SATSolver` to attempt to solve the SAT problem.
    - Prints the result: either the satisfying assignment or a message saying the formula is unsatisfiable.
    
    Usage:
    - The file name is passed as a command-line argument when running the script.
    """

    if len(sys.argv) < 2:
        print("Usage: python satsolver.py <DIMACS-file-name>")
        sys.exit(1)

    filename = sys.argv[1]
    print(f"Reading DIMACS file: {filename}")
    
    solver = SATSolver(read_file_and_create_clauses(filename))
    sat, solution = solver.solve()
    
    if sat:
         print("Satisfiable! Solution:")
         for var, value in sorted(solution.items()):
             print(f"{var} = {value}")
    else:
         print("Unatisfiable.")
    
if __name__ == "__main__":
   main()

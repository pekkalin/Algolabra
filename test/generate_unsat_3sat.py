"""
This script generates random 3-SAT formulas using cnfgen and ensures they are unsatisfiable (UNSAT).
It uses MiniSAT to check satisfiability and modifies the formula by adding conflicting clauses if needed.

Author: Pekka Linna
Email: pekka.j.linna@helsinki.fi

Dependencies:
- cnfgen:
    Install using `poetry add cnfgen`
- MiniSAT:
    Install using `sudo apt-get install minisat` or `brew install minisat`

Example:
    Generate 5 UNSAT 3-SAT formulas with 50 variables and 200 clauses:
    `poetry run python generate_unsat_3sat.py`

    The generated formulas are saved to the directory `unit-tests/unsat`.
"""

import os
import random
import shutil
import subprocess


def check_minisat():
    """Checks if MiniSAT is installed."""
    if not shutil.which("minisat"):
        raise RuntimeError("MiniSAT is not installed! Please install it on your system.")

def generate_3sat_instance(variables=50, clauses=200):
    """Generates a random 3-SAT formula using cnfgen."""
    cnf_file = "temp.cnf"
    with open(cnf_file, "w") as f:
        subprocess.run(["poetry", "run", "cnfgen", "randkcnf", "3", str(variables), str(clauses)], stdout=f)
    return cnf_file

def is_unsat(cnf_file):
    """Checks if a CNF formula is UNSAT using MiniSAT."""
    result = subprocess.run(["minisat", cnf_file], capture_output=True, text=True)
    return "UNSATISFIABLE" in result.stdout

def add_conflicting_clause(cnf_file):
    """Adds a conflicting clause to ensure the formula becomes UNSAT."""
    with open(cnf_file, "r") as f:
        lines = f.readlines()
    
    # Find the number of variables
    for line in lines:
        if line.startswith("p cnf"):
            parts = line.split()
            num_vars = int(parts[2])
            break
    
    # Add a conflicting clause (x, ¬x)
    var = random.randint(1, num_vars)
    conflicting_clause = f"{var} 0\n{-var} 0\n"
    
    with open(cnf_file, "a") as f:
        f.write(conflicting_clause)

def generate_unsat_3sat(variables=50, clauses=200, num_instances=5, output_dir="unit-tests/unsat"):
    """Generates multiple guaranteed UNSAT 3-SAT formulas and saves them to a directory."""
    check_minisat()
    os.makedirs(output_dir, exist_ok=True)
    unsat_files = []
    for i in range(num_instances):
        cnf_file = os.path.join(output_dir, f"unsat_{i+1}.cnf")
        with open(cnf_file, "w") as f:
            subprocess.run(["poetry", "run", "cnfgen", "randkcnf", "3", str(variables), str(clauses)], stdout=f)
        while not is_unsat(cnf_file):
            add_conflicting_clause(cnf_file)
        unsat_files.append(cnf_file)
    return unsat_files

if __name__ == "__main__":
    unsat_instances = generate_unsat_3sat(50, 200, 5)
    print(f"UNSAT CNF-files saved to directory: {unsat_instances}")

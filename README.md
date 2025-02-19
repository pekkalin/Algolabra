Algolabra project, Spring 2025.  
Developer: Pekka Linna  
Email:      pekka.j.linna@helsinki.fi  

SAT Solver using the DPLL Algorithm  

The program implements a simple SAT solver (Boolean satisfiability solver) based on the DPLL (Davis-Putnam-Logemann-Loveland) algorithm.  
The program reads a DIMACS file in conjunctive normal form (CNF) and returns a satisfying truth assignment or indicates that no such assignment exists.  

Installation:  

Clone the repository:   
- https://github.com/pekkalin/Algolabra.git  

Install dependencies: 
- poetry install --no-root

Ensure that the Poetry virtual environment is active:   
- poetry shell

Run the program:  
- poetry run python main.py <DIMACS-tiedosto>

Example:  
- DIMACS-inputfile (example.cnf):

- poetry run python main.py example.cnf

    Reading DIMACS file: example.cnf  
    Satisfiable. Solution:

    -3 = True  
    1 = False  
    2 = True  

Run tests:  
cd test  
     Unit tests:  
     - poetry run pytest -s sat_unit_test.py
     - poetry run pytest -s unsat_unit_test.py

     Performance tests, one test set at a time:  
     - poetry run pytest -s perf_100_420_test.py
     - poetry run pytest -s perf_100_428_test.py
     - poetry run pytest -s perf_100_429_test.py
     - poetry run pytest -s perf_100_450_test.py
     - poetry run pytest -s perf_100_480_test.py

    All tests at once:  
    - poetry run pytest -s  







import os
import sys
import time

import pytest
from test_util import load_cnf_files

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from satsolver import SATSolver


@pytest.mark.parametrize("load_cnf_files", ["perf-tests/random-3-cnf-100-480"], indirect=True)
class TestPerf:
    def test_dpll_performance(self, load_cnf_files):
        print("Executing testset n=100, m=480:")
        for i, filename in enumerate(load_cnf_files.keys(), 1):
            print(f"{i}. {filename}")
        
        num_of_tests = len(load_cnf_files.keys())
        total_time = 0
        print()
        for filename, clauses in load_cnf_files.items():
            print(f"Testing file: {filename}")
            solver = SATSolver(clauses)
            start_time = time.time()
            sat, sol = solver.solve()
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Satisfiable: {sat}, Execution time for {filename}: {execution_time} seconds")
            print()
            total_time += execution_time

        average_time = total_time / num_of_tests
        print()
        print(f"Average execution time for testset: {average_time} seconds")
        
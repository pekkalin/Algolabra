import os

import pytest


@pytest.fixture(scope="session")
def load_cnf_files(request):
    """
    Fixture that reads all .cnf files from the 'unit-tests' directory and parses them into clauses.
    """
    print("\nLoad all .cnf-files.")
    #test_dir = "unit-tests" 
    test_dir = request.param
    print(f"Using test directory: {test_dir}")
    print()
    if not os.path.exists(test_dir):
        raise FileNotFoundError(f"Directory {test_dir} not found.")

    # Read all .cnf-files and parse them into clauses
    cnf_data = {}
    for filename in os.listdir(test_dir):
        if filename.endswith(".cnf"):
            filepath = os.path.join(test_dir, filename)
            clauses = []
            with open(filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('c') or line.startswith('p') or not line:
                        continue
                    clause = list(map(int, line.split()))
                    if clause[-1] == 0:
                        clause.pop()
                    clauses.append(clause)
            cnf_data[filename] = clauses

    if not cnf_data:
        raise FileNotFoundError(f"No .cnf files found in directory {test_dir}.")

   # print(f"{len(cnf_data)} .cnf files processed.")
    return cnf_data

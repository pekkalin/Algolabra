- Directory unit-tests includes basic unit tests and corresponding .sol-files copied from https://github.com/arminbiere/cadical
  Program does not use .sol files, but .sol-files includes solution for corresponding testcase.
  
- Directory perf-tests includes performance tests generated using https://massimolauria.net/cnfgen
- For test generation we use <cnfgen randkcnf 3 n m>

- For performance testing we use 3-SAT (n = 100) testsets close to phase transition (ratio of number of clauses and number of variables) c ≈ 4.25
  where c = m / n,
  n = number of variables,
  m = number of clauses
  
  It is experimentally shown that the hardest cases for random 3-SAT problem are the instances where the ratio of number of clauses
  and number of variables is close to 4.25.[1]

    - testset 1: c = 4.2
    - testset 2: c = 4.28
    - testset 3: c = 4.29
    - testset 4: c = 4.5  
    - testset 5: c = 4.8
   

[1] https://dl.acm.org/doi/10.5555/2832249.2832300

run tests:
     pytest -s unit_test.py
     pytest -s perf_test.py



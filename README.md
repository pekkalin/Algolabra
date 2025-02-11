Algolabra harjoitustyö, kevät 2025.
Toteuttaja: Pekka Linna
Email:      pekka.j.linna@helsinki.fi


SAT-solveri DPLL-algoritmilla.

Ohjelma toteuttaa yksinkertaisen SAT-solverin (Boolean satisfiability solver), joka perustuu DPLL (Davis-Putnam-Logemann-Loveland) -algoritmiin.
Ohjelma lukee DIMACS-tiedoston, joka on konjuktiivisessa normaalimuodossa ja palauttaa sen toteuttavan totuusjakauman tai tiedon siitää, ettei tällaista jakaumaa ole olemassa.

Asennus:

Kloonaa repository: 
- https://github.com/pekkalin/Algolabra.git

Asenna riippuvuudet: 
- poetry install --no-root

Varmista, että Poetryn virtuaaliympäristö on käytössä: 
- poetry shell

Suorita ohjelma:
- poetry run python main.py <DIMACS-tiedosto>

Esimerkki:
- DIMACS-syötetiedosto (example.cnf):

- poetry run python main.py example.cnf

    Reading DIMACS file: example.cnf
    Satisfiable. Solution:

    -3 = True
    1 = False
    2 = True

Suorita testit:
cd test
     Yksikkötestit:
     - poetry run pytest -s unit_test.py

     Suorituskykytestit testisetti kerrallan:
     - poetry run pytest -s perf_100_420_test.py
     - poetry run pytest -s perf_100_428_test.py
     - poetry run pytest -s perf_100_429_test.py
     - poetry run pytest -s perf_100_450_test.py
     - poetry run pytest -s perf_100_480_test.py

    Kaikki testit kerralla:
    - poetry run pytest -s






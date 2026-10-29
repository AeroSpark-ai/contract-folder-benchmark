# Licence for the data

- **The code** (`scoring/`, `benchmark/contracts/fetch_contracts.py`) is under the MIT licence: see [LICENSE](LICENSE).
- **The data we made**: the questions, the answer key and its decisions, the claims, the recorded answers, the results and the documentation, is under
  [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). Credit "The Contract Folder Test, AeroSpark" and CUAD.
  Every system's answers are included as recorded, so that the results can be checked.
- **The contracts and CUAD's labels** are the Contract Understanding Atticus Dataset (CUAD) v1, © The Atticus Project, under
  [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): Hendrycks, Burns, Chen and Ball, "CUAD: An Expert-Annotated NLP Dataset for Legal Contract Review", NeurIPS 2021 Datasets and Benchmarks;
  Zenodo [10.5281/zenodo.4595826](https://doi.org/10.5281/zenodo.4595826). The contracts are not stored in this repository; `benchmark/contracts/fetch_contracts.py` downloads them from CUAD. The answer key
  uses CUAD's labels as CUAD publishes them, and our own labels for the clauses CUAD does not label (`benchmark/key/our_labels/`).

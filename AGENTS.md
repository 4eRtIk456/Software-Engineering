# Agent Instructions & Guidelines: `expense-split-cli`

## 1. Project Purpose & Scope
`expense-split-cli` is a lightweight, non-sensitive Python command-line utility designed to ingest synthetic expense items from a JSON file, compute total expenditures, and divide shares among group participants.
- **Data Scope**: All sample datasets, tests, and documentation must use exclusively synthetic, fictitious names (e.g., Alex, Sam, Taylor) and sample figures. Real personal, financial, or organizational data is strictly out of scope.
- **Environment**: Standalone CLI utility running on standard Python without external service dependencies or cloud connections.

## 2. Architecture & Responsibilities
The repository maintains strict separation of concerns across modules:
- `src/calculator.py`: Pure domain logic. Implements `calculate_total` and `split_expenses`. It is responsible for all arithmetic calculations, rounding logic, and mode handling (`equal` and `weighted_double_first`). It has no dependency on CLI parsing, terminal I/O, or file system operations.
- `src/cli.py`: CLI presentation and interface layer. Uses `argparse` to handle `--file`, `--split-by`, and `--mode`. Responsible for file existence checks, JSON deserialization, participant list parsing, invoking calculator domain functions, and formatting output to stdout / error diagnostics to stderr.
- `tests/test_calculator.py`: Unit test suite using standard library `unittest`. Validates domain logic, edge cases, rounding precision, and calculation invariants.
- `sample_expenses.json`: Synthetic reference fixture used for documentation examples, manual verification, and smoke tests.
- `requirements.txt`: Project dependency specification (standard library only; no external package dependencies).

## 3. Setup & Safe Execution Commands
- **Python Version**: Python >= 3.8 (System runtime: Python 3.14+).
- **Environment**: Standard Library only. No third-party packages or virtual environment activation required.

### Verified Safe Commands
Agents working in this repository must use only the following verified execution commands:

- **Syntax & Bytecode Validation**:
  ```bash
  python3 -m py_compile src/*.py tests/*.py
  ```
- **Test Suite Execution**:
  ```bash
  python3 -m unittest discover -s tests
  ```
  *(Or targeting specific test modules)*:
  ```bash
  python3 -m unittest tests/test_calculator.py
  ```
- **CLI Smoke Test (Equal Mode)**:
  ```bash
  python3 -m src.cli --file sample_expenses.json --split-by "Alex,Sam" --mode equal
  ```
- **CLI Smoke Test (Weighted Mode)**:
  ```bash
  python3 -m src.cli --file sample_expenses.json --split-by "Alex,Sam" --mode weighted_double_first
  ```
- **Git Status / Inspection**:
  ```bash
  git status
  git diff
  git log -n 5 --oneline
  ```

## 4. Coding Conventions & Standards
- **Monetary & Currency Handling**:
  - Always use `decimal.Decimal` and `decimal.ROUND_HALF_UP` for all monetary amounts, calculations, and splits.
  - Never use IEEE 754 floating-point types (`float`) for currency or financial amounts to prevent binary representation drift and rounding errors.
  - Quantize monetary amounts to two decimal places (`Decimal('0.01')`).
- **Type Annotations**:
  - Use explicit Python type annotations on all function signatures, parameters, and return types (`typing` / built-in generics).
- **Error Handling & Input Validation**:
  - Explicitly raise `ValueError` (or appropriate specific standard library exceptions) on invalid inputs, such as unknown split modes, empty participant lists, or malformed expense records.
  - Catch domain exceptions in the CLI boundary and report friendly diagnostics to `stderr` with a non-zero exit code (`sys.exit(1)`).
- **Change Discipline**:
  - Make minimal, focused, and well-justified code changes. Do not introduce speculative abstractions, extraneous frameworks, or sweeping structural rewrites.

## 5. Test Expectations & Quality Assurance
- **Coverage for Changes**:
  - Any behavioral modification, bug fix, or new feature must be accompanied by corresponding new or updated unit tests in `tests/`.
  - Specific areas requiring test verification include edge cases (empty lists, zero participants, duplicate names, non-divisible totals with remainders).
- **Pre-Acceptance Verification**:
  - Before considering a task complete or staging commits, always run:
    1. Syntax/bytecode check: `python3 -m py_compile src/*.py tests/*.py`
    2. Full unit test suite: `python3 -m unittest discover -s tests`
    3. CLI smoke tests with both `equal` and `weighted_double_first` modes.
  - All tests must pass cleanly (exit code `0`) with zero regressions.

## 6. Strictly Forbidden Actions
To maintain repository safety, integrity, and compliance, the following actions are strictly prohibited:
- **No Credentials or Real Data**: Never add, store, or commit secrets, API keys, access tokens, passwords, or real personal/financial data. Use only synthetic fixtures (e.g., Alex, Sam, Taylor).
- **No Production Deployments or Remote Publishes**: Do not attempt to push to remote Git repositories, publish packages (e.g., PyPI), or deploy to production/cloud infrastructure without explicit user authorization.
- **No Destructive Filesystem or Git Commands**: Never execute destructive commands such as `rm -rf` outside temporary scratch/test directories, force-pushing (`git push --force`), rewriting published history (`git rebase` / `git reset --hard` on tracked branches), or deleting repository histories.
- **No Unreviewed Dependency Changes**: Do not add third-party dependencies to `requirements.txt` or introduce external package installations without prior review and user consent.

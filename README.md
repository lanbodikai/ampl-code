# AMPL Course Project

## Recommended Run Order

1. `project_data.dat`
2. `task1.mod` + `task1.run`
3. `task2.mod` + `task2.run`
4. `task3.mod` + `task3.run`
5. `task4.mod` + `task4.run`
6. `task5.run`
7. `memo.md`
8. `results.json`

## What Each File Does

- `project_data.dat`: shared data file built from the three appendix tables.
- `task1.mod`, `task1.run`: Task 1 venue-opening and assignment model.
- `task2.mod`, `task2.run`: multi-week assignment model.
- `task3.mod`, `task3.run`: ticket-revenue extension of Task 2.
- `task4.mod`, `task4.run`: bus-network MIP.
- `task5.run`: scenario reruns of Task 4.
- `memo.md`: modeling notes, verified outputs, and scenario interpretation.
- `analyze_project.py`: local verification script used to reproduce the reported results.
- `results.json`: stored verification output from the script.

## Running With AMPL

If you installed AMPL through `amplpy.modules`, these commands work:

```bash
python3 -m amplpy.modules run ampl task1.run
python3 -m amplpy.modules run ampl task2.run
python3 -m amplpy.modules run ampl task3.run
python3 -m amplpy.modules run ampl task4.run
python3 -m amplpy.modules run ampl task5.run
```

The `.run` files already set `option solver highs;`.

## Current AMPL Status

- `task1.run`: executes successfully with AMPL + HiGHS.
- `task2.run`: executes successfully with AMPL + HiGHS.
- `task3.run`: executes successfully with AMPL + HiGHS.
- `task4.run`: parses correctly, but the current AMPL demo license blocks the solve because the model is larger than the demo limit.
- `task5.run`: blocked for the same reason as Task 4.

The current AMPL error on Tasks 4-5 is:

```text
Sorry, a demo license for AMPL is limited to 2000 variables
and 2000 constraints and objectives (after presolve) for linear
problems.  You have 4625 variables, 11839 constraints, and 1 objective.
```

## How To Unblock Task 4-5 In AMPL

The official AMPL Community Edition removes size limits but requires a valid license UUID and internet connectivity.

After getting a UUID from the AMPL Community Edition portal, activate it with:

```bash
python3 -m amplpy.modules activate <license-uuid>
```

Then restart the AMPL command and rerun:

```bash
python3 -m amplpy.modules run ampl task4.run
python3 -m amplpy.modules run ampl task5.run
```

## Notes

- `project_data.dat` was normalized so the optional `venue_name` and `sport_name` tables load correctly in AMPL.
- `task1.mod`, `task2.mod`, `task3.mod`, and `task4.mod` now all accept the same shared data file.

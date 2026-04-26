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
- `MIP_STUDY_GUIDE.md`: concise study notes on the main MIP techniques used in the project.
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

The `.run` files for Tasks 4-5 are set to `option solver gurobi;`.

## Current AMPL Status

- `task1.run`, `task2.run`, and `task3.run` have been verified in AMPL.
- Tasks 4-5 use the full bus-network MIP and are configured to run with Gurobi.
- Runtime for Tasks 4-5 can be substantial because the bus-network model is much larger than Tasks 1-3.

## Notes

- `project_data.dat` was normalized so the optional `venue_name` and `sport_name` tables load correctly in AMPL.
- `task1.mod`, `task2.mod`, `task3.mod`, and `task4.mod` now all accept the same shared data file.
- Tuple-indexed AMPL variables must be displayed with explicit indices such as `pair[i,k]` and `triple[i,k,l]`.

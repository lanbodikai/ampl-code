# IEOR 162 Project Memo

## What Is In This Repo

- `project_data.dat`: Person C's combined data file from the venue table, sport table, and eligibility matrix.
- `task1.mod`: original Task 1 model already in the fork.
- `task2.mod`, `task3.mod`, `task4.mod`: AMPL models for Tasks 2-4.
- `task2.run`, `task3.run`, `task4.run`, `task5.run`: AMPL run files.
- `analyze_project.py`: local verification script used to solve the tasks and write `results.json`.

## Modeling Flow

### Task 1

- Decision variables:
- `y[i] = 1` if venue `i` is opened.
- `x[i,j] = 1` if sport `j` is assigned to venue `i`.
- Objective:
- Minimize fixed venue opening cost.
- Core constraints:
- Each sport is assigned exactly once.
- A sport can only go to an eligible venue.
- A venue can host at most `kappa[i]` sports.

### Task 2

- New idea:
- Sports now choose a single week `t`, and all required sessions for that sport happen in that week.
- New variables:
- `z[j,t] = 1` if sport `j` is scheduled in week `t`.
- `x[i,j,t] = 1` if venue `i` hosts one slot of sport `j` in week `t`.
- `active[i,t] = 1` if venue `i` is used in week `t`.
- Key constraints:
- `sum_t z[j,t] = 1`
- `sum_i x[i,j,t] = R[j] * z[j,t]`
- `sum_j x[i,j,t] = active[i,t]`
- `active[i,t] = 0` for weeks past `kappa[i]`
- Interpretation:
- Multi-session sports such as Athletics, Gymnastics, Soccer, and Basketball now need multiple venues in the same week.

### Task 3

- New variable:
- `sold[i,j,t] >= 0` for tickets sold for sport `j` at venue `i` in week `t`.
- Linearization of `min(D[j], C[i])`:
- `sold[i,j,t] <= D[j] * x[i,j,t]`
- `sold[i,j,t] <= C[i] * x[i,j,t]`
- Because the objective subtracts ticket revenue, the model pushes `sold[i,j,t]` to the maximum feasible value, so this reproduces `min(D[j], C[i])` whenever `x[i,j,t] = 1`.
- Objective:
- Minimize fixed cost minus `10 * sold`.

### Task 4

- New binary network variables:
- `pair[i,k]` for two-venue bus networks.
- `triple[i,k,l]` for three-venue bus networks.
- Each venue can appear in at most one selected network.
- New weekly activation variables:
- `pair_on[i,k,t]` means the pair network is active in week `t`.
- `all3[i,k,l,t]` means all three triple-network venues are active in week `t`.
- `only_ik`, `only_il`, `only_kl` capture the two-active-venues case inside a triple network.
- Ticket variables:
- `base_week[i,t]` is the Task 3 ticket volume before bus spillovers.
- `extra_week[i,t]` is the additional ticket volume caused by bus connectivity.
- Flow variables:
- Pair flows implement the `10%` spillover in each direction.
- Triple flows implement the `7% + 7%` spillover when all three venues are active.
- Pair-only flows inside triples implement the fallback `10%` rule when only two venues in the triple are active in a week.
- Capacity logic:
- `base_week[i,t] + extra_week[i,t] <= C[i] * active[i,t]`
- So bus spillovers cannot create tickets beyond venue capacity.

## Verified Results

### Task 1

- Minimum fixed cost: `2350`
- Open venues: `V2, V4, V5, V7, V8, V9, V10`
- Assignment:
- `S1 -> V2`
- `S2 -> V5`
- `S3 -> V5`
- `S4 -> V4`
- `S5 -> V4`
- `S6 -> V9`
- `S7 -> V7`
- `S8 -> V10`
- `S9 -> V10`
- `S10 -> V9`
- `S11 -> V2`
- `S12 -> V8`
- `S13 -> V8`
- `S14 -> V2`
- `S15 -> V7`

### Task 2

- Minimum fixed cost: `2850`
- Open venues: `V1, V2, V3, V5, V7, V8, V9, V10`
- Week / venue schedule:
- `S1`: week 1 at `V1, V2`
- `S2`: week 1 at `V5`
- `S3`: week 2 at `V3, V5`
- `S4`: week 3 at `V1, V2`
- `S5`: week 1 at `V3, V9`
- `S6`: week 2 at `V9`
- `S7`: week 2 at `V7`
- `S8`: week 2 at `V8`
- `S9`: week 1 at `V10`
- `S10`: week 3 at `V3`
- `S11`: week 2 at `V1`
- `S12`: week 2 at `V10`
- `S13`: week 1 at `V8`
- `S14`: week 2 at `V2`
- `S15`: week 1 at `V7`
- Implied ticket volume under Task 3 logic: `260`

### Task 3

- Minimum net cost: `250`
- Open venues: `V1, V2, V3, V5, V7, V8, V9, V10`
- Total tickets sold: `260`
- Change versus Task 2:
- The open venue set stays the same.
- The week pattern shifts slightly, but the ticket total is unchanged at `260`.

### Task 4

- Best verified Task 4 solution found in local solve:
- Bus networks:
- Triple `V1-V2-V3`
- Triple `V5-V7-V9`
- Minimum net cost: `-28.7`
- Base tickets: `260`
- Extra tickets from buses: `5.46`
- Total tickets: `265.46`
- Schedule:
- `S1`: week 1 at `V1, V2`
- `S2`: week 2 at `V5`
- `S3`: week 1 at `V3, V5`
- `S4`: week 2 at `V1, V2`
- `S5`: week 2 at `V3, V9`
- `S6`: week 1 at `V9`
- `S7`: week 2 at `V7`
- `S8`: week 2 at `V10`
- `S9`: week 1 at `V10`
- `S10`: week 3 at `V3`
- `S11`: week 3 at `V1`
- `S12`: week 2 at `V8`
- `S13`: week 1 at `V8`
- `S14`: week 3 at `V2`
- `S15`: week 1 at `V7`

## Task 5 Scenarios

| Scenario | Objective | Networks | Total Tickets |
| --- | ---: | --- | ---: |
| Base Task 4 (`$10`) | `-28.70` | triples `V1-V2-V3`, `V5-V7-V9` | `265.46` |
| `$5` per ticket | `1430.65` | triples `V1-V2-V3`, `V5-V7-V9` | `265.46` |
| `$15` per ticket | `-1496.55` | triples `V1-V2-V3`, `V5-V7-V9`, pair `V8-V10` | `265.88` |
| Demand `-10%` | `239.78` | triples `V1-V2-V3`, `V5-V7-V9` | `240.914` |

### Interpretation

- The base, `$5`, and demand-down scenarios all keep the same bus structure.
- The `$15` scenario makes one extra pair, `V8-V10`, worth paying for because the higher ticket value makes even a small spillover profitable.
- Demand reduced by `10%` cuts both the base sales and the spillover opportunity, so the objective worsens relative to Task 4 even though the chosen bus structure stays the same.

## Cross-Evaluation Table

Numbers below are total cost after taking the solution from the column and evaluating it under the scenario in the row.

| Evaluated Under | Base solution | `$5` solution | `$15` solution | Demand `-10%` solution |
| --- | ---: | ---: | ---: | ---: |
| Base (`$10`) | `-28.70` | `-28.70` | `-27.70` | `-28.70` |
| `$5` | `1430.65` | `1430.65` | `1441.15` | `1430.65` |
| `$15` | `-1488.05` | `-1488.05` | `-1496.55` | `-1488.05` |
| Demand `-10%` | `239.78` | `239.78` | `241.88` | `239.78` |

### Suboptimality Readout

- The `$15` solution is the only one that differs structurally; it adds the pair `V8-V10`.
- That extra pair helps under `$15`, but it is slightly worse in the other three scenarios because the extra spillover is not valuable enough to justify the added fixed bus cost.
- The base, `$5`, and demand-down solutions are effectively the same decision pattern in this data set.

## Notes On Verification

- `analyze_project.py` was used to verify the reported numbers and write `results.json`.
- Tasks 1-3 were solved directly as MIPs.
- For Tasks 4-5, the local verification path solved the full scheduling model exactly for fixed bus configurations and searched across strong seed configurations. The AMPL model in `task4.mod` is still the full bus-network MIP formulation.

# IEOR 162 Project — Person C Starter Pack

## What Person C owns
- Build the AMPL `.dat` file from Tables 1–3.
- Build Task 1 model.
- Write executive summary, introduction/background, and non-technical results sections.
- Assemble final report once Person A and Person B send their results.

## Task 1 formulation
### Sets
- `I`: venues
- `J`: sports

### Parameters
- `c_i`: fixed cost to open venue `i`
- `kappa_i`: maximum number of sports venue `i` can host
- `A_ij`: eligibility indicator, equals 1 if venue `i` can host sport `j`

### Decision variables
- `y_i = 1` if venue `i` is opened
- `x_ij = 1` if sport `j` is assigned to venue `i`

### Objective
Minimize total fixed opening cost:
\[
\min \sum_{i \in I} c_i y_i
\]

### Constraints
1. Every sport assigned exactly once:
\[
\sum_{i \in I} x_{ij} = 1 \quad \forall j \in J
\]
2. Can only assign to opened venues:
\[
 x_{ij} \le y_i \quad \forall i \in I, j \in J
\]
3. Must respect venue-sport eligibility:
\[
 x_{ij} \le A_{ij} \quad \forall i \in I, j \in J
\]
4. Each venue can host at most `kappa_i` sports:
\[
\sum_{j \in J} x_{ij} \le \kappa_i \quad \forall i \in I
\]

## One optimal Task 1 solution
Minimum total fixed cost: **2350** thousand dollars.

Opened venues:
- V2, V4, V5, V7, V8, V9, V10

One optimal assignment:
- S1 -> V2
- S2 -> V5
- S3 -> V5
- S4 -> V4
- S5 -> V4
- S6 -> V9
- S7 -> V7
- S8 -> V8
- S9 -> V10
- S10 -> V9
- S11 -> V2
- S12 -> V10
- S13 -> V8
- S14 -> V2
- S15 -> V7

There is also another optimal solution with the same total cost that swaps some assignments across V6/V7/V9 while keeping the same objective value.

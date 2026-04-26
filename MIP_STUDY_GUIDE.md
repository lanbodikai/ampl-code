# IEOR 162 MIP Study Guide

## What The Instructor Wants You To Learn

This project is not just about getting one answer. The main learning goal is to turn verbal planning rules into a clean mixed-integer optimization model.

The instructor is likely testing whether you can:

- identify the right decision variables
- translate English rules into linear constraints
- use binary variables for yes/no decisions
- link strategic decisions and operational decisions
- linearize nonlinear expressions like `min()`
- model conditional logic with extra binaries instead of `if` statements
- organize AMPL sets, parameters, variables, and indexed constraints clearly
- compare scenario solutions and explain why they change

## Core MIP Principles In This Project

### 1. Binary Open/Close Decisions

Task 1 starts with the classic facility-location pattern:

- `y[i] = 1` if venue `i` is opened
- `x[i,j] = 1` if sport `j` is assigned to venue `i`

Main technique:

```ampl
subject to OpenIfAssigned{i in I, j in J}:
    x[i,j] <= y[i];
```

Principle:
- if a sport is assigned to a venue, that venue must be open
- this is a standard linking constraint in MIP

### 2. Assignment / Covering Constraints

Task 1 also checks whether you know how to force complete assignment:

```ampl
subject to AssignEachSport{j in J}:
    sum{i in I} x[i,j] = 1;
```

Principle:
- every sport must be covered exactly once
- `=` means exact assignment
- `<=` would mean optional assignment
- `>=` would mean covering, but possibly multiple times

### 3. Capacity-Like Counting Constraints

Venue sport limits are modeled by counting how many sports use a venue:

```ampl
subject to VenueSportLimit{i in I}:
    sum{j in J} x[i,j] <= kappa[i];
```

Principle:
- not every capacity is about seats
- some capacities are counts of activities, weeks, machines, or slots

### 4. Time-Indexed Formulations

Task 2 is the key modeling jump.

New variables:

- `x[i,j,t] = 1` if venue `i` hosts sport `j` in week `t`
- `z[j,t] = 1` if sport `j` is scheduled in week `t`
- `active[i,t] = 1` if venue `i` is used in week `t`

Main technique:

```ampl
subject to PickOneWeek{j in J}:
    sum {t in T} z[j,t] = 1;

subject to RequiredSlots{j in J, t in T}:
    sum {i in I} x[i,j,t] = R[j] * z[j,t];
```

Principle:
- time indexing is often the cleanest way to model scheduling
- `z[j,t]` chooses the week
- `R[j] * z[j,t]` forces the correct number of simultaneous venue slots in that chosen week

This is one of the most important ideas in the project.

### 5. Turning Activity Into Binary State

Task 2 also uses:

```ampl
subject to VenueWeekActivity{i in I, t in T}:
    sum {j in J} x[i,j,t] = active[i,t];
```

Principle:
- if a venue can host at most one sport per week, the sum is either `0` or `1`
- that makes `active[i,t]` a clean derived binary flag
- these activity flags become extremely useful later for conditional logic

### 6. Linearizing `min(D[j], C[i])`

Task 3 is the main linearization exercise.

We want ticket sales at a venue/session to equal:

`min(demand, capacity)`

But AMPL MIP models should avoid raw nonlinear `min()` inside the objective/constraints unless the solver setup supports it well.

Standard linearization:

```ampl
var sold{I,J,T} >= 0;

subject to SalesByDemand{i in I, j in J, t in T}:
    sold[i,j,t] <= demand_scale * D[j] * x[i,j,t];

subject to SalesByCapacity{i in I, j in J, t in T}:
    sold[i,j,t] <= C[i] * x[i,j,t];
```

Why this works:
- `sold` is in the objective with a negative coefficient, so the solver wants it as large as possible
- therefore it gets pushed up to the largest feasible value
- the largest feasible value is exactly `min(demand, capacity)` when `x=1`

This is a very common MIP trick:
- introduce an auxiliary variable
- upper-bound it by every limiting factor
- let the objective force it to the right value

### 7. Conditional Logic Without `if`

Task 4 is really about conditional logic in linear form.

Examples of the English rules:
- a pair network only helps if both venues are active that week
- a triple gives `7% + 7%` only if all three are active
- if only two of the triple are active, it behaves like a pair

You cannot write this in MIP as:

```text
if venue i and venue k are active then ...
```

Instead, you create binary state variables such as:

- `pair_on[i,k,t]`
- `all3[i,k,l,t]`
- `only_ik[i,k,l,t]`

and define them with linear constraints.

Example:

```ampl
subject to PairOnUpperPair{(i,k) in PAIRS, t in T}:
    pair_on[i,k,t] <= pair[i,k];

subject to PairOnUpperI{(i,k) in PAIRS, t in T}:
    pair_on[i,k,t] <= active[i,t];

subject to PairOnUpperK{(i,k) in PAIRS, t in T}:
    pair_on[i,k,t] <= active[k,t];

subject to PairOnLower{(i,k) in PAIRS, t in T}:
    pair_on[i,k,t] >= pair[i,k] + active[i,t] + active[k,t] - 2;
```

Principle:
- this encodes logical AND
- `pair_on = 1` exactly when all three conditions hold

This is one of the most important MIP patterns to know.

### 8. Big-M Thinking

Even if your model does not literally use a huge `M`, the logic is the same:

- use a binary variable to turn a constraint on or off
- when the binary is `0`, the corresponding flow/sales/assignment must also be `0`

Example:

```ampl
flow_pair_ik[i,k,t] <= 0.10 * C[i] * pair_on[i,k,t];
```

Principle:
- if `pair_on = 0`, the right-hand side is `0`, so no extra flow is allowed
- if `pair_on = 1`, the flow is allowed up to the intended limit

That is the same core logic as Big-M modeling, just with a naturally tight bound instead of an arbitrary huge number.

### 9. Tight Bounds Matter

In MIP, tighter bounds solve faster.

Good:

```ampl
flow3_ik[i,k,l,t] <= 0.07 * C[i] * all3[i,k,l,t];
```

Bad:

```ampl
flow3_ik[i,k,l,t] <= 1000000 * all3[i,k,l,t];
```

Principle:
- use the smallest valid bound you can justify from the data
- tighter models usually branch faster and solve more reliably

### 10. Symmetry And Combinatorial Explosion

Task 4 becomes hard because:

- you have many candidate pairs and triples
- each can be selected or not
- weekly activation interacts with scheduling decisions

This is why solver choice matters.

Principle:
- harder MIPs are often not “wrong,” just combinatorially large
- this is why Gurobi is a better fit than HiGHS for Tasks 4-5

### 11. Scenario Analysis Is Not Just Re-solving

Task 5 wants two things:

- the optimal solution under each scenario
- cross-evaluation of one scenario’s solution under the other scenarios

Principle:
- sensitivity analysis is about both structural change and performance degradation
- “Does the plan change?” and “How much does it hurt if we keep the wrong plan?” are different questions

## Good AMPL Coding Practice

### Use Sets Cleanly

```ampl
set I ordered;
set J ordered;
set T ordered := 1..Tmax;
```

Why:
- keeps indexing readable
- useful for tuple construction and ordered subsets

### Keep Data And Model Separate

Good structure:
- `.mod` = logic
- `.dat` = numbers
- `.run` = execution choices

That separation is exactly what instructors usually want.

### Name Variables By Meaning, Not Just By Shape

Better:
- `active[i,t]`
- `base_week[i,t]`
- `pair_on[i,k,t]`

Worse:
- `u1[i,t]`
- `q3[i,k,t]`

Principle:
- report writing is easier when variable names already explain the logic

### Use Derived Variables To Make Later Constraints Easier

Example:

```ampl
subject to BaseWeekDef{i in I, t in T}:
    base_week[i,t] = sum {j in J} sold[i,j,t];
```

Principle:
- sometimes you add a variable not because it is mathematically necessary, but because it makes the rest of the model much clearer

### Be Careful With Tuple Indexing

If a set has dimension 2:

```ampl
set PAIRS within {I,I};
```

then you usually access the variable with:

```ampl
pair[i,k]
```

not:

```ampl
pair[p]
```

Similarly for triples:

```ampl
triple[i,k,l]
```

This is an important AMPL syntax habit.

### Keep `.run` Files Practical

Example:

```ampl
reset;
model task4.mod;
data project_data.dat;
option solver gurobi;
solve;
display TotalCost;
```

Principle:
- `.run` files should be reproducible and minimal
- do not bury core logic in the `.run` file

## What To Say In A Report

For each task, explain:

1. what decisions the model chooses
2. what the objective means
3. what each main constraint family enforces
4. what new modeling idea was added relative to the previous task
5. what changed in the solution and why

Example progression:

- Task 1: basic facility opening and assignment
- Task 2: time-indexed scheduling and multi-slot events
- Task 3: auxiliary-variable linearization for ticket sales
- Task 4: conditional network effects using binary logic and bounded flows
- Task 5: scenario comparison and suboptimality analysis

## The Main Techniques To Remember

If you only remember a short list, remember these:

- linking constraints: `x <= y`
- assignment constraints: `sum x = 1`
- time-indexed variables for scheduling
- auxiliary variables for linearization
- AND logic with binary lower/upper bounds
- tight Big-M style bounds using real capacities
- scenario re-evaluation, not just scenario re-optimization

## One Short Mental Model

The whole project is basically:

- choose venues
- assign sports
- assign weeks
- compute tickets
- add network effects
- compare plans under uncertainty

That is the core MIP workflow your instructor wants you to practice:

- define decisions
- define feasibility
- define economics
- linearize logic
- solve
- interpret

set I;  # venues
set J;  # sports

param c{I} >= 0;                 # fixed opening cost (thousand $)
param C{I} >= 0;                 # capacity (unused in Task 1, kept for consistency)
param kappa{I} >= 0, integer;    # max number of sports at venue i
param D{J} >= 0;                 # demand (unused in Task 1, kept for consistency)
param R{J} >= 0, integer;        # required sessions (unused in Task 1, kept for consistency)
param A{I,J} binary;             # eligibility matrix

var y{I} binary;                 # 1 if venue i is opened
var x{I,J} binary;               # 1 if sport j assigned to venue i

minimize TotalCost:
    sum{i in I} c[i] * y[i];

subject to AssignEachSport{j in J}:
    sum{i in I} x[i,j] = 1;

subject to OpenIfAssigned{i in I, j in J}:
    x[i,j] <= y[i];

subject to RespectEligibility{i in I, j in J}:
    x[i,j] <= A[i,j];

subject to VenueSportLimit{i in I}:
    sum{j in J} x[i,j] <= kappa[i];

solve;

printf "\nOptimal total fixed cost (thousand $): %g\n", TotalCost;
printf "\nOpened venues:\n";
for {i in I: y[i] > 0.5} {
    printf "%s\n", i;
}

printf "\nAssignments:\n";
for {i in I, j in J: x[i,j] > 0.5} {
    printf "%s -> %s\n", j, i;
}

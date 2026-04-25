set I ordered;
set J ordered;

param c{I} >= 0;
param C{I} >= 0;
param kappa{I} >= 0, integer;
param D{J} >= 0;
param R{J} >= 1, integer;
param A{I,J} binary;
param venue_name{I} symbolic default "";
param sport_name{J} symbolic default "";

param Tmax integer >= 1 := max {i in I} kappa[i];
set T ordered := 1..Tmax;

var y{I} binary;
var x{I,J,T} binary;
var z{J,T} binary;
var active{I,T} binary;

minimize TotalCost:
    sum {i in I} c[i] * y[i];

subject to PickOneWeek{j in J}:
    sum {t in T} z[j,t] = 1;

subject to RequiredSlots{j in J, t in T}:
    sum {i in I} x[i,j,t] = R[j] * z[j,t];

subject to VenueWeekActivity{i in I, t in T}:
    sum {j in J} x[i,j,t] = active[i,t];

subject to InvalidWeeks{i in I, t in T: t > kappa[i]}:
    active[i,t] = 0;

subject to OpenIfActive{i in I, t in T}:
    active[i,t] <= y[i];

subject to Eligibility{i in I, j in J, t in T}:
    x[i,j,t] <= A[i,j];

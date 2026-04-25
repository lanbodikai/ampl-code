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

param ticket_value >= 0 default 10;
param demand_scale >= 0 default 1;
param bus_cost >= 0 default 20;

param Tmax integer >= 1 := max {i in I} kappa[i];
set T ordered := 1..Tmax;

set PAIRS within {I,I} :=
    setof {i in I, k in I: ord(i) < ord(k)} (i,k);

set TRIPLES within {I,I,I} :=
    setof {i in I, k in I, l in I: ord(i) < ord(k) and ord(k) < ord(l)} (i,k,l);

var y{I} binary;
var x{I,J,T} binary;
var z{J,T} binary;
var active{I,T} binary;
var sold{I,J,T} >= 0;
var base_week{I,T} >= 0;
var extra_week{I,T} >= 0;

var pair{PAIRS} binary;
var triple{TRIPLES} binary;

var pair_on{(i,k) in PAIRS, t in T} binary;
var all3{(i,k,l) in TRIPLES, t in T} binary;
var only_ik{(i,k,l) in TRIPLES, t in T} binary;
var only_il{(i,k,l) in TRIPLES, t in T} binary;
var only_kl{(i,k,l) in TRIPLES, t in T} binary;

var flow_pair_ik{(i,k) in PAIRS, t in T} >= 0;
var flow_pair_ki{(i,k) in PAIRS, t in T} >= 0;

var flow3_ik{(i,k,l) in TRIPLES, t in T} >= 0;
var flow3_il{(i,k,l) in TRIPLES, t in T} >= 0;
var flow3_ki{(i,k,l) in TRIPLES, t in T} >= 0;
var flow3_kl{(i,k,l) in TRIPLES, t in T} >= 0;
var flow3_li{(i,k,l) in TRIPLES, t in T} >= 0;
var flow3_lk{(i,k,l) in TRIPLES, t in T} >= 0;

var flow2_ik{(i,k,l) in TRIPLES, t in T} >= 0;
var flow2_ki{(i,k,l) in TRIPLES, t in T} >= 0;
var flow2_il{(i,k,l) in TRIPLES, t in T} >= 0;
var flow2_li{(i,k,l) in TRIPLES, t in T} >= 0;
var flow2_kl{(i,k,l) in TRIPLES, t in T} >= 0;
var flow2_lk{(i,k,l) in TRIPLES, t in T} >= 0;

minimize TotalCost:
    sum {i in I} c[i] * y[i]
    + bus_cost * sum {(i,k) in PAIRS} pair[i,k]
    + bus_cost * sum {(i,k,l) in TRIPLES} triple[i,k,l]
    - ticket_value * (
        sum {i in I, t in T} base_week[i,t]
        + sum {i in I, t in T} extra_week[i,t]
    );

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

subject to SalesByDemand{i in I, j in J, t in T}:
    sold[i,j,t] <= demand_scale * D[j] * x[i,j,t];

subject to SalesByCapacity{i in I, j in J, t in T}:
    sold[i,j,t] <= C[i] * x[i,j,t];

subject to BaseWeekDef{i in I, t in T}:
    base_week[i,t] = sum {j in J} sold[i,j,t];

subject to VenueCapacityWithBus{i in I, t in T}:
    base_week[i,t] + extra_week[i,t] <= C[i] * active[i,t];

subject to OneNetworkPerVenue{i in I}:
    sum {(i,k) in PAIRS} pair[i,k]
    + sum {(k,i) in PAIRS} pair[k,i]
    + sum {(i,k,l) in TRIPLES} triple[i,k,l]
    + sum {(k,i,l) in TRIPLES} triple[k,i,l]
    + sum {(k,l,i) in TRIPLES} triple[k,l,i]
    <= 1;

subject to PairOnUpperPair{(i,k) in PAIRS, t in T}:
    pair_on[i,k,t] <= pair[i,k];

subject to PairOnUpperI{(i,k) in PAIRS, t in T}:
    pair_on[i,k,t] <= active[i,t];

subject to PairOnUpperK{(i,k) in PAIRS, t in T}:
    pair_on[i,k,t] <= active[k,t];

subject to PairOnLower{(i,k) in PAIRS, t in T}:
    pair_on[i,k,t] >= pair[i,k] + active[i,t] + active[k,t] - 2;

subject to PairFlowIKBase{(i,k) in PAIRS, t in T}:
    flow_pair_ik[i,k,t] <= 0.10 * base_week[i,t];

subject to PairFlowIKActive{(i,k) in PAIRS, t in T}:
    flow_pair_ik[i,k,t] <= 0.10 * C[i] * pair_on[i,k,t];

subject to PairFlowKIBase{(i,k) in PAIRS, t in T}:
    flow_pair_ki[i,k,t] <= 0.10 * base_week[k,t];

subject to PairFlowKIActive{(i,k) in PAIRS, t in T}:
    flow_pair_ki[i,k,t] <= 0.10 * C[k] * pair_on[i,k,t];

subject to All3UpperTriple{(i,k,l) in TRIPLES, t in T}:
    all3[i,k,l,t] <= triple[i,k,l];

subject to All3UpperI{(i,k,l) in TRIPLES, t in T}:
    all3[i,k,l,t] <= active[i,t];

subject to All3UpperK{(i,k,l) in TRIPLES, t in T}:
    all3[i,k,l,t] <= active[k,t];

subject to All3UpperL{(i,k,l) in TRIPLES, t in T}:
    all3[i,k,l,t] <= active[l,t];

subject to All3Lower{(i,k,l) in TRIPLES, t in T}:
    all3[i,k,l,t] >= triple[i,k,l] + active[i,t] + active[k,t] + active[l,t] - 3;

subject to OnlyIKUpperTriple{(i,k,l) in TRIPLES, t in T}:
    only_ik[i,k,l,t] <= triple[i,k,l];

subject to OnlyIKUpperI{(i,k,l) in TRIPLES, t in T}:
    only_ik[i,k,l,t] <= active[i,t];

subject to OnlyIKUpperK{(i,k,l) in TRIPLES, t in T}:
    only_ik[i,k,l,t] <= active[k,t];

subject to OnlyIKUpperL{(i,k,l) in TRIPLES, t in T}:
    only_ik[i,k,l,t] <= 1 - active[l,t];

subject to OnlyIKLower{(i,k,l) in TRIPLES, t in T}:
    only_ik[i,k,l,t] >= triple[i,k,l] + active[i,t] + active[k,t] - active[l,t] - 2;

subject to OnlyILUpperTriple{(i,k,l) in TRIPLES, t in T}:
    only_il[i,k,l,t] <= triple[i,k,l];

subject to OnlyILUpperI{(i,k,l) in TRIPLES, t in T}:
    only_il[i,k,l,t] <= active[i,t];

subject to OnlyILUpperL{(i,k,l) in TRIPLES, t in T}:
    only_il[i,k,l,t] <= active[l,t];

subject to OnlyILUpperK{(i,k,l) in TRIPLES, t in T}:
    only_il[i,k,l,t] <= 1 - active[k,t];

subject to OnlyILLower{(i,k,l) in TRIPLES, t in T}:
    only_il[i,k,l,t] >= triple[i,k,l] + active[i,t] + active[l,t] - active[k,t] - 2;

subject to OnlyKLUpperTriple{(i,k,l) in TRIPLES, t in T}:
    only_kl[i,k,l,t] <= triple[i,k,l];

subject to OnlyKLUpperK{(i,k,l) in TRIPLES, t in T}:
    only_kl[i,k,l,t] <= active[k,t];

subject to OnlyKLUpperL{(i,k,l) in TRIPLES, t in T}:
    only_kl[i,k,l,t] <= active[l,t];

subject to OnlyKLUpperI{(i,k,l) in TRIPLES, t in T}:
    only_kl[i,k,l,t] <= 1 - active[i,t];

subject to OnlyKLLower{(i,k,l) in TRIPLES, t in T}:
    only_kl[i,k,l,t] >= triple[i,k,l] + active[k,t] + active[l,t] - active[i,t] - 2;

subject to All3FlowIKBase{(i,k,l) in TRIPLES, t in T}:
    flow3_ik[i,k,l,t] <= 0.07 * base_week[i,t];

subject to All3FlowIKOn{(i,k,l) in TRIPLES, t in T}:
    flow3_ik[i,k,l,t] <= 0.07 * C[i] * all3[i,k,l,t];

subject to All3FlowILBase{(i,k,l) in TRIPLES, t in T}:
    flow3_il[i,k,l,t] <= 0.07 * base_week[i,t];

subject to All3FlowILOn{(i,k,l) in TRIPLES, t in T}:
    flow3_il[i,k,l,t] <= 0.07 * C[i] * all3[i,k,l,t];

subject to All3FlowKIBase{(i,k,l) in TRIPLES, t in T}:
    flow3_ki[i,k,l,t] <= 0.07 * base_week[k,t];

subject to All3FlowKIOn{(i,k,l) in TRIPLES, t in T}:
    flow3_ki[i,k,l,t] <= 0.07 * C[k] * all3[i,k,l,t];

subject to All3FlowKLBase{(i,k,l) in TRIPLES, t in T}:
    flow3_kl[i,k,l,t] <= 0.07 * base_week[k,t];

subject to All3FlowKLOn{(i,k,l) in TRIPLES, t in T}:
    flow3_kl[i,k,l,t] <= 0.07 * C[k] * all3[i,k,l,t];

subject to All3FlowLIBase{(i,k,l) in TRIPLES, t in T}:
    flow3_li[i,k,l,t] <= 0.07 * base_week[l,t];

subject to All3FlowLIOn{(i,k,l) in TRIPLES, t in T}:
    flow3_li[i,k,l,t] <= 0.07 * C[l] * all3[i,k,l,t];

subject to All3FlowLKBase{(i,k,l) in TRIPLES, t in T}:
    flow3_lk[i,k,l,t] <= 0.07 * base_week[l,t];

subject to All3FlowLKOn{(i,k,l) in TRIPLES, t in T}:
    flow3_lk[i,k,l,t] <= 0.07 * C[l] * all3[i,k,l,t];

subject to PairOnlyFlowIKBase{(i,k,l) in TRIPLES, t in T}:
    flow2_ik[i,k,l,t] <= 0.10 * base_week[i,t];

subject to PairOnlyFlowIKOn{(i,k,l) in TRIPLES, t in T}:
    flow2_ik[i,k,l,t] <= 0.10 * C[i] * only_ik[i,k,l,t];

subject to PairOnlyFlowKIBase{(i,k,l) in TRIPLES, t in T}:
    flow2_ki[i,k,l,t] <= 0.10 * base_week[k,t];

subject to PairOnlyFlowKIOn{(i,k,l) in TRIPLES, t in T}:
    flow2_ki[i,k,l,t] <= 0.10 * C[k] * only_ik[i,k,l,t];

subject to PairOnlyFlowILBase{(i,k,l) in TRIPLES, t in T}:
    flow2_il[i,k,l,t] <= 0.10 * base_week[i,t];

subject to PairOnlyFlowILOn{(i,k,l) in TRIPLES, t in T}:
    flow2_il[i,k,l,t] <= 0.10 * C[i] * only_il[i,k,l,t];

subject to PairOnlyFlowLIBase{(i,k,l) in TRIPLES, t in T}:
    flow2_li[i,k,l,t] <= 0.10 * base_week[l,t];

subject to PairOnlyFlowLIOn{(i,k,l) in TRIPLES, t in T}:
    flow2_li[i,k,l,t] <= 0.10 * C[l] * only_il[i,k,l,t];

subject to PairOnlyFlowKLBase{(i,k,l) in TRIPLES, t in T}:
    flow2_kl[i,k,l,t] <= 0.10 * base_week[k,t];

subject to PairOnlyFlowKLOn{(i,k,l) in TRIPLES, t in T}:
    flow2_kl[i,k,l,t] <= 0.10 * C[k] * only_kl[i,k,l,t];

subject to PairOnlyFlowLKBase{(i,k,l) in TRIPLES, t in T}:
    flow2_lk[i,k,l,t] <= 0.10 * base_week[l,t];

subject to PairOnlyFlowLKOn{(i,k,l) in TRIPLES, t in T}:
    flow2_lk[i,k,l,t] <= 0.10 * C[l] * only_kl[i,k,l,t];

subject to InboundLimit{i in I, t in T}:
    extra_week[i,t]
    <=
    sum {(i,k) in PAIRS} flow_pair_ki[i,k,t]
    + sum {(k,i) in PAIRS} flow_pair_ik[k,i,t]
    + sum {(i,k,l) in TRIPLES} (flow3_ki[i,k,l,t] + flow3_li[i,k,l,t] + flow2_ki[i,k,l,t] + flow2_li[i,k,l,t])
    + sum {(k,i,l) in TRIPLES} (flow3_ik[k,i,l,t] + flow3_li[k,i,l,t] + flow2_ik[k,i,l,t] + flow2_li[k,i,l,t])
    + sum {(k,l,i) in TRIPLES} (flow3_il[k,l,i,t] + flow3_kl[k,l,i,t] + flow2_il[k,l,i,t] + flow2_kl[k,l,i,t]);

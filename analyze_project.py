from __future__ import annotations

import json
from dataclasses import dataclass
from itertools import combinations, permutations
from pathlib import Path

import pulp


VENUES = ["V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10"]
SPORTS = [
    "S1",
    "S2",
    "S3",
    "S4",
    "S5",
    "S6",
    "S7",
    "S8",
    "S9",
    "S10",
    "S11",
    "S12",
    "S13",
    "S14",
    "S15",
]
WEEKS = [1, 2, 3]

VENUE_NAMES = {
    "V1": "SoFi Stadium",
    "V2": "Rose Bowl (Pasadena)",
    "V3": "Crypto.com Arena",
    "V4": "Dignity Health Sports Park",
    "V5": "UCLA Athletic Facilities",
    "V6": "USC Athletic Facilities",
    "V7": "Long Beach Arena",
    "V8": "Pomona Fairplex",
    "V9": "Inglewood Forum",
    "V10": "Dignity South (StubHub Ctr)",
}

SPORT_NAMES = {
    "S1": "Athletics (Track & Field)",
    "S2": "Swimming",
    "S3": "Gymnastics",
    "S4": "Soccer / Football",
    "S5": "Basketball",
    "S6": "Boxing",
    "S7": "Wrestling",
    "S8": "Weightlifting",
    "S9": "Tennis",
    "S10": "Volleyball",
    "S11": "Cycling (Velodrome)",
    "S12": "Archery",
    "S13": "Shooting",
    "S14": "Equestrian",
    "S15": "Sailing",
}

COST = {
    "V1": 500,
    "V2": 500,
    "V3": 400,
    "V4": 400,
    "V5": 350,
    "V6": 350,
    "V7": 300,
    "V8": 250,
    "V9": 300,
    "V10": 250,
}

CAPACITY = {
    "V1": 70,
    "V2": 90,
    "V3": 20,
    "V4": 27,
    "V5": 12,
    "V6": 10,
    "V7": 11,
    "V8": 8,
    "V9": 17,
    "V10": 8,
}

KAPPA = {
    "V1": 3,
    "V2": 3,
    "V3": 3,
    "V4": 2,
    "V5": 2,
    "V6": 2,
    "V7": 2,
    "V8": 2,
    "V9": 2,
    "V10": 2,
}

DEMAND = {
    "S1": 30,
    "S2": 15,
    "S3": 9,
    "S4": 32,
    "S5": 9,
    "S6": 8,
    "S7": 7,
    "S8": 5,
    "S9": 10,
    "S10": 12,
    "S11": 20,
    "S12": 6,
    "S13": 4,
    "S14": 8,
    "S15": 10,
}

REQUIRED_SLOTS = {
    "S1": 2,
    "S2": 1,
    "S3": 2,
    "S4": 2,
    "S5": 2,
    "S6": 1,
    "S7": 1,
    "S8": 1,
    "S9": 1,
    "S10": 1,
    "S11": 1,
    "S12": 1,
    "S13": 1,
    "S14": 1,
    "S15": 1,
}

ELIGIBLE = {
    ("V1", "S1"): 1,
    ("V1", "S2"): 0,
    ("V1", "S3"): 0,
    ("V1", "S4"): 1,
    ("V1", "S5"): 0,
    ("V1", "S6"): 0,
    ("V1", "S7"): 0,
    ("V1", "S8"): 0,
    ("V1", "S9"): 0,
    ("V1", "S10"): 0,
    ("V1", "S11"): 1,
    ("V1", "S12"): 0,
    ("V1", "S13"): 0,
    ("V1", "S14"): 0,
    ("V1", "S15"): 0,
    ("V2", "S1"): 1,
    ("V2", "S2"): 0,
    ("V2", "S3"): 0,
    ("V2", "S4"): 1,
    ("V2", "S5"): 0,
    ("V2", "S6"): 0,
    ("V2", "S7"): 0,
    ("V2", "S8"): 0,
    ("V2", "S9"): 0,
    ("V2", "S10"): 0,
    ("V2", "S11"): 1,
    ("V2", "S12"): 0,
    ("V2", "S13"): 0,
    ("V2", "S14"): 1,
    ("V2", "S15"): 0,
    ("V3", "S1"): 0,
    ("V3", "S2"): 0,
    ("V3", "S3"): 1,
    ("V3", "S4"): 0,
    ("V3", "S5"): 1,
    ("V3", "S6"): 0,
    ("V3", "S7"): 0,
    ("V3", "S8"): 0,
    ("V3", "S9"): 0,
    ("V3", "S10"): 1,
    ("V3", "S11"): 0,
    ("V3", "S12"): 0,
    ("V3", "S13"): 0,
    ("V3", "S14"): 0,
    ("V3", "S15"): 0,
    ("V4", "S1"): 0,
    ("V4", "S2"): 0,
    ("V4", "S3"): 0,
    ("V4", "S4"): 1,
    ("V4", "S5"): 1,
    ("V4", "S6"): 0,
    ("V4", "S7"): 0,
    ("V4", "S8"): 0,
    ("V4", "S9"): 1,
    ("V4", "S10"): 0,
    ("V4", "S11"): 0,
    ("V4", "S12"): 0,
    ("V4", "S13"): 0,
    ("V4", "S14"): 0,
    ("V4", "S15"): 0,
    ("V5", "S1"): 0,
    ("V5", "S2"): 1,
    ("V5", "S3"): 1,
    ("V5", "S4"): 0,
    ("V5", "S5"): 0,
    ("V5", "S6"): 0,
    ("V5", "S7"): 0,
    ("V5", "S8"): 0,
    ("V5", "S9"): 0,
    ("V5", "S10"): 1,
    ("V5", "S11"): 0,
    ("V5", "S12"): 0,
    ("V5", "S13"): 0,
    ("V5", "S14"): 0,
    ("V5", "S15"): 0,
    ("V6", "S1"): 0,
    ("V6", "S2"): 1,
    ("V6", "S3"): 0,
    ("V6", "S4"): 0,
    ("V6", "S5"): 0,
    ("V6", "S6"): 1,
    ("V6", "S7"): 1,
    ("V6", "S8"): 0,
    ("V6", "S9"): 0,
    ("V6", "S10"): 0,
    ("V6", "S11"): 0,
    ("V6", "S12"): 0,
    ("V6", "S13"): 0,
    ("V6", "S14"): 0,
    ("V6", "S15"): 0,
    ("V7", "S1"): 0,
    ("V7", "S2"): 0,
    ("V7", "S3"): 0,
    ("V7", "S4"): 0,
    ("V7", "S5"): 0,
    ("V7", "S6"): 1,
    ("V7", "S7"): 1,
    ("V7", "S8"): 0,
    ("V7", "S9"): 0,
    ("V7", "S10"): 0,
    ("V7", "S11"): 0,
    ("V7", "S12"): 0,
    ("V7", "S13"): 0,
    ("V7", "S14"): 0,
    ("V7", "S15"): 1,
    ("V8", "S1"): 0,
    ("V8", "S2"): 0,
    ("V8", "S3"): 0,
    ("V8", "S4"): 0,
    ("V8", "S5"): 0,
    ("V8", "S6"): 0,
    ("V8", "S7"): 0,
    ("V8", "S8"): 1,
    ("V8", "S9"): 0,
    ("V8", "S10"): 0,
    ("V8", "S11"): 0,
    ("V8", "S12"): 1,
    ("V8", "S13"): 1,
    ("V8", "S14"): 0,
    ("V8", "S15"): 0,
    ("V9", "S1"): 0,
    ("V9", "S2"): 0,
    ("V9", "S3"): 1,
    ("V9", "S4"): 0,
    ("V9", "S5"): 1,
    ("V9", "S6"): 1,
    ("V9", "S7"): 0,
    ("V9", "S8"): 0,
    ("V9", "S9"): 0,
    ("V9", "S10"): 1,
    ("V9", "S11"): 0,
    ("V9", "S12"): 0,
    ("V9", "S13"): 0,
    ("V9", "S14"): 0,
    ("V9", "S15"): 0,
    ("V10", "S1"): 0,
    ("V10", "S2"): 0,
    ("V10", "S3"): 0,
    ("V10", "S4"): 0,
    ("V10", "S5"): 0,
    ("V10", "S6"): 0,
    ("V10", "S7"): 1,
    ("V10", "S8"): 1,
    ("V10", "S9"): 1,
    ("V10", "S10"): 0,
    ("V10", "S11"): 0,
    ("V10", "S12"): 1,
    ("V10", "S13"): 0,
    ("V10", "S14"): 0,
    ("V10", "S15"): 0,
}

PAIR_LIST = list(combinations(VENUES, 2))
TRIPLE_LIST = list(combinations(VENUES, 3))
BUS_COST = 20
VENUE_ORDER = {venue: idx for idx, venue in enumerate(VENUES)}


@dataclass
class Scenario:
    name: str
    ticket_value: float
    demand_scale: float = 1.0


def valid_week(venue: str, week: int) -> bool:
    return week <= KAPPA[venue]


def canon_pair(a: str, b: str) -> tuple[str, str]:
    return tuple(sorted((a, b), key=lambda venue: VENUE_ORDER[venue]))


def canon_triple(a: str, b: str, c: str) -> tuple[str, str, str]:
    return tuple(sorted((a, b, c), key=lambda venue: VENUE_ORDER[venue]))


def active_expr(x_vars: dict[tuple[str, str, int], pulp.LpVariable], venue: str, week: int):
    return pulp.lpSum(x_vars[(venue, sport, week)] for sport in SPORTS if (venue, sport, week) in x_vars)


def build_task1():
    prob = pulp.LpProblem("task1", pulp.LpMinimize)
    y = pulp.LpVariable.dicts("y", VENUES, lowBound=0, upBound=1, cat="Binary")
    x = pulp.LpVariable.dicts(
        "x",
        [(venue, sport) for venue in VENUES for sport in SPORTS],
        lowBound=0,
        upBound=1,
        cat="Binary",
    )

    prob += pulp.lpSum(COST[venue] * y[venue] for venue in VENUES)

    for sport in SPORTS:
        prob += pulp.lpSum(x[(venue, sport)] for venue in VENUES) == 1

    for venue in VENUES:
        prob += pulp.lpSum(x[(venue, sport)] for sport in SPORTS) <= KAPPA[venue]
        for sport in SPORTS:
            prob += x[(venue, sport)] <= y[venue]
            prob += x[(venue, sport)] <= ELIGIBLE[(venue, sport)]

    return prob, {"y": y, "x": x}


def build_task2_or_3(name: str, ticket_value: float = 0.0, demand_scale: float = 1.0):
    prob = pulp.LpProblem(name, pulp.LpMinimize)
    x_keys = [
        (venue, sport, week)
        for venue in VENUES
        for sport in SPORTS
        for week in WEEKS
        if valid_week(venue, week)
    ]
    x = pulp.LpVariable.dicts("x", x_keys, lowBound=0, upBound=1, cat="Binary")
    z = pulp.LpVariable.dicts(
        "z",
        [(sport, week) for sport in SPORTS for week in WEEKS],
        lowBound=0,
        upBound=1,
        cat="Binary",
    )
    y = pulp.LpVariable.dicts("y", VENUES, lowBound=0, upBound=1, cat="Binary")
    base = pulp.LpVariable.dicts("base", x_keys, lowBound=0, cat="Continuous")

    prob += (
        pulp.lpSum(COST[venue] * y[venue] for venue in VENUES)
        - ticket_value * pulp.lpSum(base[key] for key in x_keys)
    )

    for sport in SPORTS:
        prob += pulp.lpSum(z[(sport, week)] for week in WEEKS) == 1
        for week in WEEKS:
            prob += (
                pulp.lpSum(x[(venue, sport, week)] for venue in VENUES if (venue, sport, week) in x)
                == REQUIRED_SLOTS[sport] * z[(sport, week)]
            )

    for venue in VENUES:
        for week in WEEKS:
            keys = [(venue, sport, week) for sport in SPORTS if (venue, sport, week) in x]
            if keys:
                prob += pulp.lpSum(x[key] for key in keys) <= 1
        for sport in SPORTS:
            for week in WEEKS:
                if (venue, sport, week) not in x:
                    continue
                prob += x[(venue, sport, week)] <= y[venue]
                prob += x[(venue, sport, week)] <= ELIGIBLE[(venue, sport)]
                prob += base[(venue, sport, week)] <= CAPACITY[venue] * x[(venue, sport, week)]
                prob += base[(venue, sport, week)] <= demand_scale * DEMAND[sport] * x[(venue, sport, week)]

    return prob, {"y": y, "x": x, "z": z, "base": base}


def add_and_constraints(prob, out_var, binaries):
    for var in binaries:
        prob += out_var <= var
    prob += out_var >= pulp.lpSum(binaries) - (len(binaries) - 1)


def build_task4_like(name: str, ticket_value: float, demand_scale: float):
    prob, vars_dict = build_task2_or_3(name, ticket_value=0.0, demand_scale=demand_scale)
    x = vars_dict["x"]
    y = vars_dict["y"]
    base = vars_dict["base"]

    pair = pulp.LpVariable.dicts("pair", PAIR_LIST, lowBound=0, upBound=1, cat="Binary")
    triple = pulp.LpVariable.dicts("triple", TRIPLE_LIST, lowBound=0, upBound=1, cat="Binary")

    pair_active = pulp.LpVariable.dicts(
        "pair_active",
        [(i, k, t) for (i, k) in PAIR_LIST for t in WEEKS],
        lowBound=0,
        upBound=1,
        cat="Binary",
    )
    all3_active = pulp.LpVariable.dicts(
        "all3_active",
        [(i, k, l, t) for (i, k, l) in TRIPLE_LIST for t in WEEKS],
        lowBound=0,
        upBound=1,
        cat="Binary",
    )
    pair_only_active = pulp.LpVariable.dicts(
        "pair_only_active",
        [(src, dst, other, t) for (src, dst, other) in permutations(VENUES, 3) if canon_triple(src, dst, other) in triple for t in WEEKS],
        lowBound=0,
        upBound=1,
        cat="Binary",
    )

    ordered_pair_flow = pulp.LpVariable.dicts(
        "pair_flow",
        [(src, dst, t) for (src, dst) in permutations(VENUES, 2) if canon_pair(src, dst) in pair for t in WEEKS],
        lowBound=0,
        cat="Continuous",
    )
    ordered_triple_all3_flow = pulp.LpVariable.dicts(
        "triple_all3_flow",
        [
            (src, dst, other, t)
            for (src, dst, other) in permutations(VENUES, 3)
            if canon_triple(src, dst, other) in triple
            for t in WEEKS
        ],
        lowBound=0,
        cat="Continuous",
    )
    ordered_triple_pair_flow = pulp.LpVariable.dicts(
        "triple_pair_flow",
        [
            (src, dst, other, t)
            for (src, dst, other) in permutations(VENUES, 3)
            if canon_triple(src, dst, other) in triple
            for t in WEEKS
        ],
        lowBound=0,
        cat="Continuous",
    )
    extra = pulp.LpVariable.dicts(
        "extra",
        list(x.keys()),
        lowBound=0,
        cat="Continuous",
    )

    prob.setObjective(
        pulp.lpSum(COST[venue] * y[venue] for venue in VENUES)
        + BUS_COST * pulp.lpSum(pair[p] for p in PAIR_LIST)
        + BUS_COST * pulp.lpSum(triple[g] for g in TRIPLE_LIST)
        - ticket_value * pulp.lpSum(base[key] + extra[key] for key in x)
    )

    for venue in VENUES:
        prob += (
            pulp.lpSum(pair[p] for p in PAIR_LIST if venue in p)
            + pulp.lpSum(triple[g] for g in TRIPLE_LIST if venue in g)
            <= 1
        )

    for (i, k) in PAIR_LIST:
        for t in WEEKS:
            ui = active_expr(x, i, t)
            uk = active_expr(x, k, t)
            add_and_constraints(prob, pair_active[(i, k, t)], [pair[(i, k)], ui, uk])

    for (i, k, l) in TRIPLE_LIST:
        for t in WEEKS:
            ui = active_expr(x, i, t)
            uk = active_expr(x, k, t)
            ul = active_expr(x, l, t)
            add_and_constraints(prob, all3_active[(i, k, l, t)], [triple[(i, k, l)], ui, uk, ul])

            for src, dst, other in (
                (i, k, l),
                (k, i, l),
                (i, l, k),
                (l, i, k),
                (k, l, i),
                (l, k, i),
            ):
                out = pair_only_active[(src, dst, other, t)]
                prob += out <= triple[(i, k, l)]
                prob += out <= active_expr(x, src, t)
                prob += out <= active_expr(x, dst, t)
                prob += out <= 1 - active_expr(x, other, t)
                prob += out >= (
                    triple[(i, k, l)]
                    + active_expr(x, src, t)
                    + active_expr(x, dst, t)
                    - active_expr(x, other, t)
                    - 2
                )

    for (src, dst) in permutations(VENUES, 2):
        pair_key = canon_pair(src, dst)
        if pair_key not in pair:
            continue
        for t in WEEKS:
            flow = ordered_pair_flow[(src, dst, t)]
            prob += flow <= 0.10 * pulp.lpSum(base[(src, sport, t)] for sport in SPORTS if (src, sport, t) in base)
            prob += flow <= 0.10 * CAPACITY[src] * pair_active[(pair_key[0], pair_key[1], t)]

    for (src, dst, other) in permutations(VENUES, 3):
        triple_key = canon_triple(src, dst, other)
        if triple_key not in triple:
            continue
        for t in WEEKS:
            flow_all3 = ordered_triple_all3_flow[(src, dst, other, t)]
            flow_pair = ordered_triple_pair_flow[(src, dst, other, t)]
            prob += flow_all3 <= 0.07 * pulp.lpSum(base[(src, sport, t)] for sport in SPORTS if (src, sport, t) in base)
            prob += flow_all3 <= 0.07 * CAPACITY[src] * all3_active[(triple_key[0], triple_key[1], triple_key[2], t)]

            prob += flow_pair <= 0.10 * pulp.lpSum(base[(src, sport, t)] for sport in SPORTS if (src, sport, t) in base)
            prob += flow_pair <= 0.10 * CAPACITY[src] * pair_only_active[(src, dst, other, t)]

    for venue in VENUES:
        for week in WEEKS:
            inbound = []
            for other in VENUES:
                if other == venue:
                    continue
                pair_key = canon_pair(venue, other)
                if pair_key in pair:
                    inbound.append(ordered_pair_flow[(other, venue, week)])

            for src, other in permutations([v for v in VENUES if v != venue], 2):
                triple_key = canon_triple(src, venue, other)
                if triple_key in triple:
                    inbound.append(ordered_triple_all3_flow[(src, venue, other, week)])
                    inbound.append(ordered_triple_pair_flow[(src, venue, other, week)])

            base_keys = [(venue, sport, week) for sport in SPORTS if (venue, sport, week) in base]
            if not base_keys:
                continue

            prob += pulp.lpSum(base[key] + extra[key] for key in base_keys) <= CAPACITY[venue] * active_expr(x, venue, week)
            prob += pulp.lpSum(extra[key] for key in base_keys) <= pulp.lpSum(inbound)

    vars_dict.update(
        {
            "pair": pair,
            "triple": triple,
            "extra": extra,
            "pair_active": pair_active,
            "all3_active": all3_active,
            "pair_only_active": pair_only_active,
            "ordered_pair_flow": ordered_pair_flow,
            "ordered_triple_all3_flow": ordered_triple_all3_flow,
            "ordered_triple_pair_flow": ordered_triple_pair_flow,
        }
    )
    return prob, vars_dict


def solve(prob: pulp.LpProblem):
    status = prob.solve(pulp.HiGHS(msg=False))
    label = pulp.LpStatus[status]
    if label != "Optimal":
        raise RuntimeError(f"Solver status {label}")


def summarize_task1(prob: pulp.LpProblem, vars_dict):
    y = vars_dict["y"]
    x = vars_dict["x"]
    opened = [venue for venue in VENUES if y[venue].value() > 0.5]
    assignments = {sport: next(venue for venue in VENUES if x[(venue, sport)].value() > 0.5) for sport in SPORTS}
    return {
        "objective": pulp.value(prob.objective),
        "opened_venues": opened,
        "assignments": assignments,
    }


def summarize_schedule(prob: pulp.LpProblem, vars_dict, include_buses: bool = False):
    y = vars_dict["y"]
    x = vars_dict["x"]
    z = vars_dict["z"]
    base = vars_dict["base"]
    extra = vars_dict.get("extra")

    opened = [venue for venue in VENUES if y[venue].value() > 0.5]
    schedule = []
    tickets_by_sport = {sport: 0.0 for sport in SPORTS}
    total_base = 0.0
    total_extra = 0.0

    for sport in SPORTS:
        assigned_week = next(week for week in WEEKS if z[(sport, week)].value() > 0.5)
        sport_rows = []
        for venue in VENUES:
            key = (venue, sport, assigned_week)
            if key in x and x[key].value() > 0.5:
                base_val = base[key].value()
                extra_val = extra[key].value() if extra else 0.0
                total_base += base_val
                total_extra += extra_val
                tickets_by_sport[sport] += base_val + extra_val
                sport_rows.append(
                    {
                        "venue": venue,
                        "venue_name": VENUE_NAMES[venue],
                        "week": assigned_week,
                        "base_tickets": round(base_val, 4),
                        "extra_tickets": round(extra_val, 4),
                        "total_tickets": round(base_val + extra_val, 4),
                    }
                )
        schedule.append(
            {
                "sport": sport,
                "sport_name": SPORT_NAMES[sport],
                "week": assigned_week,
                "slots": sport_rows,
                "total_tickets": round(tickets_by_sport[sport], 4),
            }
        )

    result = {
        "objective": pulp.value(prob.objective),
        "opened_venues": opened,
        "schedule": schedule,
        "tickets": {
            "base_total": round(total_base, 4),
            "extra_total": round(total_extra, 4),
            "grand_total": round(total_base + total_extra, 4),
            "by_sport": {sport: round(value, 4) for sport, value in tickets_by_sport.items()},
        },
    }

    if include_buses:
        pair = vars_dict["pair"]
        triple = vars_dict["triple"]
        result["bus_networks"] = {
            "pairs": [list(p) for p in PAIR_LIST if pair[p].value() > 0.5],
            "triples": [list(g) for g in TRIPLE_LIST if triple[g].value() > 0.5],
        }

    return result


SEARCH_SEEDS = [
    (set(), set()),
    (set(), {("V1", "V2", "V3")}),
    (set(), {("V1", "V2", "V3"), ("V5", "V7", "V9")}),
    (set(), {("V1", "V2", "V3"), ("V7", "V8", "V9")}),
    ({("V5", "V8")}, {("V1", "V2", "V3"), ("V7", "V9", "V10")}),
]


def select_best_networks(summary: dict, ticket_value: float):
    base = {
        (slot["venue"], slot["week"]): slot["base_tickets"]
        for row in summary["schedule"]
        for slot in row["slots"]
    }
    total = {
        (slot["venue"], slot["week"]): slot["total_tickets"]
        for row in summary["schedule"]
        for slot in row["slots"]
    }
    residual = {(venue, week): CAPACITY[venue] - total[(venue, week)] for (venue, week) in total}
    items = []

    for pair_key in PAIR_LIST:
        i, k = pair_key
        added = 0.0
        for week in WEEKS:
            if (i, week) in base and (k, week) in base:
                added += min(0.10 * base[(i, week)], residual[(k, week)])
                added += min(0.10 * base[(k, week)], residual[(i, week)])
        value = ticket_value * added - BUS_COST
        if value > 1e-9:
            items.append((frozenset(pair_key), ("pair", pair_key), value))

    for triple_key in TRIPLE_LIST:
        i, k, l = triple_key
        added = 0.0
        for week in WEEKS:
            active = [venue for venue in triple_key if (venue, week) in base]
            if len(active) == 2:
                a, b = active
                added += min(0.10 * base[(a, week)], residual[(b, week)])
                added += min(0.10 * base[(b, week)], residual[(a, week)])
            elif len(active) == 3:
                for target, src1, src2 in ((i, k, l), (k, i, l), (l, i, k)):
                    added += min(
                        0.07 * base[(src1, week)] + 0.07 * base[(src2, week)],
                        residual[(target, week)],
                    )
        value = ticket_value * added - BUS_COST
        if value > 1e-9:
            items.append((frozenset(triple_key), ("triple", triple_key), value))

    memo: dict[tuple[str, ...], tuple[float, list[tuple[str, tuple[str, ...]]]]] = {}

    def best_for(remaining_tuple: tuple[str, ...]):
        if remaining_tuple in memo:
            return memo[remaining_tuple]

        remaining = set(remaining_tuple)
        best_value = 0.0
        best_choice: list[tuple[str, tuple[str, ...]]] = []
        for venue_set, description, value in items:
            if venue_set <= remaining:
                next_tuple = tuple(venue for venue in VENUES if venue in remaining - venue_set)
                sub_value, sub_choice = best_for(next_tuple)
                candidate_value = value + sub_value
                if candidate_value > best_value:
                    best_value = candidate_value
                    best_choice = [description] + sub_choice

        memo[remaining_tuple] = (best_value, best_choice)
        return memo[remaining_tuple]

    _, chosen = best_for(tuple(VENUES))
    pair_set = {entry for kind, entry in chosen if kind == "pair"}
    triple_set = {entry for kind, entry in chosen if kind == "triple"}
    return pair_set, triple_set


def solve_fixed_network_scenario(ticket_value: float, demand_scale: float, pair_set, triple_set):
    prob, vars_dict = build_task4_like("fixed_networks", ticket_value=ticket_value, demand_scale=demand_scale)
    for pair_key in PAIR_LIST:
        prob += vars_dict["pair"][pair_key] == (1 if pair_key in pair_set else 0)
    for triple_key in TRIPLE_LIST:
        prob += vars_dict["triple"][triple_key] == (1 if triple_key in triple_set else 0)
    solve(prob)
    return prob, vars_dict


def solve_scenario_with_seed_search(scenario: Scenario):
    best_summary = None
    best_signature = None

    for seed_pairs, seed_triples in SEARCH_SEEDS:
        pair_set = set(seed_pairs)
        triple_set = set(seed_triples)
        seen = set()

        for _ in range(5):
            state = (tuple(sorted(pair_set)), tuple(sorted(triple_set)))
            if state in seen:
                break
            seen.add(state)

            prob, vars_dict = solve_fixed_network_scenario(
                scenario.ticket_value,
                scenario.demand_scale,
                pair_set,
                triple_set,
            )
            summary = summarize_schedule(prob, vars_dict, include_buses=True)
            pair_set, triple_set = select_best_networks(summary, scenario.ticket_value)

        prob, vars_dict = solve_fixed_network_scenario(
            scenario.ticket_value,
            scenario.demand_scale,
            pair_set,
            triple_set,
        )
        summary = summarize_schedule(prob, vars_dict, include_buses=True)
        signature = extract_solution_signature(vars_dict)

        if best_summary is None or summary["objective"] < best_summary["objective"]:
            best_summary = summary
            best_signature = signature

    return best_summary, best_signature


def solve_all():
    outputs: dict[str, dict] = {}

    task1_prob, task1_vars = build_task1()
    solve(task1_prob)
    outputs["task1"] = summarize_task1(task1_prob, task1_vars)

    task2_prob, task2_vars = build_task2_or_3("task2", ticket_value=0.0)
    solve(task2_prob)
    outputs["task2"] = summarize_schedule(task2_prob, task2_vars)

    task3_prob, task3_vars = build_task2_or_3("task3", ticket_value=10.0)
    solve(task3_prob)
    outputs["task3"] = summarize_schedule(task3_prob, task3_vars)

    scenarios = [
        Scenario(name="task4_base", ticket_value=10.0, demand_scale=1.0),
        Scenario(name="ticket_5", ticket_value=5.0, demand_scale=1.0),
        Scenario(name="ticket_15", ticket_value=15.0, demand_scale=1.0),
        Scenario(name="demand_minus_10pct", ticket_value=10.0, demand_scale=0.9),
    ]

    scenario_outputs = {}
    raw_solutions = {}

    for scenario in scenarios:
        summary, signature = solve_scenario_with_seed_search(scenario)
        scenario_outputs[scenario.name] = summary
        raw_solutions[scenario.name] = signature

    outputs["task4"] = scenario_outputs["task4_base"]

    cross_evaluation = {}
    for scenario in scenarios:
        cross_evaluation[scenario.name] = {}
        for applied_name, signature in raw_solutions.items():
            cross_evaluation[scenario.name][applied_name] = round(
                evaluate_solution(signature, scenario.ticket_value, scenario.demand_scale),
                4,
            )

    outputs["task5"] = {
        "scenario_results": scenario_outputs,
        "cross_evaluation_costs": cross_evaluation,
    }

    return outputs


def extract_solution_signature(vars_dict):
    x = vars_dict["x"]
    pair = vars_dict.get("pair")
    triple = vars_dict.get("triple")

    schedule = [(venue, sport, week) for (venue, sport, week), var in x.items() if var.value() > 0.5]
    pairs = [p for p in PAIR_LIST if pair and pair[p].value() > 0.5]
    triples = [g for g in TRIPLE_LIST if triple and triple[g].value() > 0.5]
    return {"schedule": schedule, "pairs": pairs, "triples": triples}


def evaluate_solution(signature, ticket_value: float, demand_scale: float):
    prob = pulp.LpProblem("evaluation", pulp.LpMinimize)
    x = {
        key: pulp.LpVariable(f"x_{key[0]}_{key[1]}_{key[2]}", lowBound=1, upBound=1, cat="Binary")
        for key in signature["schedule"]
    }
    base = {key: pulp.LpVariable(f"base_{key[0]}_{key[1]}_{key[2]}", lowBound=0) for key in signature["schedule"]}
    extra = {key: pulp.LpVariable(f"extra_{key[0]}_{key[1]}_{key[2]}", lowBound=0) for key in signature["schedule"]}

    pair_active = {}
    all3_active = {}
    pair_only_active = {}
    pair_flow = {}
    triple_all3_flow = {}
    triple_pair_flow = {}

    fixed_cost = sum(COST[venue] for venue in {venue for venue, _, _ in signature["schedule"]})
    bus_cost = BUS_COST * (len(signature["pairs"]) + len(signature["triples"]))

    prob += fixed_cost + bus_cost - ticket_value * pulp.lpSum(base.values()) - ticket_value * pulp.lpSum(extra.values())

    for key in signature["schedule"]:
        venue, sport, _ = key
        prob += base[key] <= CAPACITY[venue]
        prob += base[key] <= demand_scale * DEMAND[sport]

    schedule_lookup = {(venue, week): sport for venue, sport, week in signature["schedule"]}

    for (i, k) in signature["pairs"]:
        for t in WEEKS:
            pair_active[(i, k, t)] = 1 if (i, t) in schedule_lookup and (k, t) in schedule_lookup else 0
            for src, dst in ((i, k), (k, i)):
                var = pulp.LpVariable(f"pair_flow_{src}_{dst}_{t}", lowBound=0)
                pair_flow[(src, dst, t)] = var
                base_src = base[(src, schedule_lookup[(src, t)], t)] if (src, t) in schedule_lookup else 0
                prob += var <= 0.10 * base_src
                prob += var <= 0.10 * CAPACITY[src] * pair_active[(i, k, t)]

    for (i, k, l) in signature["triples"]:
        for t in WEEKS:
            active = {venue: int((venue, t) in schedule_lookup) for venue in (i, k, l)}
            all3_active[(i, k, l, t)] = 1 if sum(active.values()) == 3 else 0

            for src, dst, other in (
                (i, k, l),
                (k, i, l),
                (i, l, k),
                (l, i, k),
                (k, l, i),
                (l, k, i),
            ):
                pair_only_active[(src, dst, other, t)] = 1 if active[src] and active[dst] and not active[other] else 0
                var_all3 = pulp.LpVariable(f"all3_flow_{src}_{dst}_{other}_{t}", lowBound=0)
                var_pair = pulp.LpVariable(f"paironly_flow_{src}_{dst}_{other}_{t}", lowBound=0)
                triple_all3_flow[(src, dst, other, t)] = var_all3
                triple_pair_flow[(src, dst, other, t)] = var_pair

                if active[src]:
                    base_src = base[(src, schedule_lookup[(src, t)], t)]
                else:
                    base_src = 0

                prob += var_all3 <= 0.07 * base_src
                prob += var_all3 <= 0.07 * CAPACITY[src] * all3_active[(i, k, l, t)]

                prob += var_pair <= 0.10 * base_src
                prob += var_pair <= 0.10 * CAPACITY[src] * pair_only_active[(src, dst, other, t)]

    for (venue, week), sport in schedule_lookup.items():
        inbound = []
        for other in VENUES:
            if other == venue:
                continue
            if (other, venue, week) in pair_flow:
                inbound.append(pair_flow[(other, venue, week)])
        for src, other in permutations([v for v in VENUES if v != venue], 2):
            if (src, venue, other, week) in triple_all3_flow:
                inbound.append(triple_all3_flow[(src, venue, other, week)])
            if (src, venue, other, week) in triple_pair_flow:
                inbound.append(triple_pair_flow[(src, venue, other, week)])

        key = (venue, sport, week)
        prob += base[key] + extra[key] <= CAPACITY[venue]
        prob += extra[key] <= pulp.lpSum(inbound)

    solve(prob)
    return pulp.value(prob.objective)


def main():
    outputs = solve_all()
    out_path = Path(__file__).with_name("results.json")
    out_path.write_text(json.dumps(outputs, indent=2))
    print(json.dumps(outputs, indent=2))


if __name__ == "__main__":
    main()

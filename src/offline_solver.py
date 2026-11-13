r"""
Offline solvers for maximum-weight b-matching and fairness-penalized MILP.
1. SciPy HiGHS MILP formulation for general \mu >= 0.
2. NetworkX Min-Cost Max-Flow solver for polynomial time \mu = 0 case.
"""

import time
from typing import List, Tuple, Dict
import numpy as np
import scipy.optimize as opt
import scipy.sparse as sp
import networkx as nx
from .models import ProblemInstance, AssignmentResult, Volunteer, Request
from .metrics import compute_jains_index


class OfflineSolver:
    """Exact offline solvers knowing all requests in advance."""

    @staticmethod
    def solve_milp(instance: ProblemInstance) -> AssignmentResult:
        r"""
        Solves the exact offline integer linear program via HiGHS:
        max \sum_{(v,r) \in E} w_{vr} * x_{vr} - \mu * L
        s.t.
          \sum_{v} x_{vr} <= 1          \forall r \in R
          \sum_{r} x_{vr} <= \kappa_v   \forall v \in V
          \sum_{r} x_{vr} <= L          \forall v \in V
          x_{vr} \in {0, 1}, L >= 0
        """
        t_start = time.perf_counter()
        instance.reset_volunteers()

        # Extract eligible edges
        edges = instance.get_eligible_edges()
        if not edges:
            return AssignmentResult(
                algorithm_name="Offline-MILP",
                matched_pairs=[],
                rejected_requests=[r.id for r in instance.requests],
                total_utility=0.0,
                total_travel_time=0.0,
                net_objective=0.0,
                max_load=0,
                volunteer_loads={v.id: 0 for v in instance.volunteers},
                jains_fairness_index=1.0,
                execution_time_seconds=time.perf_counter() - t_start
            )

        num_edges = len(edges)
        # Decision variables: z = [x_0, x_1, ..., x_{m-1}, L]
        # Length: num_edges + 1
        num_vars = num_edges + 1

        # Objective vector: minimize -sum(w_e * x_e) + mu * L
        c = np.zeros(num_vars, dtype=float)
        for i, (_, _, w) in enumerate(edges):
            c[i] = -w
        c[num_edges] = instance.mu_fairness

        # Integrality: 1 for binary edges, 0 for continuous L
        integrality = np.zeros(num_vars, dtype=int)
        integrality[:num_edges] = 1  # Binary {0, 1}

        # Variable bounds: x_e \in [0, 1], L \in [0, \infty)
        lb = np.zeros(num_vars, dtype=float)
        ub = np.ones(num_vars, dtype=float)
        ub[num_edges] = np.inf
        bounds = opt.Bounds(lb, ub)

        # Build constraints
        # Row groups:
        # 1. Request matching: for each r, sum_{v} x_{vr} <= 1
        # 2. Volunteer capacity: for each v, sum_{r} x_{vr} <= \kappa_v
        # 3. Max load definition: for each v, sum_{r} x_{vr} - L <= 0
        rows = []
        cols = []
        data = []
        row_ub = []

        curr_row = 0
        # Map r_id -> list of edge indices
        r_to_edges: Dict[int, List[int]] = {}
        # Map v_id -> list of edge indices
        v_to_edges: Dict[int, List[int]] = {}

        for edge_idx, (v_id, r_id, _) in enumerate(edges):
            r_to_edges.setdefault(r_id, []).append(edge_idx)
            v_to_edges.setdefault(v_id, []).append(edge_idx)

        # 1. Request constraints
        for r in instance.requests:
            if r.id in r_to_edges:
                for edge_idx in r_to_edges[r.id]:
                    rows.append(curr_row)
                    cols.append(edge_idx)
                    data.append(1.0)
                row_ub.append(1.0)
                curr_row += 1

        # 2. Capacity constraints
        for v in instance.volunteers:
            if v.id in v_to_edges:
                for edge_idx in v_to_edges[v.id]:
                    rows.append(curr_row)
                    cols.append(edge_idx)
                    data.append(1.0)
                row_ub.append(float(v.capacity))
                curr_row += 1

        # 3. Max load constraints (sum x_{vr} - L <= 0)
        for v in instance.volunteers:
            if v.id in v_to_edges:
                for edge_idx in v_to_edges[v.id]:
                    rows.append(curr_row)
                    cols.append(edge_idx)
                    data.append(1.0)
                # -1.0 on L
                rows.append(curr_row)
                cols.append(num_edges)
                data.append(-1.0)
                row_ub.append(0.0)
                curr_row += 1

        num_constraints = curr_row
        A = sp.csr_matrix((data, (rows, cols)), shape=(num_constraints, num_vars))
        b_u = np.array(row_ub, dtype=float)
        b_l = np.full(num_constraints, -np.inf, dtype=float)

        constraints = opt.LinearConstraint(A, b_l, b_u)

        # Solve with HiGHS
        res = opt.milp(c=c, integrality=integrality, bounds=bounds, constraints=constraints)

        if not res.success:
            raise RuntimeError(f"MILP solver failed: {res.status} - {res.message}")

        matched_pairs: List[Tuple[int, int]] = []
        volunteer_loads = {v.id: 0 for v in instance.volunteers}
        total_utility = 0.0
        total_travel_time = 0.0

        for edge_idx, (v_id, r_id, _) in enumerate(edges):
            if res.x[edge_idx] > 0.5:
                matched_pairs.append((v_id, r_id))
                volunteer_loads[v_id] += 1
                total_utility += instance.r_map[r_id].utility
                total_travel_time += instance.compute_travel_time(v_id, r_id)

        matched_r_ids = {r_id for _, r_id in matched_pairs}
        rejected = [r.id for r in instance.requests if r.id not in matched_r_ids]
        max_load = max(volunteer_loads.values()) if volunteer_loads else 0
        net_obj = (total_utility - instance.lambda_cost * total_travel_time) - (instance.mu_fairness * max_load)

        return AssignmentResult(
            algorithm_name="Offline-MILP",
            matched_pairs=matched_pairs,
            rejected_requests=rejected,
            total_utility=round(total_utility, 2),
            total_travel_time=round(total_travel_time, 2),
            net_objective=round(net_obj, 2),
            max_load=max_load,
            volunteer_loads=volunteer_loads,
            jains_fairness_index=round(compute_jains_index(list(volunteer_loads.values())), 4),
            execution_time_seconds=round(time.perf_counter() - t_start, 4)
        )

    @staticmethod
    def solve_flow(instance: ProblemInstance) -> AssignmentResult:
        r"""
        Solves offline maximum-weight b-matching via Min-Cost Flow in polynomial time (when \mu = 0).
        Reduces maximum-weight b-matching to min-cost flow on a directed graph:
          Source S -> Volunteers v (capacity \kappa_v, cost 0)
          Volunteer v -> Request r (capacity 1, cost -int(1000 * w_vr))
          Request r -> Sink T (capacity 1, cost 0)
        """
        t_start = time.perf_counter()
        instance.reset_volunteers()

        edges = instance.get_eligible_edges()
        if not edges:
            return AssignmentResult(
                algorithm_name="Offline-Flow",
                matched_pairs=[],
                rejected_requests=[r.id for r in instance.requests],
                total_utility=0.0,
                total_travel_time=0.0,
                net_objective=0.0,
                max_load=0,
                volunteer_loads={v.id: 0 for v in instance.volunteers},
                jains_fairness_index=1.0,
                execution_time_seconds=time.perf_counter() - t_start
            )

        G = nx.DiGraph()
        SOURCE = "source"
        SINK = "sink"

        # Add nodes
        G.add_node(SOURCE)
        G.add_node(SINK)

        SCALE = 10000  # Scaling factor to integer costs for NetworkX

        for v in instance.volunteers:
            v_node = f"v_{v.id}"
            G.add_edge(SOURCE, v_node, capacity=v.capacity, weight=0)

        for r in instance.requests:
            r_node = f"r_{r.id}"
            # Can match at most once, or skip to sink at cost 0 (dummy edge to allow partial matching)
            G.add_edge(r_node, SINK, capacity=1, weight=0)

        for v_id, r_id, w in edges:
            v_node = f"v_{v_id}"
            r_node = f"r_{r_id}"
            # Negative cost to maximize weight
            G.add_edge(v_node, r_node, capacity=1, weight=-int(round(w * SCALE)))

        # Also allow excess volunteer capacity to bypass to sink at cost 0
        for v in instance.volunteers:
            v_node = f"v_{v.id}"
            G.add_edge(v_node, SINK, capacity=v.capacity, weight=0)

        total_cap = sum(v.capacity for v in instance.volunteers)
        G.nodes[SOURCE]["demand"] = -total_cap
        G.nodes[SINK]["demand"] = total_cap

        flow_dict = nx.min_cost_flow(G)

        matched_pairs: List[Tuple[int, int]] = []
        volunteer_loads = {v.id: 0 for v in instance.volunteers}
        total_utility = 0.0
        total_travel_time = 0.0

        for v in instance.volunteers:
            v_node = f"v_{v.id}"
            for r in instance.requests:
                r_node = f"r_{r.id}"
                if r_node in flow_dict[v_node] and flow_dict[v_node][r_node] > 0.5:
                    matched_pairs.append((v.id, r.id))
                    volunteer_loads[v.id] += 1
                    total_utility += r.utility
                    total_travel_time += instance.compute_travel_time(v.id, r.id)

        matched_r_ids = {r_id for _, r_id in matched_pairs}
        rejected = [r.id for r in instance.requests if r.id not in matched_r_ids]
        max_load = max(volunteer_loads.values()) if volunteer_loads else 0
        net_obj = total_utility - instance.lambda_cost * total_travel_time

        return AssignmentResult(
            algorithm_name="Offline-Flow",
            matched_pairs=matched_pairs,
            rejected_requests=rejected,
            total_utility=round(total_utility, 2),
            total_travel_time=round(total_travel_time, 2),
            net_objective=round(net_obj, 2),
            max_load=max_load,
            volunteer_loads=volunteer_loads,
            jains_fairness_index=round(compute_jains_index(list(volunteer_loads.values())), 4),
            execution_time_seconds=round(time.perf_counter() - t_start, 4)
        )

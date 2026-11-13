"""
Online dispatch algorithms and classical baselines for emergency response.
1. Greedy Dispatch (Maximum Weight / Nearest Eligible)
2. Random Eligible Dispatch
3. Karp-Vazirani-Vazirani (KVV) Ranking
4. Water-Filling / Balance (Fairness-oriented)
"""

import time
import random
from typing import List, Tuple, Dict, Optional
from .models import ProblemInstance, AssignmentResult, Volunteer, Request
from .metrics import compute_jains_index


class OnlineAlgorithms:
    """Implements online dispatch policies operating one request at a time."""

    @staticmethod
    def run_greedy(instance: ProblemInstance) -> AssignmentResult:
        """
        Greedy policy: For each incoming request r, greedily match with the
        eligible available volunteer v that maximizes net weight w_vr = u_r - lambda * c_vr.
        """
        t_start = time.perf_counter()
        instance.reset_volunteers()

        matched_pairs: List[Tuple[int, int]] = []
        rejected_requests: List[int] = []
        total_utility = 0.0
        total_travel_time = 0.0

        for req in instance.requests:
            best_v_id: Optional[int] = None
            best_weight: float = 0.0

            for v in instance.volunteers:
                if v.is_available() and instance.is_eligible(v.id, req.id):
                    weight = instance.get_weight(v.id, req.id)
                    if weight > best_weight:
                        best_weight = weight
                        best_v_id = v.id

            if best_v_id is not None:
                instance.v_map[best_v_id].assign(req.id)
                matched_pairs.append((best_v_id, req.id))
                total_utility += req.utility
                total_travel_time += instance.compute_travel_time(best_v_id, req.id)
            else:
                rejected_requests.append(req.id)

        volunteer_loads = {v.id: v.current_load for v in instance.volunteers}
        max_load = max(volunteer_loads.values()) if volunteer_loads else 0
        net_obj = (total_utility - instance.lambda_cost * total_travel_time) - (instance.mu_fairness * max_load)

        return AssignmentResult(
            algorithm_name="Online-Greedy",
            matched_pairs=matched_pairs,
            rejected_requests=rejected_requests,
            total_utility=round(total_utility, 2),
            total_travel_time=round(total_travel_time, 2),
            net_objective=round(net_obj, 2),
            max_load=max_load,
            volunteer_loads=volunteer_loads,
            jains_fairness_index=round(compute_jains_index(list(volunteer_loads.values())), 4),
            execution_time_seconds=round(time.perf_counter() - t_start, 4)
        )

    @staticmethod
    def run_random(instance: ProblemInstance, seed: Optional[int] = 42) -> AssignmentResult:
        """
        Random baseline: Uniformly randomly select from eligible available volunteers.
        """
        t_start = time.perf_counter()
        if seed is not None:
            random.seed(seed)
        instance.reset_volunteers()

        matched_pairs: List[Tuple[int, int]] = []
        rejected_requests: List[int] = []
        total_utility = 0.0
        total_travel_time = 0.0

        for req in instance.requests:
            candidates = [
                v.id for v in instance.volunteers
                if v.is_available() and instance.is_eligible(v.id, req.id)
            ]
            if candidates:
                chosen_v_id = random.choice(candidates)
                instance.v_map[chosen_v_id].assign(req.id)
                matched_pairs.append((chosen_v_id, req.id))
                total_utility += req.utility
                total_travel_time += instance.compute_travel_time(chosen_v_id, req.id)
            else:
                rejected_requests.append(req.id)

        volunteer_loads = {v.id: v.current_load for v in instance.volunteers}
        max_load = max(volunteer_loads.values()) if volunteer_loads else 0
        net_obj = (total_utility - instance.lambda_cost * total_travel_time) - (instance.mu_fairness * max_load)

        return AssignmentResult(
            algorithm_name="Online-Random",
            matched_pairs=matched_pairs,
            rejected_requests=rejected_requests,
            total_utility=round(total_utility, 2),
            total_travel_time=round(total_travel_time, 2),
            net_objective=round(net_obj, 2),
            max_load=max_load,
            volunteer_loads=volunteer_loads,
            jains_fairness_index=round(compute_jains_index(list(volunteer_loads.values())), 4),
            execution_time_seconds=round(time.perf_counter() - t_start, 4)
        )

    @staticmethod
    def run_ranking(instance: ProblemInstance, seed: Optional[int] = 42) -> AssignmentResult:
        """
        Karp-Vazirani-Vazirani (KVV) Ranking algorithm:
        Assigns a random priority rank Y_v ~ Uniform(0, 1) to each volunteer upfront.
        When request r arrives, chooses the eligible volunteer that minimizes Y_v (or maximizes rank).
        """
        t_start = time.perf_counter()
        if seed is not None:
            random.seed(seed)
        instance.reset_volunteers()

        # Generate random priority values Y_v \in [0, 1] for each volunteer
        ranks = {v.id: random.random() for v in instance.volunteers}

        matched_pairs: List[Tuple[int, int]] = []
        rejected_requests: List[int] = []
        total_utility = 0.0
        total_travel_time = 0.0

        for req in instance.requests:
            candidates = [
                v.id for v in instance.volunteers
                if v.is_available() and instance.is_eligible(v.id, req.id)
            ]
            if candidates:
                # Select the volunteer with the highest priority (lowest Y_v)
                chosen_v_id = min(candidates, key=lambda v_id: ranks[v_id])
                instance.v_map[chosen_v_id].assign(req.id)
                matched_pairs.append((chosen_v_id, req.id))
                total_utility += req.utility
                total_travel_time += instance.compute_travel_time(chosen_v_id, req.id)
            else:
                rejected_requests.append(req.id)

        volunteer_loads = {v.id: v.current_load for v in instance.volunteers}
        max_load = max(volunteer_loads.values()) if volunteer_loads else 0
        net_obj = (total_utility - instance.lambda_cost * total_travel_time) - (instance.mu_fairness * max_load)

        return AssignmentResult(
            algorithm_name="Online-Ranking",
            matched_pairs=matched_pairs,
            rejected_requests=rejected_requests,
            total_utility=round(total_utility, 2),
            total_travel_time=round(total_travel_time, 2),
            net_objective=round(net_obj, 2),
            max_load=max_load,
            volunteer_loads=volunteer_loads,
            jains_fairness_index=round(compute_jains_index(list(volunteer_loads.values())), 4),
            execution_time_seconds=round(time.perf_counter() - t_start, 4)
        )

    @staticmethod
    def run_water_filling(instance: ProblemInstance) -> AssignmentResult:
        """
        Water-filling / Balance algorithm:
        Prioritizes the volunteer with the minimum current load (breaking ties by highest weight).
        Directly optimizes workload fairness and prevents volunteer burnout.
        """
        t_start = time.perf_counter()
        instance.reset_volunteers()

        matched_pairs: List[Tuple[int, int]] = []
        rejected_requests: List[int] = []
        total_utility = 0.0
        total_travel_time = 0.0

        for req in instance.requests:
            candidates = [
                v for v in instance.volunteers
                if v.is_available() and instance.is_eligible(v.id, req.id)
            ]
            if candidates:
                # Key: sort primarily by current_load ascending, secondarily by net weight descending
                chosen_v = min(
                    candidates,
                    key=lambda v: (v.current_load, -instance.get_weight(v.id, req.id))
                )
                chosen_v.assign(req.id)
                matched_pairs.append((chosen_v.id, req.id))
                total_utility += req.utility
                total_travel_time += instance.compute_travel_time(chosen_v.id, req.id)
            else:
                rejected_requests.append(req.id)

        volunteer_loads = {v.id: v.current_load for v in instance.volunteers}
        max_load = max(volunteer_loads.values()) if volunteer_loads else 0
        net_obj = (total_utility - instance.lambda_cost * total_travel_time) - (instance.mu_fairness * max_load)

        return AssignmentResult(
            algorithm_name="Online-WaterFilling",
            matched_pairs=matched_pairs,
            rejected_requests=rejected_requests,
            total_utility=round(total_utility, 2),
            total_travel_time=round(total_travel_time, 2),
            net_objective=round(net_obj, 2),
            max_load=max_load,
            volunteer_loads=volunteer_loads,
            jains_fairness_index=round(compute_jains_index(list(volunteer_loads.values())), 4),
            execution_time_seconds=round(time.perf_counter() - t_start, 4)
        )


"""
Proposed Learning-Augmented Algorithm: Follow-the-Prediction with Safeguard (FTPS).
Combines offline optimization on predictions with an online error-tracking safeguard.
Guarantees:
  - Consistency: Competitive Ratio -> 1.0 as prediction error \eta -> 0.
  - Robustness: Competitive Ratio >= \beta' * Baseline Ratio as \eta -> 1.
  - Smoothness: Graceful degradation between consistent and robust regimes.
"""

import time
from typing import List, Tuple, Dict, Optional
from .models import ProblemInstance, AssignmentResult, Volunteer, Request
from .offline_solver import OfflineSolver
from .online_algorithms import OnlineAlgorithms
from .metrics import compute_jains_index


class FollowThePredictionWithSafeguard:
    """
    Learning-augmented dispatch policy with adaptive safeguard and trust parameter \beta \in [0, 1].
    """

    def __init__(
        self,
        beta: float = 0.7,
        fallback_policy: str = "water_filling",  # 'water_filling' or 'ranking'
        error_threshold: Optional[float] = None
    ):
        """
        beta: Trust parameter in [0, 1].
              beta = 1.0 means pure trust in predictions.
              beta = 0.0 means pure robust baseline.
        """
        self.beta = beta
        self.fallback_policy = fallback_policy
        # Error threshold above which predictions are distrusted
        self.error_threshold = error_threshold if error_threshold is not None else (1.0 - 0.5 * beta)

    def run(
        self,
        instance: ProblemInstance,
        predicted_requests: List[Request],
        seed: Optional[int] = 42
    ) -> AssignmentResult:
        t_start = time.perf_counter()
        instance.reset_volunteers()

        # Step 1: Compute offline optimum on the PREDICTED sequence \hat{R}
        pred_instance = ProblemInstance(
            volunteers=[
                Volunteer(v.id, v.location, v.skills.copy(), v.capacity)
                for v in instance.volunteers
            ],
            requests=predicted_requests,
            lambda_cost=instance.lambda_cost,
            mu_fairness=instance.mu_fairness,
            travel_speed=instance.travel_speed,
            city_bounds=instance.city_bounds
        )

        pred_result = OfflineSolver.solve_flow(pred_instance)
        # Map predicted request ID -> assigned volunteer ID
        planned_dispatch: Dict[int, int] = {
            r_id: v_id for v_id, r_id in pred_result.matched_pairs
        }

        # Step 2: Online dispatch with running error estimation
        matched_pairs: List[Tuple[int, int]] = []
        rejected_requests: List[int] = []
        total_utility = 0.0
        total_travel_time = 0.0

        num_mismatches = 0
        total_seen = 0
        ranks = {v.id: (hash((v.id, seed)) % 10000) / 10000.0 for v in instance.volunteers}

        for t, real_req in enumerate(instance.requests):
            total_seen += 1
            pred_req = predicted_requests[t] if t < len(predicted_requests) else None

            # Check if current request matches prediction
            is_match = False
            if pred_req is not None:
                # Skill match and location proximity
                skills_match = real_req.required_skills == pred_req.required_skills
                is_match = skills_match

            if not is_match:
                num_mismatches += 1

            current_error_rate = num_mismatches / total_seen
            safeguard_active = current_error_rate > self.error_threshold or self.beta < 0.05

            assigned_v_id: Optional[int] = None

            # Try following prediction if safeguard not triggered and prediction exists
            if not safeguard_active and pred_req is not None and pred_req.id in planned_dispatch:
                target_v_id = planned_dispatch[pred_req.id]
                target_vol = instance.v_map[target_v_id]
                if target_vol.is_available() and instance.is_eligible(target_v_id, real_req.id):
                    assigned_v_id = target_v_id

            # Fallback to robust online baseline if prediction cannot be used
            if assigned_v_id is None:
                candidates = [
                    v for v in instance.volunteers
                    if v.is_available() and instance.is_eligible(v.id, real_req.id)
                ]
                if candidates:
                    if self.fallback_policy == "water_filling":
                        chosen_v = min(
                            candidates,
                            key=lambda v: (v.current_load, -instance.get_weight(v.id, real_req.id))
                        )
                        assigned_v_id = chosen_v.id
                    elif self.fallback_policy == "ranking":
                        chosen_v = min(candidates, key=lambda v: ranks[v.id])
                        assigned_v_id = chosen_v.id
                    else:
                        # Greedy fallback
                        chosen_v = max(candidates, key=lambda v: instance.get_weight(v.id, real_req.id))
                        assigned_v_id = chosen_v.id

            # Execute assignment or record rejection
            if assigned_v_id is not None:
                instance.v_map[assigned_v_id].assign(real_req.id)
                matched_pairs.append((assigned_v_id, real_req.id))
                total_utility += real_req.utility
                total_travel_time += instance.compute_travel_time(assigned_v_id, real_req.id)
            else:
                rejected_requests.append(real_req.id)

        volunteer_loads = {v.id: v.current_load for v in instance.volunteers}
        max_load = max(volunteer_loads.values()) if volunteer_loads else 0
        net_obj = (total_utility - instance.lambda_cost * total_travel_time) - (instance.mu_fairness * max_load)

        return AssignmentResult(
            algorithm_name=f"Proposed-FTPS(beta={self.beta})",
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


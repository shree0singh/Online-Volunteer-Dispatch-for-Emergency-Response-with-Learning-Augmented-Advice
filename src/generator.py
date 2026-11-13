"""
Instance and prediction generators for emergency response volunteer dispatch.
Includes city-grid synthetic instances and hard adversarial instances.
"""

import random
import copy
from typing import List, Tuple, Set, Optional
from .models import Volunteer, Request, ProblemInstance


SKILL_UNIVERSE = ["CPR", "FirstAid", "TraumaCare", "PediatricCare", "WaterRescue", "Hazmat"]


class InstanceGenerator:
    """Generates synthetic city-grid dispatch instances and predictions."""

    @staticmethod
    def generate_city_grid(
        num_volunteers: int = 20,
        num_requests: int = 50,
        city_size: float = 100.0,
        capacity_range: Tuple[int, int] = (2, 4),
        skills_per_volunteer: Tuple[int, int] = (2, 4),
        skills_per_request: Tuple[int, int] = (1, 2),
        utility_range: Tuple[float, float] = (15.0, 50.0),
        max_travel_time_range: Tuple[float, float] = (20.0, 45.0),
        lambda_cost: float = 0.5,
        mu_fairness: float = 0.0,
        seed: Optional[int] = 42
    ) -> ProblemInstance:
        """Generates a realistic urban emergency response instance."""
        if seed is not None:
            random.seed(seed)

        volunteers: List[Volunteer] = []
        for v_id in range(num_volunteers):
            loc = (random.uniform(0, city_size), random.uniform(0, city_size))
            k_skills = random.randint(skills_per_volunteer[0], skills_per_volunteer[1])
            skills = set(random.sample(SKILL_UNIVERSE, k=k_skills))
            cap = random.randint(capacity_range[0], capacity_range[1])
            volunteers.append(Volunteer(id=v_id, location=loc, skills=skills, capacity=cap))

        requests: List[Request] = []
        for r_id in range(num_requests):
            loc = (random.uniform(0, city_size), random.uniform(0, city_size))
            k_req = random.randint(skills_per_request[0], skills_per_request[1])
            req_skills = set(random.sample(SKILL_UNIVERSE, k=k_req))
            utility = round(random.uniform(utility_range[0], utility_range[1]), 2)
            max_tt = round(random.uniform(max_travel_time_range[0], max_travel_time_range[1]), 2)
            requests.append(Request(
                id=r_id,
                location=loc,
                required_skills=req_skills,
                utility=utility,
                max_travel_time=max_tt,
                arrival_index=r_id
            ))

        return ProblemInstance(
            volunteers=volunteers,
            requests=requests,
            lambda_cost=lambda_cost,
            mu_fairness=mu_fairness,
            city_bounds=(city_size, city_size)
        )

    @staticmethod
    def generate_adversarial_instance(k: int = 10, lambda_cost: float = 0.0) -> ProblemInstance:
        """
        Generates an adversarial instance exposing the 1/2 competitive ratio of Greedy.
        Structure:
          - Volunteers: V = {v_1, ..., v_{2k}} all with capacity 1 and skill "CPR"
          - Phase 1: Requests r_1, ..., r_k arrive.
                     Request r_i is eligible for BOTH v_i and v_{k+i}.
                     Greedy is biased/tied to pick v_i.
          - Phase 2: Requests r_{k+1}, ..., r_{2k} arrive.
                     Request r_{k+i} is eligible ONLY for v_i.
                     Since Greedy consumed v_i in Phase 1, it must reject r_{k+i}.
                     Greedy matches k requests.
                     OPT matches r_i -> v_{k+i} and r_{k+i} -> v_i, matching all 2k requests!
                     Competitive ratio = k / 2k = 1/2.
        """
        volunteers: List[Volunteer] = []
        # 2*k volunteers
        for i in range(2 * k):
            # Place v_i at coordinates (i * 2, 0)
            volunteers.append(Volunteer(
                id=i,
                location=(float(i * 2), 0.0),
                skills={"CPR"},
                capacity=1
            ))

        requests: List[Request] = []
        # Phase 1: r_0 .. r_{k-1}
        for i in range(k):
            # Position r_i closer to v_i than to v_{k+i} to strictly force Greedy to pick v_i
            # v_i is at (2i, 0), v_{k+i} is at (2(k+i), 0)
            # r_i is placed at (2i + 0.1, 0)
            requests.append(Request(
                id=i,
                location=(float(2 * i + 0.1), 0.0),
                required_skills={"CPR"},
                utility=20.0,
                max_travel_time=100.0,
                arrival_index=i
            ))

        # Phase 2: r_k .. r_{2k-1}
        for i in range(k):
            req_id = k + i
            # r_{k+i} is placed at (2i, 0), but with max travel time 0.5, so only v_i is eligible!
            requests.append(Request(
                id=req_id,
                location=(float(2 * i), 0.0),
                required_skills={"CPR"},
                utility=20.0,
                max_travel_time=0.5,
                arrival_index=req_id
            ))

        return ProblemInstance(
            volunteers=volunteers,
            requests=requests,
            lambda_cost=lambda_cost,
            mu_fairness=0.0
        )

    @staticmethod
    def generate_predictions(
        true_requests: List[Request],
        error_rate_eta: float,
        seed: Optional[int] = None
    ) -> List[Request]:
        """
        Generates a predicted sequence \hat{R} with error rate \eta \in [0, 1].
        \eta fraction of requests are corrupted (skill set changed or location shifted).
        """
        if seed is not None:
            random.seed(seed)

        predicted_requests: List[Request] = []
        num_mismatches = int(round(error_rate_eta * len(true_requests)))
        corrupted_indices = set(random.sample(range(len(true_requests)), k=num_mismatches))

        for idx, req in enumerate(true_requests):
            pred_req = copy.deepcopy(req)
            if idx in corrupted_indices:
                # Corrupt the request: alter required skills and drastically shift location
                all_skills = list(SKILL_UNIVERSE)
                # Pick skills disjoint from true skills if possible
                diff_skills = [s for s in all_skills if s not in req.required_skills]
                if diff_skills:
                    pred_req.required_skills = set(random.sample(diff_skills, k=1))
                else:
                    pred_req.required_skills = {"Hazmat"}
                # Shift coordinates
                pred_req.location = (
                    (pred_req.location[0] + 50.0) % 100.0,
                    (pred_req.location[1] + 50.0) % 100.0
                )
                pred_req.utility = max(5.0, pred_req.utility * random.uniform(0.5, 1.5))
            pred_req.predicted_type_id = idx
            predicted_requests.append(pred_req)

        return predicted_requests


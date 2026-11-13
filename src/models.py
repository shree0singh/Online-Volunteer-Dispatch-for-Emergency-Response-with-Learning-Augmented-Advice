"""
Data models and core definitions for Online Volunteer Dispatch.
Problem Statement 6: Online Volunteer Dispatch for Emergency Response
"""

from dataclasses import dataclass, field
from typing import Set, Tuple, List, Dict, Optional
import math
import numpy as np


@dataclass
class Volunteer:
    """Represents a volunteer first responder."""
    id: int
    location: Tuple[float, float]
    skills: Set[str]
    capacity: int  # maximum allowed assignments in planning horizon (\kappa_v)
    current_load: int = 0
    assigned_requests: List[int] = field(default_factory=list)

    @property
    def remaining_capacity(self) -> int:
        return self.capacity - self.current_load

    def is_available(self) -> bool:
        return self.remaining_capacity > 0

    def assign(self, request_id: int):
        if not self.is_available():
            raise ValueError(f"Volunteer {self.id} has reached capacity {self.capacity}")
        self.current_load += 1
        self.assigned_requests.append(request_id)

    def reset(self):
        self.current_load = 0
        self.assigned_requests = []


@dataclass
class Request:
    """Represents an incoming emergency incident request."""
    id: int
    location: Tuple[float, float]
    required_skills: Set[str]
    utility: float  # priority-based utility u_r
    max_travel_time: float  # threshold \theta_r
    arrival_index: int = 0  # sequence position
    predicted_type_id: Optional[int] = None  # for learning-augmented advice

    @property
    def skill_key(self) -> str:
        return "-".join(sorted(list(self.required_skills)))


@dataclass
class AssignmentResult:
    """Stores the execution trace and outcomes of a dispatch policy."""
    algorithm_name: str
    matched_pairs: List[Tuple[int, int]]  # (volunteer_id, request_id)
    rejected_requests: List[int]
    total_utility: float
    total_travel_time: float
    net_objective: float  # sum w_vr - mu * L
    max_load: int
    volunteer_loads: Dict[int, int]
    jains_fairness_index: float
    execution_time_seconds: float = 0.0


class ProblemInstance:
    """
    Encapsulates all static and dynamic components of the dispatch instance.
    """
    def __init__(
        self,
        volunteers: List[Volunteer],
        requests: List[Request],
        lambda_cost: float = 0.5,
        mu_fairness: float = 0.0,
        travel_speed: float = 1.0,
        city_bounds: Tuple[float, float] = (100.0, 100.0)
    ):
        self.volunteers = volunteers
        self.requests = requests
        self.lambda_cost = lambda_cost
        self.mu_fairness = mu_fairness
        self.travel_speed = travel_speed
        self.city_bounds = city_bounds

        self.v_map: Dict[int, Volunteer] = {v.id: v for v in volunteers}
        self.r_map: Dict[int, Request] = {r.id: r for r in requests}

        # Cache travel times and weights
        self._travel_times: Dict[Tuple[int, int], float] = {}
        self._weights: Dict[Tuple[int, int], float] = {}
        self._eligibility: Dict[Tuple[int, int], bool] = {}

    def compute_travel_time(self, v_id: int, r_id: int) -> float:
        key = (v_id, r_id)
        if key not in self._travel_times:
            vx, vy = self.v_map[v_id].location
            rx, ry = self.r_map[r_id].location
            euclidean_dist = math.hypot(vx - rx, vy - ry)
            self._travel_times[key] = euclidean_dist / self.travel_speed
        return self._travel_times[key]

    def is_eligible(self, v_id: int, r_id: int) -> bool:
        """
        Check if volunteer v meets requirements for request r:
        1. Required skills Q_r subset of Volunteer skills S_v
        2. Travel time c_vr <= max acceptable travel time \theta_r
        3. Weight w_vr = u_r - \lambda * c_vr > 0
        """
        key = (v_id, r_id)
        if key in self._eligibility:
            return self._eligibility[key]

        vol = self.v_map[v_id]
        req = self.r_map[r_id]

        # Skill requirement check: Q_r \subseteq S_v
        if not req.required_skills.issubset(vol.skills):
            self._eligibility[key] = False
            return False

        # Travel time threshold check: c_vr <= \theta_r
        c_vr = self.compute_travel_time(v_id, r_id)
        if c_vr > req.max_travel_time:
            self._eligibility[key] = False
            return False

        # Net positive weight check: w_vr = u_r - \lambda * c_vr > 0
        w_vr = req.utility - self.lambda_cost * c_vr
        self._weights[key] = w_vr
        eligible = w_vr > 0
        self._eligibility[key] = eligible
        return eligible

    def get_weight(self, v_id: int, r_id: int) -> float:
        key = (v_id, r_id)
        if key not in self._weights:
            c_vr = self.compute_travel_time(v_id, r_id)
            self._weights[key] = self.r_map[r_id].utility - self.lambda_cost * c_vr
        return self._weights[key]

    def get_eligible_volunteers(self, r_id: int) -> List[int]:
        """Returns list of all volunteer IDs eligible for request r."""
        return [v.id for v in self.volunteers if self.is_eligible(v.id, r_id)]

    def get_eligible_edges(self) -> List[Tuple[int, int, float]]:
        """Returns all edges (v_id, r_id, weight) in the bipartite eligibility graph E."""
        edges = []
        for v in self.volunteers:
            for r in self.requests:
                if self.is_eligible(v.id, r.id):
                    edges.append((v.id, r.id, self.get_weight(v.id, r.id)))
        return edges

    def reset_volunteers(self):
        for v in self.volunteers:
            v.reset()


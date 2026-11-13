"""
Simulation orchestrator and benchmarking suite for Online Volunteer Dispatch.
Runs Offline OPT, Greedy, Random, KVV Ranking, Water-Filling, and Proposed FTPS.
"""

from typing import Dict, List, Any
import copy
from .models import ProblemInstance, AssignmentResult
from .offline_solver import OfflineSolver
from .online_algorithms import OnlineAlgorithms
from .learning_augmented import FollowThePredictionWithSafeguard
from .generator import InstanceGenerator
from .metrics import compute_competitive_ratio


class DispatchSimulator:
    """Runs and compares all dispatch algorithms on an instance."""

    def __init__(self, instance: ProblemInstance, predicted_requests: List[Any], beta: float = 0.7):
        self.instance = instance
        self.predicted_requests = predicted_requests
        self.beta = beta

    def run_all(self, seed: int = 42) -> Dict[str, Dict[str, Any]]:
        """
        Executes all policies and returns comprehensive comparative statistics.
        """
        # 1. Offline Optimal Benchmark
        opt_res = OfflineSolver.solve_flow(self.instance)
        # If mu > 0, solve with MILP
        if self.instance.mu_fairness > 0:
            opt_res = OfflineSolver.solve_milp(self.instance)

        # 2. Online Baselines
        greedy_res = OnlineAlgorithms.run_greedy(self.instance)
        random_res = OnlineAlgorithms.run_random(self.instance, seed=seed)
        ranking_res = OnlineAlgorithms.run_ranking(self.instance, seed=seed)
        water_res = OnlineAlgorithms.run_water_filling(self.instance)

        # 3. Proposed Learning-Augmented Policy
        ftps = FollowThePredictionWithSafeguard(beta=self.beta, fallback_policy="water_filling")
        ftps_res = ftps.run(self.instance, self.predicted_requests, seed=seed)

        all_results = {
            "Offline-OPT": opt_res,
            "Greedy": greedy_res,
            "Random": random_res,
            "KVV-Ranking": ranking_res,
            "Water-Filling": water_res,
            "Proposed-FTPS": ftps_res
        }

        opt_obj = opt_res.net_objective

        summary = {}
        for name, res in all_results.items():
            cr = compute_competitive_ratio(res.net_objective, opt_obj)
            matched_count = len(res.matched_pairs)
            service_rate = (matched_count / len(self.instance.requests)) if self.instance.requests else 0.0

            summary[name] = {
                "algorithm": name,
                "net_objective": res.net_objective,
                "competitive_ratio": round(cr, 4),
                "matched_count": matched_count,
                "service_rate": round(service_rate, 4),
                "total_utility": res.total_utility,
                "total_travel_time": res.total_travel_time,
                "max_load": res.max_load,
                "jains_fairness": res.jains_fairness_index,
                "exec_time_sec": res.execution_time_seconds
            }

        return summary


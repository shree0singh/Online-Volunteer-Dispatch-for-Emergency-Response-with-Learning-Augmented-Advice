"""
Comprehensive Unit and System Test Suite for PS-6: Online Volunteer Dispatch.
Verifies invariants, theoretical bounds, and implementation correctness.
"""

import unittest
from src.models import Volunteer, Request, ProblemInstance
from src.generator import InstanceGenerator
from src.offline_solver import OfflineSolver
from src.online_algorithms import OnlineAlgorithms
from src.learning_augmented import FollowThePredictionWithSafeguard
from src.metrics import compute_jains_index, compute_competitive_ratio


class TestVolunteerDispatch(unittest.TestCase):

    def setUp(self):
        self.instance = InstanceGenerator.generate_city_grid(
            num_volunteers=10,
            num_requests=25,
            city_size=50.0,
            seed=101
        )

    def test_eligibility_constraints(self):
        """Verify that eligibility strictly enforces skill containment and travel bounds."""
        v = Volunteer(id=0, location=(0.0, 0.0), skills={"CPR"}, capacity=2)
        r_valid = Request(id=0, location=(3.0, 4.0), required_skills={"CPR"}, utility=20.0, max_travel_time=10.0)
        r_unskilled = Request(id=1, location=(3.0, 4.0), required_skills={"TraumaCare"}, utility=20.0, max_travel_time=10.0)
        r_far = Request(id=2, location=(30.0, 40.0), required_skills={"CPR"}, utility=20.0, max_travel_time=10.0)

        inst = ProblemInstance(volunteers=[v], requests=[r_valid, r_unskilled, r_far], lambda_cost=0.5)

        self.assertTrue(inst.is_eligible(0, 0))
        self.assertFalse(inst.is_eligible(0, 1), "Should fail due to missing skill")
        self.assertFalse(inst.is_eligible(0, 2), "Should fail due to travel time exceeding deadline")

    def test_offline_solvers_equivalence_when_mu_zero(self):
        """Verify that Flow and MILP solvers yield identical objectives when fairness penalty mu = 0."""
        res_milp = OfflineSolver.solve_milp(self.instance)
        res_flow = OfflineSolver.solve_flow(self.instance)

        # Allow slight rounding difference due to integer scaling in flow
        self.assertAlmostEqual(res_milp.net_objective, res_flow.net_objective, delta=1.5)
        self.assertEqual(len(res_milp.matched_pairs), len(res_flow.matched_pairs))

    def test_volunteer_capacity_invariants(self):
        """Verify that NO algorithm violates any volunteer's maximum capacity kappa_v."""
        preds = InstanceGenerator.generate_predictions(self.instance.requests, error_rate_eta=0.2, seed=42)

        algorithms = [
            ("Greedy", lambda: OnlineAlgorithms.run_greedy(self.instance)),
            ("Random", lambda: OnlineAlgorithms.run_random(self.instance, seed=42)),
            ("Ranking", lambda: OnlineAlgorithms.run_ranking(self.instance, seed=42)),
            ("WaterFilling", lambda: OnlineAlgorithms.run_water_filling(self.instance)),
            ("FTPS", lambda: FollowThePredictionWithSafeguard(beta=0.7).run(self.instance, preds, seed=42))
        ]

        for name, alg_func in algorithms:
            res = alg_func()
            for v_id, load in res.volunteer_loads.items():
                cap = self.instance.v_map[v_id].capacity
                self.assertLessEqual(load, cap, f"Algorithm {name} violated capacity for volunteer {v_id}!")

    def test_adversarial_instance_greedy_half_ratio(self):
        """
        Verify the theoretical adversarial counterexample where Greedy achieves ratio <= 0.5.
        """
        adv_inst = InstanceGenerator.generate_adversarial_instance(k=6)
        opt_res = OfflineSolver.solve_flow(adv_inst)
        greedy_res = OnlineAlgorithms.run_greedy(adv_inst)

        # In this instance, OPT should match all 2k = 12 requests
        self.assertEqual(len(opt_res.matched_pairs), 12)
        # Greedy matches exactly k = 6 requests
        self.assertEqual(len(greedy_res.matched_pairs), 6)
        # Competitive ratio is exactly 6 / 12 = 0.5
        cr = compute_competitive_ratio(greedy_res.net_objective, opt_res.net_objective)
        self.assertAlmostEqual(cr, 0.5, delta=0.01)

    def test_learning_augmented_consistency_and_robustness(self):
        """Verify consistency (eta=0 -> ratio ~ 1.0) and robustness (eta=1 -> ratio >= baseline)."""
        # Perfect predictions (eta = 0.0)
        perfect_preds = InstanceGenerator.generate_predictions(self.instance.requests, error_rate_eta=0.0)
        opt_res = OfflineSolver.solve_flow(self.instance)
        ftps_perfect = FollowThePredictionWithSafeguard(beta=1.0).run(self.instance, perfect_preds)
        cr_perfect = compute_competitive_ratio(ftps_perfect.net_objective, opt_res.net_objective)
        self.assertGreaterEqual(cr_perfect, 0.98, "At eta=0, FTPS should achieve near-optimal consistency >= 0.98")

        # Completely corrupted predictions (eta = 1.0)
        corrupted_preds = InstanceGenerator.generate_predictions(self.instance.requests, error_rate_eta=1.0, seed=999)
        ftps_corrupt = FollowThePredictionWithSafeguard(beta=0.6).run(self.instance, corrupted_preds)
        cr_corrupt = compute_competitive_ratio(ftps_corrupt.net_objective, opt_res.net_objective)
        self.assertGreater(cr_corrupt, 0.4, "At eta=1, FTPS safeguard should maintain baseline robustness")

    def test_jains_fairness_index_bounds(self):
        """Verify Jain's index properties: 1.0 for equal loads, bounded in [1/n, 1.0]."""
        self.assertAlmostEqual(compute_jains_index([2, 2, 2, 2]), 1.0)
        self.assertAlmostEqual(compute_jains_index([4, 0, 0, 0]), 1/4)
        loads = [1, 2, 3, 4]
        j = compute_jains_index(loads)
        self.assertTrue(1/4 <= j <= 1.0)


if __name__ == "__main__":
    unittest.main()


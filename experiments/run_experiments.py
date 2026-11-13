"""
Comprehensive Experimental Benchmarking Suite for PS-6: Online Volunteer Dispatch.
Runs Monte Carlo experiments, records performance statistics, and generates figures.
"""

import os
import sys
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Any

# Ensure root directory is on python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.models import ProblemInstance
from src.generator import InstanceGenerator
from src.offline_solver import OfflineSolver
from src.online_algorithms import OnlineAlgorithms
from src.learning_augmented import FollowThePredictionWithSafeguard
from src.metrics import compute_competitive_ratio, compute_jains_index


# Styling for academic figures
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 14
})


def run_experiment_1_eta_sweep(
    output_dir: str,
    num_runs: int = 10,
    num_volunteers: int = 25,
    num_requests: int = 60
) -> pd.DataFrame:
    """
    Experiment 1: Competitive Ratio vs Prediction Error Rate \eta \in [0, 1].
    Evaluates consistency (as \eta -> 0) and robustness (as \eta -> 1).
    """
    print("Running Experiment 1: Competitive Ratio vs Prediction Error (\eta)...")
    eta_values = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    records = []

    for eta in eta_values:
        for seed in range(num_runs):
            instance = InstanceGenerator.generate_city_grid(
                num_volunteers=num_volunteers,
                num_requests=num_requests,
                city_size=100.0,
                capacity_range=(2, 4),
                lambda_cost=0.4,
                seed=seed + 100
            )

            # Offline OPT
            opt_res = OfflineSolver.solve_flow(instance)
            opt_obj = opt_res.net_objective

            if opt_obj <= 0:
                continue

            # Online Baselines
            greedy_res = OnlineAlgorithms.run_greedy(instance)
            random_res = OnlineAlgorithms.run_random(instance, seed=seed)
            ranking_res = OnlineAlgorithms.run_ranking(instance, seed=seed)
            water_res = OnlineAlgorithms.run_water_filling(instance)

            # Proposed FTPS with different trust levels
            preds = InstanceGenerator.generate_predictions(instance.requests, error_rate_eta=eta, seed=seed + 500)
            ftps_high = FollowThePredictionWithSafeguard(beta=0.85).run(instance, preds, seed=seed)
            ftps_mid = FollowThePredictionWithSafeguard(beta=0.50).run(instance, preds, seed=seed)

            records.append({
                "eta": eta,
                "seed": seed,
                "Greedy": compute_competitive_ratio(greedy_res.net_objective, opt_obj),
                "Random": compute_competitive_ratio(random_res.net_objective, opt_obj),
                "Ranking": compute_competitive_ratio(ranking_res.net_objective, opt_obj),
                "WaterFilling": compute_competitive_ratio(water_res.net_objective, opt_obj),
                "FTPS (beta=0.85)": compute_competitive_ratio(ftps_high.net_objective, opt_obj),
                "FTPS (beta=0.50)": compute_competitive_ratio(ftps_mid.net_objective, opt_obj),
            })

    df = pd.DataFrame(records)
    summary = df.groupby("eta").mean().reset_index()

    # Generate Figure 1
    plt.figure(figsize=(8, 5), dpi=300)
    plt.plot(summary["eta"], summary["FTPS (beta=0.85)"], 'r-o', linewidth=2.2, label="Proposed FTPS (β=0.85)")
    plt.plot(summary["eta"], summary["FTPS (beta=0.50)"], 'm--^', linewidth=2.0, label="Proposed FTPS (β=0.50)")
    plt.plot(summary["eta"], summary["WaterFilling"], 'g-s', linewidth=1.8, label="Water-Filling (Balance)")
    plt.plot(summary["eta"], summary["Ranking"], 'b-d', linewidth=1.8, label="KVV Ranking")
    plt.plot(summary["eta"], summary["Greedy"], 'c-.v', linewidth=1.8, label="Greedy (Nearest)")
    plt.plot(summary["eta"], summary["Random"], 'k:', linewidth=1.5, label="Random Baseline")

    plt.axhline(y=1.0, color='gray', linestyle='--', alpha=0.7, label="Offline OPT Benchmark")
    plt.xlabel("Prediction Error Rate (η)")
    plt.ylabel("Competitive Ratio (ALG / OPT)")
    plt.title("Competitive Ratio vs. Prediction Error (Consistency & Robustness)")
    plt.ylim(0.4, 1.05)
    plt.legend(loc='lower left', frameon=True)
    plt.tight_layout()
    plot_path = os.path.join(output_dir, "exp1_competitive_ratio_vs_eta.png")
    plt.savefig(plot_path)
    plt.close()
    print(f"Saved: {plot_path}")

    return summary


def run_experiment_2_fairness_and_capacity(
    output_dir: str,
    num_runs: int = 10
) -> pd.DataFrame:
    """
    Experiment 2: Workload distribution, Jain's Fairness Index, and Max Load vs Capacity.
    """
    print("Running Experiment 2: Fairness & Capacity Analysis...")
    capacities = [1, 2, 3, 4, 5, 6]
    records = []

    for cap in capacities:
        for seed in range(num_runs):
            instance = InstanceGenerator.generate_city_grid(
                num_volunteers=20,
                num_requests=50,
                city_size=100.0,
                capacity_range=(cap, cap),
                lambda_cost=0.4,
                seed=seed + 200
            )

            preds = InstanceGenerator.generate_predictions(instance.requests, error_rate_eta=0.2, seed=seed)

            greedy_res = OnlineAlgorithms.run_greedy(instance)
            water_res = OnlineAlgorithms.run_water_filling(instance)
            ftps_res = FollowThePredictionWithSafeguard(beta=0.7).run(instance, preds, seed=seed)
            milp_fair_res = OfflineSolver.solve_milp(
                ProblemInstance(
                    volunteers=instance.volunteers,
                    requests=instance.requests,
                    lambda_cost=0.4,
                    mu_fairness=2.0
                )
            )

            records.append({
                "capacity": cap,
                "Greedy_Jain": greedy_res.jains_fairness_index,
                "Greedy_MaxLoad": greedy_res.max_load,
                "WaterFilling_Jain": water_res.jains_fairness_index,
                "WaterFilling_MaxLoad": water_res.max_load,
                "FTPS_Jain": ftps_res.jains_fairness_index,
                "FTPS_MaxLoad": ftps_res.max_load,
                "MILP_Fair_Jain": milp_fair_res.jains_fairness_index,
                "MILP_Fair_MaxLoad": milp_fair_res.max_load,
            })

    df = pd.DataFrame(records)
    summary = df.groupby("capacity").mean().reset_index()

    # Figure 2: Jain's Fairness Index vs Volunteer Capacity
    plt.figure(figsize=(8, 5), dpi=300)
    plt.plot(summary["capacity"], summary["WaterFilling_Jain"], 'g-s', linewidth=2.2, label="Water-Filling (Balance)")
    plt.plot(summary["capacity"], summary["FTPS_Jain"], 'r-o', linewidth=2.0, label="Proposed FTPS (β=0.7)")
    plt.plot(summary["capacity"], summary["MILP_Fair_Jain"], 'm--^', linewidth=2.0, label="Offline MILP (μ=2.0)")
    plt.plot(summary["capacity"], summary["Greedy_Jain"], 'c-.v', linewidth=1.8, label="Greedy (Nearest)")

    plt.xlabel("Volunteer Capacity Limit (κ)")
    plt.ylabel("Jain's Fairness Index (Higher is fairer)")
    plt.title("Workload Fairness vs. Volunteer Capacity Limit")
    plt.ylim(0.4, 1.0)
    plt.legend(loc='lower right', frameon=True)
    plt.tight_layout()
    plot_path = os.path.join(output_dir, "exp2_jains_fairness_vs_capacity.png")
    plt.savefig(plot_path)
    plt.close()
    print(f"Saved: {plot_path}")

    return summary


def run_experiment_3_adversarial_comparison(output_dir: str) -> pd.DataFrame:
    """
    Experiment 3: Performance Under Adversarial vs Random Request Arrivals.
    Exposes the 0.5 competitive barrier of Greedy under worst-case arrivals.
    """
    print("Running Experiment 3: Adversarial vs Random Arrival Evaluation...")
    k_values = [4, 6, 8, 10, 12, 16]
    records = []

    for k in k_values:
        adv_inst = InstanceGenerator.generate_adversarial_instance(k=k)
        opt_res = OfflineSolver.solve_flow(adv_inst)
        greedy_res = OnlineAlgorithms.run_greedy(adv_inst)
        ranking_res = OnlineAlgorithms.run_ranking(adv_inst, seed=42)
        water_res = OnlineAlgorithms.run_water_filling(adv_inst)

        # Learning-augmented with adversarial predictions (e.g. eta = 0.5)
        preds = InstanceGenerator.generate_predictions(adv_inst.requests, error_rate_eta=0.5, seed=42)
        ftps_res = FollowThePredictionWithSafeguard(beta=0.6).run(adv_inst, preds, seed=42)

        opt_obj = opt_res.net_objective
        records.append({
            "k": k,
            "Total_Requests": 2 * k,
            "OPT_Matched": len(opt_res.matched_pairs),
            "Greedy_CR": round(compute_competitive_ratio(greedy_res.net_objective, opt_obj), 4),
            "Ranking_CR": round(compute_competitive_ratio(ranking_res.net_objective, opt_obj), 4),
            "WaterFilling_CR": round(compute_competitive_ratio(water_res.net_objective, opt_obj), 4),
            "FTPS_CR": round(compute_competitive_ratio(ftps_res.net_objective, opt_obj), 4),
        })

    df = pd.DataFrame(records)

    # Figure 3: Adversarial Ratio
    plt.figure(figsize=(8, 5), dpi=300)
    plt.plot(df["k"], df["Greedy_CR"], 'r-o', linewidth=2.2, label="Greedy (Collapses to 0.5)")
    plt.plot(df["k"], df["Ranking_CR"], 'b-s', linewidth=2.0, label="KVV Ranking")
    plt.plot(df["k"], df["WaterFilling_CR"], 'g-^', linewidth=2.0, label="Water-Filling")
    plt.plot(df["k"], df["FTPS_CR"], 'm--d', linewidth=2.0, label="Proposed FTPS (β=0.6)")

    plt.axhline(y=0.5, color='black', linestyle=':', label="Theoretical 1/2 Lower Bound")
    plt.axhline(y=1.0 - 1.0/np.e, color='gray', linestyle='--', label="KVV Theoretical Bound (1 - 1/e ≈ 0.632)")
    plt.xlabel("Instance Scale Parameter k (2k requests, 2k volunteers)")
    plt.ylabel("Competitive Ratio (ALG / OPT)")
    plt.title("Adversarial Arrival Order: Greedy Barrier vs. Robust Policies")
    plt.ylim(0.4, 0.9)
    plt.legend(loc='center right', frameon=True)
    plt.tight_layout()
    plot_path = os.path.join(output_dir, "exp3_adversarial_performance.png")
    plt.savefig(plot_path)
    plt.close()
    print(f"Saved: {plot_path}")

    return df


def run_experiment_4_lambda_tradeoff(output_dir: str, num_runs: int = 8) -> pd.DataFrame:
    """
    Experiment 4: Trade-off between Utility and Travel Time under varying cost weights \lambda.
    """
    print("Running Experiment 4: Cost Weight Trade-Off Analysis...")
    lambdas = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5]
    records = []

    for lam in lambdas:
        for seed in range(num_runs):
            instance = InstanceGenerator.generate_city_grid(
                num_volunteers=20,
                num_requests=50,
                city_size=100.0,
                lambda_cost=lam,
                seed=seed + 300
            )

            opt_res = OfflineSolver.solve_flow(instance)
            greedy_res = OnlineAlgorithms.run_greedy(instance)
            preds = InstanceGenerator.generate_predictions(instance.requests, error_rate_eta=0.2, seed=seed)
            ftps_res = FollowThePredictionWithSafeguard(beta=0.7).run(instance, preds, seed=seed)

            records.append({
                "lambda": lam,
                "OPT_Net": opt_res.net_objective,
                "OPT_Matched": len(opt_res.matched_pairs),
                "OPT_TravelTime": opt_res.total_travel_time,
                "FTPS_Net": ftps_res.net_objective,
                "FTPS_Matched": len(ftps_res.matched_pairs),
                "FTPS_TravelTime": ftps_res.total_travel_time,
                "Greedy_Net": greedy_res.net_objective,
                "Greedy_Matched": len(greedy_res.matched_pairs),
                "Greedy_TravelTime": greedy_res.total_travel_time,
            })

    df = pd.DataFrame(records)
    summary = df.groupby("lambda").mean().reset_index()

    # Figure 4: Net Objective vs Lambda
    plt.figure(figsize=(8, 5), dpi=300)
    plt.plot(summary["lambda"], summary["OPT_Net"], 'k-', linewidth=2.2, label="Offline OPT")
    plt.plot(summary["lambda"], summary["FTPS_Net"], 'r-o', linewidth=2.0, label="Proposed FTPS (β=0.7)")
    plt.plot(summary["lambda"], summary["Greedy_Net"], 'c--s', linewidth=1.8, label="Greedy")

    plt.xlabel("Travel Time Cost Weight (λ)")
    plt.ylabel("Net Objective (Total Utility - λ * Travel Time)")
    plt.title("Net Objective Trade-Off Across Travel Cost Penalty (λ)")
    plt.legend(loc='upper right', frameon=True)
    plt.tight_layout()
    plot_path = os.path.join(output_dir, "exp4_lambda_tradeoff.png")
    plt.savefig(plot_path)
    plt.close()
    print(f"Saved: {plot_path}")

    return summary


def main():
    output_dir = "/home/shree/code/krishna/experiments/plots"
    os.makedirs(output_dir, exist_ok=True)

    print("=== STARTING FULL EXPERIMENTAL BENCHMARKING ===")
    df1 = run_experiment_1_eta_sweep(output_dir)
    df2 = run_experiment_2_fairness_and_capacity(output_dir)
    df3 = run_experiment_3_adversarial_comparison(output_dir)
    df4 = run_experiment_4_lambda_tradeoff(output_dir)

    # Save summary tables to CSV
    csv_dir = "/home/shree/code/krishna/experiments"
    df1.to_csv(os.path.join(csv_dir, "exp1_eta_results.csv"), index=False)
    df2.to_csv(os.path.join(csv_dir, "exp2_fairness_results.csv"), index=False)
    df3.to_csv(os.path.join(csv_dir, "exp3_adversarial_results.csv"), index=False)
    df4.to_csv(os.path.join(csv_dir, "exp4_lambda_results.csv"), index=False)

    print("\n=== EXPERIMENTAL BENCHMARKING COMPLETE ===")
    print(f"Plots saved to: {output_dir}")
    print(f"CSV data tables saved to: {csv_dir}")


if __name__ == "__main__":
    main()

"""
Evaluation metrics: Competitive Ratio, Jain's Fairness Index, Load distribution, and error stats.
"""

from typing import List, Dict
import numpy as np


def compute_jains_index(loads: List[int]) -> float:
    """
    Computes Jain's Fairness Index for volunteer workloads:
    J(x_1, ..., x_n) = (sum x_i)^2 / (n * sum (x_i^2))
    Returns 1.0 if all loads are equal (or all zero).
    Bounded between 1/n (worst case) and 1.0 (best case).
    """
    if not loads:
        return 1.0
    arr = np.array(loads, dtype=float)
    total = np.sum(arr)
    if total == 0:
        return 1.0
    n = len(arr)
    sum_sq = np.sum(arr ** 2)
    if sum_sq == 0:
        return 1.0
    return float((total ** 2) / (n * sum_sq))


def compute_competitive_ratio(alg_obj: float, opt_obj: float) -> float:
    """
    Computes Competitive Ratio: ALG / OPT.
    In case OPT is 0, returns 1.0 if ALG is 0 else 0.0.
    """
    if opt_obj <= 0:
        return 1.0 if alg_obj >= 0 else 0.0
    return float(alg_obj / opt_obj)


def compute_prediction_error(true_types: List[str], predicted_types: List[str]) -> float:
    """
    Computes error rate eta = 1 - |R \cap \hat{R}| / |R|
    Fraction of requests whose predicted type differs from the real one.
    """
    if not true_types:
        return 0.0
    mismatches = sum(1 for t, p in zip(true_types, predicted_types) if t != p)
    return float(mismatches / len(true_types))


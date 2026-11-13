# Online Volunteer Dispatch for Emergency Response

**Course:** Advanced Algorithms (Problem Statement 6)  
**Institution:** Rajiv Gandhi Institute of Petroleum Technology (RGIPT)  
**Academic Year:** 2026–27  

---

## 📌 Project Overview
In medical or disaster emergencies, trained civilian volunteers can reach victims crucial minutes before ambulances arrive. This repository contains the complete algorithmic formulation, exact offline optimization models, competitive analysis, and a learning-augmented dispatch algorithm (**Follow-the-Prediction with Safeguard - FTPS**) for online volunteer dispatch.

### Key Highlights:
1. **Exact Offline Optimization:** Formulated as an Integer Linear Program (ILP) with fairness penalties and solved in polynomial time via Minimum Cost Flow (NetworkX) and MILP (SciPy HiGHS).
2. **Adversarial Competitive Analysis:** Rigorous mathematical proofs and empirical demonstration of the $1/2$ competitive ratio lower bound for deterministic greedy dispatch.
3. **Randomized Matching:** Karp-Vazirani-Vazirani (KVV 1990) Ranking algorithm achieving $1 - 1/e \approx 0.632$ competitive ratio.
4. **Proposed Algorithm (FTPS):** Learning-augmented online dispatch with trust parameter $\beta \in [0, 1]$ and adaptive error tracking, guaranteeing consistency ($\text{CR} \to 1.0$ as $\eta \to 0$) and robustness against adversarial predictions.
5. **Fairness Evaluation:** Real-time tracking of Jain's Fairness Index ($\mathcal{J} \in [1/n, 1]$) and peak volunteer load to prevent responder burnout.

---

## 📂 Repository Structure
```
krishna/
├── README.md                                # Project overview and guide
├── requirements.txt                         # Python dependencies
├── src/
│   ├── __init__.py                          # Package initialization
│   ├── models.py                            # Volunteer, Request, ProblemInstance models
│   ├── generator.py                         # City-grid & adversarial instance generators
│   ├── offline_solver.py                    # SciPy HiGHS MILP & NetworkX Min-Cost Flow
│   ├── online_algorithms.py                 # Greedy, Random, KVV Ranking, Water-Filling
│   ├── learning_augmented.py                # Proposed FTPS algorithm with safeguard
│   ├── metrics.py                           # Competitive ratio & Jain's fairness index
│   └── simulator.py                         # End-to-end benchmarking runner
├── experiments/
│   ├── run_experiments.py                   # Monte Carlo evaluation suite
│   ├── exp1_eta_results.csv                 # CR vs prediction error results
│   ├── exp2_fairness_results.csv            # Fairness & capacity results
│   ├── exp3_adversarial_results.csv         # Adversarial arrival order results
│   ├── exp4_lambda_results.csv              # Travel cost trade-off results
│   └── plots/                               # Publication-quality benchmark figures
│       ├── exp1_competitive_ratio_vs_eta.png
│       ├── exp2_jains_fairness_vs_capacity.png
│       ├── exp3_adversarial_performance.png
│       └── exp4_lambda_tradeoff.png
├── tests/
│   └── test_suite.py                        # Comprehensive unit & invariant tests
├── paper/
│   ├── research_paper.md                    # Full conference format research paper
│   └── Research_Paper.pdf                   # IEEE two-column formatted conference paper
├── pdf_generator/
│   ├── generate_all_pdfs.py                 # ReportLab script compiling all 5 viva PDFs
│   └── generate_ieee_paper.py               # IEEE two-column conference paper generator
├── IEEE_Research_Paper_Online_Volunteer_Dispatch.pdf # IEEE two-column conference paper
├── Research Paper – Online Volunteer Dispatch.pdf    # Final research paper (IEEE format)
├── Member 1 – Study Guide.pdf               # Model, eligibility, MILP & complexity
├── Member 2 – Study Guide.pdf               # Online algorithms, bounds, KVV & baselines
├── Member 3 – Study Guide.pdf               # Learning-augmented FTPS, proofs & safeguards
├── Member 4 – Study Guide.pdf               # Experiments, simulation, fairness & code
└── Complete Project Overview & Team Coordination.pdf # Team coordination & viva defense
```

---

## 🚀 Installation & Running

### 1. Requirements
Ensure Python 3.10+ is installed:
```bash
pip install -r requirements.txt
```

### 2. Run Invariant & Unit Tests
```bash
python3 -m unittest tests/test_suite.py
```

### 3. Run Benchmark Experiments & Generate Plots
```bash
python3 experiments/run_experiments.py
```

### 4. Compile All 5 Viva Study Guides and PDFs
```bash
python3 pdf_generator/generate_all_pdfs.py
```

---

## 📊 Summary of Experimental Results
- **Consistency:** At $\eta = 0.0$ prediction error, FTPS achieves **$0.9903$** competitive ratio.
- **Robustness:** At $\eta = 1.0$ (pure noise), FTPS activates safeguard to achieve **$0.9208$** competitive ratio, exactly matching the robust Water-Filling baseline.
- **Adversarial Resilience:** While Greedy collapses to **$0.5000$** under adversarial attacks, FTPS maintains **$0.5833 - 0.6875$** and KVV Ranking achieves **$0.7188 - 0.7500$**.
- **Workload Fairness:** Water-Filling and FTPS preserve Jain's Fairness Index above **$0.72$**, preventing responder burnout observed in Greedy (dropping to $0.56$).

